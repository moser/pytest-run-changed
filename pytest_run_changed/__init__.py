import collections
import functools
import itertools
import json
import operator
import pathlib
import subprocess
import sys

import pytest

PATH = pathlib.Path(".pytest-deps")
DEPS = set()
TEST_FILES = set()


def pytest_addoption(parser):
    group = parser.getgroup("run-changed")
    group.addoption(
        "--dirty",
        action="store_true",
        dest="dirty",
        help="",
    )


def pytest_unconfigure():
    key = operator.itemgetter(0)
    indexed = {
        caller: set(c for _, c in called)
        for caller, called in itertools.groupby(sorted(DEPS, key=key), key=key)
    }

    result = {}

    for tf in TEST_FILES:
        mod_set = {tf}
        new = True
        while new:
            new = [indexed.get(tf, set()) for fname in tf]
            new = functools.reduce(lambda x, y: x.union(y), new, set())
            new = new.difference(mod_set)
            mod_set = mod_set.union(new)
        result[tf] = mod_set

    del indexed

    result = {tf: list(mod_set) for tf, mod_set in result.items()}

    if PATH.exists():
        with open(PATH, "r") as fp:
            old_index = json.load(fp)
        for tf, mod_set in result.items():
            old_index[tf] = mod_set
        result = old_index

    with open(PATH, "w") as fp:
        json.dump(result, fp, sort_keys=True, indent=4)


def pytest_runtest_makereport(item, call):
    pass


def pytest_collection_modifyitems(session, config, items):
    dirty_only = config.getoption("dirty")
    if dirty_only and PATH.exists():
        with open(PATH, "r") as fp:
            inverse_file_index = json.load(fp)
        file_index = collections.defaultdict(set)
        for tf, mod_set in inverse_file_index.items():
            for mod in mod_set:
                file_index[mod].add(tf)

        dirty = get_dirty_files()

        selected_test_files = [set(file_index.get(fname, [])) for fname in dirty]
        selected_test_files = functools.reduce(
            lambda x, y: x.union(y), selected_test_files, set()
        )

        unknown_test_files = {
            item.module.__file__
            for item in items
            if item.module.__file__ not in file_index
        }

        items[:] = [
            item
            for item in items
            if item.module.__file__ in selected_test_files
            or item.module.__file__ in unknown_test_files
        ]


@pytest.fixture(scope="function", autouse=True)
def profile(request):
    if request.config.getoption("dirty"):
        TEST_FILES.add(request.node.module.__file__)

        def trace_calls(frame, event, arg):
            if event != "call":
                return
            func_filename = frame.f_code.co_filename
            caller_filename = frame.f_back.f_code.co_filename
            if func_filename != caller_filename:
                DEPS.add((caller_filename, func_filename))
            return

        sys.settrace(trace_calls)
        yield
        sys.settrace(None)
    else:
        yield


def get_dirty_files():
    proc = subprocess.run(["git", "status", "--porcelain"], stdout=subprocess.PIPE)
    proc.check_returncode()
    modified = set()
    untracked = set()
    for line in proc.stdout.decode().splitlines():
        action, fname = line[0:3], line[3:]
        if action == " M ":
            modified.add(fname)
        elif action == " D ":
            modified.add(fname)
        elif action == "?? ":
            fname = pathlib.Path(fname)
            if fname.is_dir():
                for ffname in fname.glob("*"):
                    untracked.add(str(ffname))
            else:
                untracked.add(str(fname))

    return {str(pathlib.Path(fname).absolute()) for fname in modified.union(untracked)}

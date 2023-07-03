# pytest run changed

When applying TDD, a key to successful, fast development is quick feedback.
This plugin tries to shorten the time to feedback by only running tests that
could be failing.It does so by tracking dependencies between test and source
files and only running tests which depend on files changed according to `git
status`.


## Installation

```bash
pip install pytest-run-changed
```

## Usage

```bash
pytest --changed-only
```

The first time (or after you deleted `.pytest-deps`) this will run all tests to
gather the dependencies between test and source files. Afterwards it will only
run tests in files that depend on source files that have unstaged changes in
git.  New test files (or more generally test files that have no info in
`.pytest-deps`) will be run, too.


## Options

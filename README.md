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



## License: [MIT](https://opensource.org/licenses/MIT)

Copyright 2021 Martin Vielsmaier

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

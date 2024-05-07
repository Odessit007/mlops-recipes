* [Intro](#intro)
* [Usage](#usage)
* [Rules](#rules)



<a id="intro"></a>
# Intro

[Ruff](https://github.com/astral-sh/ruff) is an extremely fast Python linter, written in Rust. Some of its features:
* it claims to be 10-100x faster than the other existing linters;
* has built-in caching to avoid re-analyzing unchanged files;
* can be used to replace Flake8, isort, pydocstyle, yesqa, eradicate, pyupgrade, and autoflake;
* autofix support, for automatic error correction (e.g., automatically remove unused imports);

Ruff is **not** near equivalent to Pylint yet.

Run `pip install ruff` or `pdm add ruff` to install Ruff.

To run Ruff over the project, go to the project's root and run `ruff check .`.

Ruff can identify some check failures as fixable: for example, unused imports can easily be removed, and this can be
done by Ruff via the `ruff check --fix .` command.

Full list of rules that Ruff supports is available [here](https://beta.ruff.rs/docs/rules/).

Ruff can be configured in several ways including pyproject.toml. Full list of the available settings is
[here](https://beta.ruff.rs/docs/settings/).



<a id="usage"></a>
# Usage

```bash 
ruff check .                        # Lint all files in the current directory (and any subdirectories)
ruff check path/to/code/            # Lint all files in `/path/to/code` (and any subdirectories)
ruff check path/to/code/*.py        # Lint all `.py` files in `/path/to/code`
ruff check path/to/code/to/file.py  # Lint `file.py`
```

Look [here](https://beta.ruff.rs/docs/usage/) for examples of using Ruff with pre-commit and GitHub Actions.

Ruff's pre-commit hook should be placed after other formatting tools, such as Black and isort, unless you enable autofix, 
in which case, Ruff's pre-commit hook should run before Black, isort, and other formatting tools, as Ruff's autofix 
behavior can output code changes that require reformatting.



<a id="rules"></a>
# Rules

Ruff supports multiple rule groups. The current (as of 31 Jul 2023) rule groups are:

| Prefix | Name                       |
|--------|----------------------------|
| F      | Pyflakes                   |
| E      | pycodestyle, errors        |
| W      | pycodestyle, warnings      |
| C90    | mccabe                     |
| I      | isort                      |
| N      | pep8-naming                |
| D      | pydocstyle                 |
| UP     | pyupgrade                  |
| YTT    | flake8-2020                |
| ANN    | flake8-annotations         |
| ASYNC  | flake8-async               |
| S      | flake8-bandit              |
| BLE    | flake8-blind-except        |
| FBT    | flake8-boolean-trap        |
| B      | flake8-bugbear             |
| A      | flake8-builtins            |
| COM    | flake8-commas              |
| CPY    | flake8-copyright           |
| C4     | flake8-comprehensions      |
| DTZ    | flake8-datetimez           |
| T10    | flake8-debugger            |
| DJ     | flake8-django              |
| EM     | flake8-errmsg              |
| EXE    | flake8-executable          |
| FA     | flake8-future-annotations  |
| ISC    | flake8-implicit-str-concat |
| ICN    | flake8-import-conventions  |
| G      | flake8-logging-format      |
| INP    | flake8-no-pep420           |
| PIE    | flake8-pie                 |
| T20    | flake8-print               |
| PYI    | flake8-pyi                 |
| PT     | flake8-pytest-style        |
| Q      | flake8-quotes              |
| RSE    | flake8-raise               |
| RET    | flake8-return              |
| SLF    | flake8-self                |
| SLOT   | flake8-slots               |
| SIM    | flake8-simplify            |
| TID    | flake8-tidy-imports        |
| TCH    | flake8-type-checking       |
| INT    | flake8-gettext             |
| ARG    | flake8-unused-arguments    |
| PTH    | flake8-use-pathlib         |
| TD     | flake8-todos               |
| FIX    | flake8-fixme               |
| ERA    | flake8-eradicate           |
| PD     | pandas-vet                 |
| PGH    | pygrep-hooks               |
| PL     | Pylint                     |
| TRY    | tryceratops                |
| FLY    | flynt                      |
| NPY    | NumPy-specific rules       |
| AIR    | Airflow                    |
| PERF   | Perflint                   |
| RUF    | Ruff-specific rules        |

By default, Ruff enforces the E- and F-prefixed rules. The set of enabled rules is determined by the `select` and `ignore` 
options, which accept either the full code (e.g., F401) or the prefix (e.g., F). An example configuration with pyproject.toml:
```toml
[tool.ruff]
select = [
  "E",   # pycodestyle
  "F",   # pyflakes
  "UP",  # pyupgrade
]
```

You can ignore rules by  adding comments to your code (if you're using Black, note that Black might move these comments):
* ignore rule <id> for the given line: add `# noqa: <id>` comment at the end of the line (example: `# noqa: UP006`);
* ignore rule <id> for the entire file: add `# ruff: noqa: <id>` at the top of the file

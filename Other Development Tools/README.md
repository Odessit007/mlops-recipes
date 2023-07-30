Modern software development is much more than writing and testing code.

It is a good practice to enforce certain code style for the project.([Black](https://github.com/psf/black)) can format 
the code for you, so you don't need to do much manual work - just commit the changed files. Black is highly opinionated, 
i.e. there are very few options you can tune, so it's not a trivial decision to use it. It might be a good idea to see 
examples of what it does to the code and understand the small number of formatting options that Black allows.

<br/>

Checking code quality beyond the tests is also important.

Linters can assess the code quality: they don't only check the style, but also can find certain bugs, estimate code
complexity, etc. Some of the most popular options today (31 Jul 2023) are [Pylint](https://github.com/pylint-dev/pylint)
and [Ruff](https://github.com/astral-sh/ruff). Pylint is very thorough aiming at the highest code quality at the cost
of being probably the slowest of all linters and resulting significant number of false positive alerts. Ruff is written
in Rust and is probably the fastest linter. It has autofix support for automatic error correction and tries to replace
other popular code quality tools such as Flake8, isort, pydocstyle, yesqa, eradicate, pyupgrade, and autoflake, but
can't fully replace Pylint at the moment.

Code safety is yet another dimension of code quality. ([Bandit](https://github.com/PyCQA/bandit)) can find some common
security issues. Several tools can perform static typing to ensure that you’re using variables and functions correctly.
At least four tools are popular:
* [mypy](https://github.com/python/mypy);
* [pyre-check](https://github.com/facebook/pyre-check) from Facebook;
* [pytype](https://github.com/google/pytype/) from Google;
* [pyright](https://github.com/microsoft/pyright) from Microsoft.

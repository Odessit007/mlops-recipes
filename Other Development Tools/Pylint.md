* [Intro](#intro)
* [How to run](#how-to-run)
* [Messages](#messages)
  * [Messages control](#messages-control)



<a id="intro"></a>
# Intro
Installation: `pip install pylint`, `pdm add pylint`
    * or use `pylint[spelling]` to also check spelling with `enchant` (you might need to 
[install the enchant C library](https://pyenchant.github.io/pyenchant/install.html#installing-the-enchant-c-library))

Run `pylint --help` or `pylint --long-help` to get a basic or detailed help message.



<a id="how-to-run"></a>
# How to run

You can run Pylint on a given Python module or package with `pylint [options] <modules_or_packages>`. Some details:
* `pylint mymodule.py` should always work since the current working directory is automatically added on top of the python path
* `pylint directory/mymodule.py` will work if `directory` is a python package (i.e. has an `__init__.py` file), an 
implicit namespace package or if `director`y is in the python path (you can control it via `PYTHONPATH` environment
variable).

You can also use globbing patterns: `pylint [options] package/*/src`.

`options` can be "local", specific to certain checkers in Pylint, or "global" that control the general behavior of Pylint.

It's possible to speed up Pylint by spreading work across computer's cores. This is controlled by `-j` flag:
* `-j 0` will make Pylint use the total number of CPUs
* `-j <n>` will spawn `n` parallel Pylint sub-processes and each provided module will be checked in parallel.
Discovered problems by checkers are not displayed immediately. They are shown just after checking a module is complete.

Other useful global options:
* `--ignore=<file,[file...]>`: files or directories to be skipped - they should be base names, not paths;
* `--output-format=<format>`: select output format (text, json, custom);
* `--list-msgs-enabled`: display a list of messages that are enabled and disabled with the given configuration;
* `--list-groups`: display a list of groups of checks.

A full list of options is available [here](https://pylint.readthedocs.io/en/latest/user_guide/configuration/all-options.html).

Pylint can be configured not only via command line options, but in many ways including pyproject.toml.
Use `pylint --generate-toml-config` to generate a sample TOML file with settings and their default values, that can 
then be copied into the pyproject.toml. In practice, it is often better to create a minimal configuration file which 
only contains configuration overrides.


<a id="messages"></a>
# Messages

When you run Pylint it outputs a bunch of **messages**. For example, running `pylint my_module.py` may result into two
messages:
```
************* Module simplecaesar
my_module.py:1:0: C0114: Missing module docstring (missing-module-docstring)
my_module.py:5:0: C0103: Constant name "shift" doesn't conform to UPPER_CASE naming style (invalid-name)
```

The messages include the **message symbol** (shown in parentheses at the end): `missing-module-docstring` and 
`invalid-name` in the example above. You can get information about the message using its id: `pylint --help-msg=<id>`. For example,
``` 
pylint --help-msg=missing-module-docstring
```

There are 5 main categories of messages :

| Category (short) | Category name | Description                                                            | Exit code |
|------------------|---------------|------------------------------------------------------------------------|-----------|
| C                | convention    | programing standard violation                                          | 16        |
| R                | refactor      | bad code smell                                                         | 8         |
| W                | warning       | Python specific problems                                               | 4         |
| E                | error         | Probable bugs in the code                                              | 2         |
| F                | fatal         | An error occurred which prevented Pylint from doing further processing | 1         |

All the currently supported messages (and their categories) are listed [here](https://pylint.readthedocs.io/en/latest/user_guide/messages/messages_overview.html#messages-overview).

Additional status codes are 0 if everything went fine and 32 if there was an usage error.


<a id="messages-control"></a>
## Messages control

In order to control messages, Pylint accepts the following values:
* a symbol: `no-member`, `undefined-variable`, etc.;
* a numerical ID: `E1101`, `E1102`, etc.;
* the name of the group of checks: `typecheck`, `variables`, etc.;
* category of the checks: `C`, `R`, `W`, `E`, `F`;
* all the checks: `all`.

The user can disable or enable certain message types or symbols. To enforce that only specific types/symbols are used,
the following flag combination can be used: `pylint --disable=all --enable=<symbols>` where `<symbols>` can be a
comma-separated list mixing checkers, message symbols and categories like `-d C,W,no-error,design`.

You can [use comments](https://pylint.readthedocs.io/en/latest/user_guide/messages/message_control.html#block-disables)
to control which parts of code should not be checked.

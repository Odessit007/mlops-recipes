* [Intro](#intro)
* [Dotenv file syntax](#syntax)
* [Python code](#python-code)
* [CLI](#cli)
* [IPython](#ipython)



<a id="intro"></a>
# Intro
If your project requires environment variables, and you have different sets of those (dev vs prod, or maybe
different data sources are configured by them, etc.) then it's convenient to store all of them in a single file.

`python-dotenv` is a package that helps with these.

The following is based on the [package's GitHub page](https://github.com/theskumar/python-dotenv).

Some basic information:
* The default location of the dotfile is the file called `.env` in the root of the current working directory.
* The tool can be used from Python code or via CLI.



<a id="syntax"></a>
# Dotenv file syntax
The basics of dotenv file syntax:
* The syntax of .env files supported by python-dotenv is similar to that of Bash:
```bash
# Development settings
DOMAIN=example.org
ADMIN_EMAIL=admin@${DOMAIN}
ROOT_URL=${DOMAIN}/app
```
* If you use variables in values, ensure they are surrounded with `{` and `}`, like `${DOMAIN}`, as bare variables
such as `$DOMAIN` are not expanded.
* Keys can be unquoted or single-quoted.
* Values can be unquoted, single- or double-quoted.
* Spaces before and after keys, equal signs, and values are ignored.
* Values can be followed by a comment.
* Lines can start with the `export` directive, which does not affect their interpretation.
* A variable can have no value:
```
FOO
```
  * It results in `dotenv_values` associating that variable name with the value `None` (e.g. `{"FOO": None}`.
  * `load_dotenv`, on the other hand, simply ignores such variables.
  * This shouldn't be confused with `FOO=`, in which case the variable is associated with the empty string.



<a id="python-code"></a>
# Python code

Run the following to make values from the `.env` file accessible via usual `os.environ` and `os.getenv` commands`:
```python
from dotenv import load_dotenv
load_dotenv()
```

By default, `load_dotenv` doesn't override existing environment variables, but you can make it do so:
* `load_dotenv` and its equivalent `load_dotenv(override=False)` search for the variable value in the following order:
the value in the environment, then `.env` file, then the default value (if provided, otherwise an empty string)
* `load_dotenv(override=True)` search for the variable value in the following order:
`.env` file, then the value in the environment, then the default value (if provided, otherwise an empty string)

Run the following to get the variables stored in the `.env` file without touching the envrionment:
```python
from dotenv import dotenv_values

config = dotenv_values(".env")  # Will return a dictionary with the values stored in `.env.secret` file
```

The following snippet will override the values from two dotenv files with the values from the environment, and keep
the values that are not set in the environment:
```python
config = {
    **dotenv_values(".env.shared"),  # load shared development variables
    **dotenv_values(".env.secret"),  # load sensitive variables
    **os.environ,  # override loaded values with environment variables
}
```

Both `load_dotenv` and `dotenv_values` accept `io` streams via the `stream` argument, so you can load variables
from the stream rather than from the file:
```python
from io import StringIO

from dotenv import load_dotenv

config = StringIO("USER=foo\nEMAIL=foo@example.org")
load_dotenv(stream=config)
```



<a id="cli"></a>
# CLI
The tool also includes a CLI that allows to set or unset environment variables in the file without opening it.

`dotenv` CLI accepts some command line options:
* `-f`: specify the dotenv file path, the default value is `.env` file in the current working directory
* `-q`: by default, the values provided to the CLI are quoted:
    * if you run `dotenv -q set A 42` will result into the entry `A='42'` in the .env file
* `-e`: will write dotenv file as an executable bash script, i.e. the entry will be of the form `export {KEY}={VAL}`

The supported commands:
* `dotenv` or `dotenv --help` will print the help message with the list of all subcommands
* `dotenv [COMMAND] --help` will show help message for a specific subcommand
* `dotenv [OPTIONS] set KEY VALUE`: will set `KEY` variable with `VALUE`
    * by default, `dotenv set X 42` will result into `X='42'` entry in the dotenv file
    * `dotenv -q always set X 42` --> `X='42'` (a more verbose version of the default behavior)
    * `dotenv -q never set X 42`  --> `X=42` (no quotes)
    * `dotenv -e true set X 42`   --> `export X='42'`
    * `dotenv -e false set X 42`  --> `X='42'`
    * of course, you can combine `-e` and `-q` options
* `dotenv unset KEY`: unset variable KEY
* `dotenv get KEY`: get the value for variable KEY (will show the value without quotes)
* `dotenv list [OPTIONS]`: list all the stored key/value pairs.
    * accepts an optional `--format` option, described below
* `dotenv run [CMD]`: run given command with the variables loaded from dotenv file



<a id="ipython"></a>
# IPython
You can also use dotenv as an IPython extension:
```
%load_ext dotenv
%dotenv [Optional path to .env file]
```

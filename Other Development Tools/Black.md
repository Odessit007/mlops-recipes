* [Intro](#intro)
* [Configuration](#configuration)



<a id="intro"></a>
# Intro

[Black](https://black.readthedocs.io/en/stable/index.html) is an auto-formatting tool. It changes your files enforcing 
a unified code style across your code base. The style docs are available [here](https://black.readthedocs.io/en/stable/the_black_code_style/current_style.html).

Installation: `pip install black`, `pdm add black`, etc.

Basic usage: `black <file_or_directory>`.

Black has integrations with
* [GitHub Actions](https://black.readthedocs.io/en/stable/integrations/github_actions.html)
* [pre-commit](https://black.readthedocs.io/en/stable/integrations/source_version_control.html#version-control-integration)

If `--exclude` is not set, Black will automatically ignore files and directories in .gitignore file(s), if present.
If you want Black to continue using .gitignore while also configuring the exclusion rules, please use `--extend-exclude`.

Black is a well-behaved Unix-style command-line tool:
* it does nothing if it finds no sources to format;
* it will read from standard input and write to standard output if `-` is used as the filename;
* it only outputs messages to users on standard error;
* exits with code 0 unless an internal error occurred or a CLI option prompted it.



<a id="configuration"></a>
# Configuration

Command line options have defaults that you can see in `--help`. A pyproject.toml can override those defaults. 
Finally, options provided by the user on the command line override both. The option keys in pyproject.toml are the same 
as long names of options on the command line. The full list of options is available
[here](https://black.readthedocs.io/en/stable/usage_and_configuration/the_basics.html#command-line-options)). Below,
I summarize the once that I find the most useful (sorted by the long name):
* `--check` (exit with code 1 if any file would be reformatted; code 0 if nothing would change;
code 123 if there was an internal error)
* `--diff` (print to stdout a diff that indicates what changes Black would have made instead of reformatting files)
  * if you like colored diffs, add `--color` flag
* `--exclude`: a regular expression that matches files and directories that should be excluded on recursive searches.
  * An empty value means no paths are excluded.
  * Exclusions are calculated first, inclusions later.
* `--force-exclude`: like `--exclude`, but files and directories matching this regex will be excluded even when they are 
passed explicitly as arguments. This is useful when invoking Black programmatically on changed files, such as in a 
pre-commit hook or editor plugin.
* `--include`: a regular expression that matches files and directories that should be included on recursive searches.
  * An empty value means all files are included regardless of the name.
  * Exclusions are calculated first, inclusions later.
* `-l, --line-length`: how many characters per line to allow (default 88).
* `-q, --quiet` will cause Black to stop emitting all non-critical output. Error messages will still be emitted 
(which can silenced by 2>/dev/null).
* `--required-version`: require a specific version of Black to be running. This is useful for ensuring that all contributors
to your project are using the same version, because different versions of Black may format code a little differently.
* `-C, --skip-magic-trailing-comma`: by default, Black uses existing trailing commas as an indication that short lines 
should be left separate. If this option is given, the magic trailing comma is ignored.
* `-S, --skip-string-normalization`: by default, Black uses double quotes for all strings and normalizes string prefixes. 
If this option is given, strings are left unchanged instead.
* `-t, --target-version`: Python versions that should be supported by Black's output (should include all versions that
your code supports). Black uses this option to decide what grammar to use to parse your code and potentially to decide
what style to use. Examples:
  * command line: `-t py37 -t py38 -t py39 -t py310`
  * pyproject.toml: `target-versions = ["py37", "py38", "py39", "py310"]`
* `-v, --verbose`: will cause Black to emit files modified and error messages, plus a short summary.  If Black is using 
a configuration file, a blue message detailing which one it is using will be emitted.
* `-W, --workers`: when Black formats multiple files, it may use a process pool to speed up formatting. This option 
controls the number of parallel workers.

By default, Black reformats the files given and/or found in place. Sometimes you need Black to just tell you what it 
would do without actually rewriting the Python files. There are two flags to control this (both can be enabled at once):
`--check` and `--diff` (see above).

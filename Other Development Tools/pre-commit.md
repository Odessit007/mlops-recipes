* [Intro](#intro)
* [Installation](#install)
* [Config file](#config)
  * [Repository local hooks](#local-hooks)
* [Installing and updating hooks](#hooks-management)
* [Running hooks](#running-hooks)



<a id="intro"></a>
# Intro

Git events (commit, push, etc.) can trigger scripts that do something useful. When the event happens (say, user runs 
`git push` command), the script runs and this script can perform some action and potentially block the Git flow.
For example, the script triggered after `git push` might run unit tests and block the actual push if those fail. 
Or the `git commit` may trigger the formatting of the source code and prevent the actual commit if any of the committed 
files had formatting issues (the user can then re-commit the files with changes). The examples below are mostly for Python, 
but `pre-commit` works with any language.

Some things that might be happening in such scripts (called "hooks") and some examples of the tools that might be used:
* reformat code ([black](https://github.com/psf/black));
* check style ([ruff](https://github.com/astral-sh/ruff));
* do static type checking based on type hints ([mypy](https://github.com/python/mypy));
* upgrade Python code for newer language version ([pyupgrade](https://github.com/asottile/pyupgrade));
  * use `--py{version}-plus` to apply changes relevant for Python >= given version (for example, `--py38-plus`);
* run tests ([pytest](https://github.com/pytest-dev/pytest));
* find common security issues ([bandit](https://github.com/PyCQA/bandit));
* `pre-commit` itself supports a bunch of built-in utilities including:
  * `check-added-large-files`: prevents giant files from being committed; 
  * `check-ast`: simply checks whether the files parse as valid Python;
  * `check-json`, `chek-toml`, `chek-xml`, `chek-yaml`: checks that JSON/TOML/XML/YAML files are parseable
  * `check-shebang-scripts-are-executable`: ensures that (non-binary) files with a shebang are executable;
  * `pretty-format-json`: sets a standard for formatting JSON files;
  * `check-merge-conflict`: checks for files that contain merge conflict strings;
  * `detect-aws-credentials`: detects *your* aws credentials from the aws cli credentials file;
  * `end-of-file-fixer`: ensures that a file is either empty, or ends with one newline;
  * `file-contents-sorter` - sorts the lines in specified files (defaults to alphabetical).
You must provide list of target files as input in your .pre-commit-config.yaml file
* and [many more options](https://pre-commit.com/hooks.html)



<a id="install"></a>
# Installation

Package name: `pre-commit`. Use this name with your favourite package management tool, for example,
```bash
pip install pre-commit
pdm install -d pre-commit
```

Check that installation was successful: `pre-commit --version`.



<a id="config"></a>
# Config file

The hooks are defined in a file called `.pre-commit-config.yaml` and located in the root of your project (you can 
generate a sample file with `pre-commit sample-config`). An example using `black` and `ruff`:
```yaml
repos:
- repo: https://github.com/pre-commit/pre-commit-hooks
  rev: v2.3.0
  hooks:
    - id: check-yaml
    - id: end-of-file-fixer
    - id: trailing-whitespace
- repo: https://github.com/psf/black
  rev: 23.7.0
  hooks:
    - id: black
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.0.280
  hooks:
    - id: ruff
```

In this example, `repos` is the only top-level field. Some other interesting options include:
* `files`: (optional: default `''`) global file include pattern;
* `exclude`: (optional: default `^$`) global file exclude pattern;
* `fail_fast`: (optional: default `false`) set to `true` to have pre-commit stop running hooks after the first failure.

The `repos` field contains a list of repository mappings, each of which specifies three fields:
* `repo`: the repository url to `git clone` from;
* `rev`: the revision or tag to clone at;
* `hooks`: a list of hook mappings which in turn contains the following fields (this is an incomplete list, a
full list is [here](https://pre-commit.com/#pre-commit-configyaml---hooks)):
  * `id`: which hook from the repository to use;
  * `name`: (optional) override the name of the hook - shown during hook execution;
  * `files`: same as the global one, overrides the global one;
  * `exclude`: same as the global one, overrides the global one;
  * `stages`: (optional) selects which [git hook(s)](#git-hooks-list) to run for;
  * `verbose`: (optional) if `true`, forces the output of the hook to be printed even when the hook passes;
  * `log_file`: (optional) if present, the hook output will additionally be written to a file when the hook fails or 
`verbose` is `true`.

  
<a id="local-hooks"></a>
## Repository local hooks
Instead of pulling hooks from the remote repositories, one can configure everything to be fully local. For this,
hook's `repo` field should have the value `local` instead of Git repository.

A local hook must define
* `id`: the id of the hook - used in pre-commit-config.yam;
* `name`: the name of the hook - shown during hook execution;
* `language`: the language of the hook - tells pre-commit how to install the hook;
  * use the value `system` if the tool used in a hook becomes a system command after installation;
* `entry`: the entry point - the executable to run. `entry` can also contain arguments that will not be overridden 
such as `entry: autopep8 -i`;
* `files`: (optional: default `''`) the pattern of files to run on;
* `types`: (optional: default `^$`) exclude files that were matched by files.

Here's an example configuration with a single local hook (there can be many):
```yaml
- repo: local
  hooks:
  - id: pylint
    name: pylint
    entry: pylint
    language: system
    types: [python]
    require_serial: true
```



<a id="hooks-management"></a>
# Installing and updating hooks

Install the git hooks script: `pre-commit install`. Every time you clone a project using pre-commit running `pre-commit 
install` should always be the first thing you do.

You can also automatically enable pre-commit on your repository, so that any newly cloned repository will automatically 
have the hooks set up without the need to run `pre-commit install`:
```bash
git config --global init.templateDir ~/.git-template
pre-commit init-templatedir ~/.git-template
```

See more info in the [docs](https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories).

<br/>

You can install `pre-commit` for particular git hooks passing a `--hook-type` option to `pre-commit install`:
```bash
pre-commit install --hook-type pre-commit --hook-type pre-push
```

<a id="git-hooks-list"></a>
The supported git hooks are:
* commit-msg
* post-checkout
* post-merge
* post-rewrite
* pre-commit
* pre-merge-commit
* pre-push
* pre-rebase
* prepare-comit-msg

You can also specify git hooks for specific hook via the `stages` field as shown in the [Config file](#config) section.

<br/>

Update hooks to the latest version: `pre-commit autoupdate`. By default, this will bring the hooks to the latest tag on the default branch.

<br/>

Uninstall the pre-commit script: `pre-commit uninstall`. Options:
* `-t <hook_type>, --hook-type <hook_type>`: which hook type to uninstall

<br/>

pre-commit can also be used as a tool for continuous integration. For instance, adding `pre-commit run --all-files` as
a CI step will ensure everything stays in tip-top shape. To check only files which have changed, which may be faster, 
use something like `pre-commit run --from-ref origin/HEAD --to-ref HEAD`.

The relevant docs:
* [official pre-commit GitHub section](https://github.com/pre-commit/action)
* [pre-commit docs](https://pre-commit.com/#github-actions-example)



<a id="running-hooks"></a>
# Running hooks
By default, pre-commit runs only on the changed files.
If you want to manually run all pre-commit hooks on a repository, run `pre-commit run --all-files`. 
To run individual hooks use `pre-commit run <hook_id>`.

The first time pre-commit runs on a file it will automatically download, install, and run the hook. Note that running a 
hook for the first time may be slow. For example: If the machine does not have node installed, pre-commit will download 
and build a copy of node.

You can disable all hooks by adding `--no-verify` flag to your git command.

You can disable specific hooks via the `SKIP` environment variable that contains a comma-separated list of hook ids:
```bash
SKIP=ruff,pytest git commit -m "bla-bla-bla"
```

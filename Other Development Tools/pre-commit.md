* [Intro](#intro)
* [Installation](#install)
* [Config file](#config)
* [Installing and updating hooks](#hooks-management)
* [Running hooks](#running-hooks)



<a id="intro"></a>
# Intro

Git events (commit, push, etc.) can trigger scripts that do something useful. When the event happens (say, user runs 
`git push` command), the script runs and this script can perform some action and potentially block the Git flow.
For example, the script triggered after `git push` might run unit tests and block the actual push if those fail. 
Or the `git commit` may trigger the formatting of the source code and prevent the actual commit if any of the commited 
files had formatting issues (the user can then re-commit the files with changes). The examples below are mostly for Python, 
but `pre-commit` works with any language.

Some things that might be happening in such scripts (called "hooks") and some examples of the tools that might be used:
* reformat code ([black](https://github.com/psf/black));
* check style ([ruff](https://github.com/astral-sh/ruff));
* do static type checking based on type hints ([mypy](https://github.com/python/mypy));
* upgrade Python code for newer language version ([pyupgrade](https://github.com/asottile/pyupgrade));
* run tests ([pytest](https://github.com/pytest-dev/pytest));
* and many more things -- a full list of supported hooks is available [here](https://pre-commit.com/hooks.html).



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

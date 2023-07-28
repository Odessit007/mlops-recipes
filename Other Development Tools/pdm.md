* [Intro](#intro)
* [Package management](#packages)
    * [pdm add](#pdm-add)
    * [pdm update](#pdm-update)
    * [Some other important commands](#other-commands)



<a id="intro"></a>
# Intro

[PDM](https://pdm.fming.dev/latest/) is yet another Python packaging tool (there are quite a lot with pip being the 
classical one and Pipenv, Poetry, pip-tools, and PDM being some popular newcomers). PDM and Poetry have the largest
number of features including virtual environment and pyproject.toml management, package version locking, package
publishing, etc. As far as I see on the Internet, PDM is more conformant to the PEP conventions than Poetry, so that's why
I'm describing it here.

PDM requires Python version 3.7 or higher and can be installed on Linux, Mac, and Windows.
Check the [installation guide](https://pdm.fming.dev/latest/#installation) for how to install PDM on your platform.

To start a new project with PDM, go to the project folder and run `pdm init` that will ask you a bunch of questions
to configure PDM. The very first question asks you to specify the base Python interpreter.
* PDM can automatically create a virtual environment for you using the base interpreter (this will live in a `.venv/` 
subdirectory inside the project directory);
* or you can use an interpreter that is already living inside a virtual environment.

I had troubles making the default PDM environment work in PyCharm, so I came up with this flow:
* create a new environment and attach its interpreter to the project in whatever way you typically do it with PyCharm
* run `pdm init` and select the interpreter living in this environment.

The interpreter path will be stored in `.pdm-python` and used by subsequent commands. You can also change it later with `pdm use`.

Alternatively, you can specify the Python interpreter path via `PDM_PYTHON` environment variable. When it is set, the path saved in `.pdm-python` will be ignored.

If you're migrating to PDM from some other tool, you can use `pdm import` command to init the project using
* Pipenv's Pipfile
* Poetry's or Flit's section in pyproject.toml
* pip's requirements.txt
* setuptools' setup.py (this one is slightly more tricky than the rest -- check 
[the docs](https://pdm.fming.dev/latest/usage/project/#import-the-project-from-other-package-managers))

PDM will create `pyproject.toml` that contains project's build metadata and dependencies needed for PDM. The pinned
versions of the installed packages will be stored in `pdm.lock` file. These two files should be commited to version control.
`.pmd-python` file stores the Python path used by the **current** project and needn't be shared.

You can use `pdm info` to get information about the current environment (PDM version, Python interpreter path, project root,
where the project packages are stored). `pdm info --env` will provide information about the platform.

The final introductory comment from the [docs](https://pdm.fming.dev/latest/usage/config/#override-the-resolved-package-versions): 
sometimes you can't get a dependency resolution due to incorrect version ranges set by upstream libraries that you
can't fix. In this case you can use PDM's overrides feature to force a specific version of a package to be installed.



<a id="packages"></a>
# Package management

<a id="pdm-add"></a>
## pdm add
Use `pdm add` to install a dependency:
```bash
pdm add requests   # add requests
pdm add requests==2.25.1   # add requests with version constraint
pdm add requests[socks]   # add requests with extra dependency
pdm add "flask>=1.0" flask-sqlalchemy   # add multiple dependencies with different specifiers
```

You can specify package groups using `-G <name>` or `--group <name>` option. Those will be added to the
`[project.optional-dependencies.<name>]` table in the `pyproject.toml` file.

PDM allows to install local, URL-based, and VCS-based dependencies. Check the [docs](https://pdm.fming.dev/latest/usage/dependency/#local-dependencies).

You can hide the credentials in the URL (they will be populated from the environment variables during installation):
```bash
[project]
dependencies = [
  "mypackage @ git+http://${VCS_USER}:${VCS_PASSWD}@test.git.com/test/mypackage.git@master"
]
```

Development-only dependencies can be specified using the `-d/--dev` flag, and you can specify the groups for them as well:
```bash
pdm add -d -G test pytest
```
will result into the following section in `pyproject.toml`:
```bash
[tool.pdm.dev-dependencies]
test = ["pytest"]
```

Local and VCS dependencies can be installed in editable mode (like `pip install -e <package>`), but this is allowed only
for the development dependencies.

If PDM is not able to find a resolution to satisfy the requirements, it will raise an error. For example,
```bash
pdm django==3.1.4 "asgiref<3"
...
🔒 Lock failed
Unable to find a resolution for asgiref because of the following conflicts:
  asgiref<3 (from project)
  asgiref<4,>=3.2.10 (from <Candidate django 3.1.4 from https://pypi.org/simple/django/>)
To fix this, you could loosen the dependency version constraints in pyproject.toml. If that is not possible, you could also override the resolved version in `[tool.pdm.resolution.overrides]` table.
```

You can either change to a lower version of `django` or remove the upper bound of `asgiref`.
But if it is not eligible for your project, you can try [overriding the resolved package versions](https://pdm.fming.dev/latest/usage/config/#override-the-resolved-package-versions) 
in `pyproject.toml`.



<a id="pdm-update"></a>
## pdm update

pdm can manage package updates via `pdm update` command:
* `pdm update`: update all dependencies in the lockfile
* `pdm update <package>`: update specific package
* `pdm update -G <group_1> -G <group_2>`: update specific group(s) of dependencies
  * `pdm update -G "<group_1>,<group_2>"`: equivalent syntax
* `pdm update -G <group> <package>`: update a given package in a given group
* `pdm update -d`: update all dev dependencies
* `pdm update -d -G <group> <package>`: update a given package in a given dev group
  * for example, `pdm update -d -G test pytest`


<a id="other-commands"></a>
## Some other important commands
* `pdm export -o requirements.txt`: export dependencies in `requirements.txt` format
* `pdm install`: checks the project file for changes, updates the lock file if needed, then `sync`
* `pdm list`: show installed packages
  * `pdm list --graph`: show a dependency graph
* `pdm remove`: remove packages
  * `pdm remove <package>`: remove a given package from the default dependencies
  * `pdm remove -G <group> <packae>`: remove a given package from a given group
  * `pdm remove -dG <group> <package>`: remove a given package from a given dev group
* `pdm run [options] [script]`: run commands or scripts with local packages loaded
* `pdm sync`: installs packages from the lock file
  * `--clean`: removes packages no longer in the lockfile
  * `pdm update` consists of two steps: first it updates the lock file, then runs `sync`
* `pdm search <package>`: searches for PyPI packages
* `pdm show <package>`: show the package information (the package doesn't need to be installed)

* [Intro](#intro)
  * [Prefect server & Prefect Cloud](#prefect-server-cloud)
  * [Configuration](#configuration)
* [Important details](#details)
* [Example](#example)
* [Deployment example](#deployment-example)
* [Logging](#logging)
* [Testing](#testing)



<a id="intro"></a>
# Intro

**Flows** are like functions. They can take inputs, perform work, and return an output. In fact, you can turn 
any function into a Prefect flow by adding the `@flow` decorator. When a function becomes a flow, its behavior changes,
giving it the following advantages:
* It has a **state**, which determines when it can run. Transitions between states are recorded, allowing for flow execution to be observed.
* Input arguments types can be validated.
* Retries can be performed on failure.
* Timeouts can be enforced to prevent unintentional, long-running workflows.
* Metadata about **flow runs**, such as run time and final state, is tracked.

A **task** is a Python function decorated with a `@task` decorator. Tasks are atomic pieces of work that are executed 
independently within a flow. Tasks, and the dependencies between them, are displayed in the flow run graph, enabling you
to break down a complex flow into something you can observe and understand. When a function becomes a task, it can be 
executed concurrently and its return value can be cached.

Flows and tasks share some common features:
* Both are defined easily using their respective decorator, which accepts settings for that flow / task (see all task settings / flow settings).
* Each can be given a name, description and tags for organization and bookkeeping.
* Both provide functionality for retries, timeouts, and other hooks to handle failure and completion events.

In order to schedule flow runs or trigger them based on events or certain conditions, you’ll need to deploy them.
Deploying a flow is the act of specifying where, when, and how it will run. This information is encapsulated and sent 
to Prefect as a **deployment** which contains the crucial metadata needed for orchestration. Deployments elevate 
workflows from functions that you call manually to API-managed entities. Attributes of a deployment include 
(but are not limited to):
* Flow entrypoint: path to your flow function would start the flow
* Work pool: points to the infrastructure you want your flow to run in
* Schedule: optional schedule for this deployment
* Tags: optional text labels for organizing your deployments

Running Prefect flows locally is great for testing and development purposes. But for production settings, Prefect 
work pools and workers allow you to run flows in the environments best suited to their execution.
* Workers and work pools bridge the Prefect orchestration layer with the infrastructure the flows are actually executed on.
* **Work pools**:
  * Respond to polling from the worker
  * Organize and prioritize the flow runs for a worker to pick up and execute
  * Describe the ephemeral infrastructure configuration that the worker will create for each flow run
* **Workers** are light-weight processes that run in the environment where flow runs are executed.
  * Workers kick off flow runs on a certain type of infrastructure (like Process)
![prefect_pools_and_workers.png](..%2F_images%2Fprefect_pools_and_workers.png)


<a id="prefect-server-cloud"></a>
## Prefect server & Prefect Cloud

To run Prefect, you need to start Prefect server locally or to use Prefect cloud. The differences between the two are
mostly related to user roles, authentication and triggers. You can  find them 
[here](https://docs.prefect.io/2.11.3/guides/host/#differences-between-a-prefect-server-and-prefect-cloud).

If you want to run locally, run `prefect server start` to start local Prefect server. You can access the dashboard at
http://127.0.0.1:4200. Use Ctrl + C if you want to stop the server.


<a id="configuration"></a>
## Configuration

One possible approach is to:
* run `prefect config view --show-defaults | grep PROFILES_PATH` to get the current location of the
Prefect profile file (most likely it's `~/.prefect//profiles.toml`)
* add "local" and "cloud" profiles to the file:
```toml
[profiles.cloud]
ACCOUNT='xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxx'
WORKSPACE='xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
PREFECT_API_URL='https://api.prefect.cloud/api/accounts/${ACCOUNT}/workspaces/${WORKSPACE}'
PREFECT_API_KEY='xxx_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

[profiles.local]
PREFECT_API_URL='http://127.0.0.1:4200/api'
```
* run `prefect profile use <profile_name>` or set an environment variable `PREFECT_PROFILE=<profile_name>`

Another approach is to use python-dotenv or some other tool (maybe reading configuration directly from .env, JSON, YAML, TOML, 
whatever without 3d-party packages) and to set the environment variables based on this configuration. 
* All Prefect settings have keys that match the environment variable that can be used to override them.
* This approach is convenient if you need to configure multiple tools, and you don't want to have a separate config file
  for each of them.

If you're mixing the two approaches (both using profiles.toml and setting environment variables), environment variables
will take precedence over the profile.



<a id="details"></a>
# Important details

Some important details:
* All tasks must be called from within a flow. Tasks may not call other tasks directly.
* Not all functions in a flow need be tasks. Use them only when their features are useful.
* Tasks enable concurrency, allowing you to execute multiple tasks asynchronously. This concurrency can greatly enhance 
the efficiency and performance of your workflows. 
* Prefect can capture print statements as info logs by specifying `log_prints=True` in your flow decorator 
(e.g. `@flow(log_prints=True)`).
* To enable caching, specify a `cache_key_fn` — a function that returns a cache key — on your task. You may optionally 
provide a `cache_expiration` timedelta indicating when the cache expires. You can define a task that is cached based on
its inputs by using the Prefect `task_input_hash`.
  * Task results are cached in memory during a flow run and persisted to your home directory by default. Prefect Cloud 
  only stores the cache key, not the data itself.
* Not only can you call tasks within a flow, but you can also call other flows! Child flows are called **subflows** and
allow you to efficiently manage, track, and version common multitask logic. Subflows are a great way to organize your 
workflows and offer more visibility within the UI.
  * Whenever we run the parent flow, a new run will be generated for related functions within that as well. Not only is
  this run tracked as a subflow run of the main flow, but you can also inspect it independently in the UI.
* You can create and configure work pools within the Prefect UI.



<a id="example"></a>
# Example

Example showing flow creation, logging, caching, and retries:
```python
import httpx
from datetime import timedelta
from prefect import flow, task, get_run_logger
from prefect.tasks import task_input_hash


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(hours=1))
def get_url(url: str, params: dict = None):
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_open_issues(repo_name: str, open_issues_count: int, per_page: int = 100):
    issues = []
    pages = range(1, -(open_issues_count // -per_page) + 1)
    for page in pages:
        issues.append(
            get_url.submit(
                f"https://api.github.com/repos/{repo_name}/issues",
                params={"page": page, "per_page": per_page, "state": "open"},
            )
        )
    return [i for p in issues for i in p.result()]



@flow(retries=3, retry_delay_seconds=5)
def get_repo_info(
    repo_name: str = "PrefectHQ/prefect"
):
    repo = get_url(f"https://api.github.com/repos/{repo_name}")
    issues = get_open_issues(repo_name, repo["open_issues_count"])
    issues_per_user = len(issues) / len(set([i["user"]["id"] for i in issues]))
    logger = get_run_logger()
    logger.info(f"PrefectHQ/prefect repository statistics 🤓:")
    logger.info(f"Stars 🌠 : {repo['stargazers_count']}")
    logger.info(f"Forks 🍴 : {repo['forks_count']}")
    logger.info(f"Average open issues per user 💌 : {issues_per_user:.2f}")


if __name__ == "__main__":
    get_repo_info()
```



<a id="deployment-example"></a>
# Deployment example

An example of how to create work pool and start a worker:
```bash
prefect work-pool create --type process my-process-pool  # Create a "Process" type work pool
prefect work-pool ls  # Confirm that the work pool was successfully created
# Check "Work Pool" tab in the Prefect UI to see the new pool
prefect worker start --pool my-process-pool
```

An example of how to create a deployment:
```bash 
prefect deploy  # Interactive
```
or
```bash 
prefect deploy my_flow.py:my_flow -n my-deployment -p my-pool.
```

* When running `prefect deploy` or `prefect init` commands, double check that you are at the root of your repo, 
otherwise the worker may attempt to use an incorrect flow entrypoint during remote execution.
* Ensure that you have pushed any changes to your flow script to your GitHub repo - at any given time, your worker 
will pull the code that exists there.
* A Prefect flow can have more than one deployment. This can be useful if you want your flow to run in different 
execution environments or have multiple different schedules.



<a id="logging"></a>
# Logging

* By default, Prefect displays log messages with INFO level and above
  * You can set the default logging level via `PREFECT_LOGGING_LEVEL` environment variable, for example,
    `PREFECT_LOGGING_LEVEL="DEBUG"`
  * There is a [logging.yml](https://github.com/PrefectHQ/prefect/blob/main/src/prefect/logging/logging.yml) file
    packaged with Prefect that defines the default logging configuration.
* To access the Prefect logger, import `from prefect import get_run_logger` and use it in your flows and tasks.
* To make Prefect log outputs of `print` statements, set `log_prints=True` for a task or flow.
  * This can be configured globally via `PREFECT_LOGGING_LOG_PRINT=True`
* Logs can be [formatted](https://docs.prefect.io/2.11.3/guides/logs/#formatters), but this is out of scope for my notes.
* Logged events are also persisted to the Prefect DB
* By default, Prefect won't capture log statements from libraries that your flows and tasks use. You can tell Prefect 
  to include logs from these libraries with the `PREFECT_LOGGING_EXTRA_LOGGERS=list,of,packages`



<a id="testing"></a>
# Testing

Prefect provides a simple context manager for unit tests that allows you to run flows and tasks against a temporary 
local SQLite database:
```python
from prefect.testing.utilities import prefect_test_harness

@flow
def my_flow():
    return 42

def test_my_flow():
    with prefect_test_harness():
        # run the flow against a temporary testing database
        assert my_flow() == 42
```

To test an individual task, you can access the original function using .fn:
```python
from prefect import flow, task

@task
def my_favorite_task():
    return 42

@flow
def my_favorite_flow():
    val = my_favorite_task()
    return val

def test_my_favorite_task():
    assert my_favorite_task.fn() == 42
```

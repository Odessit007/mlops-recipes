Based on [the official docs](https://testcontainers-python.readthedocs.io/en/latest/README.html).



# Intro
`testcontainers-python` facilitates the use of Docker containers for functional and integration testing.
Check the docs for the currently supported packages.

Installation:
* full suite: `pip install testcontainers`
* individual packages: `pip install testcontainers-[feature]` as in `pip install testcontainers-postgres`



# Some specific examples
## DockerContainer
```python
# class DockerContainer(image: str, docker_client_kw: dict | None = None, **kwargs):
from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_for_logs

with DockerContainer("hello-world") as container:
   delay = wait_for_logs(container, "Hello from Docker!")
```



# Docker in Docker (DinD)
When trying to launch a testcontainer from within a Docker container, e.g., in continuous integration testing, two things have to be provided:
1. The container has to provide a docker client installation. Either use an image that has docker pre-installed (e.g. the official docker images) or install the client from within the Dockerfile specification.
2. The container has to have access to the docker daemon which can be achieved by mounting /var/run/docker.sock or setting the DOCKER_HOST environment variable as part of your docker run command.

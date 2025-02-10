Tech Stack:
* LangChain
* Gemini via Google AI Studio
* Streamlit

Based on:
https://www.youtube.com/watch?v=wUAUdEw5oxM


# Debugging in PyCharm
The main app logic in this project is stored in app.py.
To debug an app change the PyCharm config for app.py:
* select `module` instead of `script`
* set module name to `streamlit`
* set script parameters to `run app.py`


# Issue with torch.classes
The following error was raised for some unclear reason:
```
2025-02-09 02:41:18.631 Examining the path of torch.classes raised:
Traceback (most recent call last):
  File "/Users/ivustianiu/PycharmProjects/mlops-recipes/Projects/Chat with PDF (Streamlit; 1 file)/venv/lib/python3.12/site-packages/streamlit/watcher/local_sources_watcher.py", line 217, in get_module_paths
    potential_paths = extract_paths(module)
                      ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/ivustianiu/PycharmProjects/mlops-recipes/Projects/Chat with PDF (Streamlit; 1 file)/venv/lib/python3.12/site-packages/streamlit/watcher/local_sources_watcher.py", line 210, in <lambda>
    lambda m: list(m.__path__._path),
                   ^^^^^^^^^^^^^^^^
  File "/Users/ivustianiu/PycharmProjects/mlops-recipes/Projects/Chat with PDF (Streamlit; 1 file)/venv/lib/python3.12/site-packages/torch/_classes.py", line 13, in __getattr__
    proxy = torch._C._get_custom_class_python_wrapper(self.name, attr)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
RuntimeError: Tried to instantiate class '__path__._path', but it does not exist! Ensure that it is registered via torch::class_
```

A fix was suggested by https://github.com/VikParuchuri/marker/issues/442:
```python
import torch

torch.classes.__path__ = []
```


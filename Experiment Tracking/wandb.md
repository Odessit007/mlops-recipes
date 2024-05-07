Weights & Biases (aka W&B or wandb) supports
* experiment tracking (both metrics and files);
* model registry
* hyperparameter optimization (aka sweeps)
* some nice visual tools to analyze data, model performance, etc.



The core concept of W&B is a *run* which I treat as a single training run for a fixed set of hyperparameters. Runs are
created via `wandb.init()` method. All parameters of this method are options. Here's an example:
```python
import wandb

run = wandb.init(
    project='project-name',  # If not provided, then 'Uncategorized' project will be used. Each project has its own page in the UI
    notes='Some notes about your project',
    tags=['baseline', 'paper1'],  # Can be used later to filter runs in the UI
    save_code=True,  # whether to save the main script or notebook to W&B
    group='my-group',  # Can group runs together: for example, training on each fold of cross-validation
    job_type='train',  # Can group runs together: train, eval, etc.
    name='My awesome run',  # A short name which will identify this run in the UI
    force=False,  # If True, the script will crush if a suer isn't logged in to W&B
    config={'alpha': 0.5, 'gamma': 3},  # Hyperparameters of a model or settings for a data preprocessing job
    # and some more that control runs behavior and integration with tools like TensorBoard and OpenAI Gym
)
```
* `wandb.init()` returns a `Run` object
* Runs are added to pre-existing projects if that project already exists when you call `wandb.init()`.
* Config keys should not contain `.` in their names, and values should be under 10 MB.
  * W&B docs suggest using dashes or underscores instead of dots.
  * You can pass a nested dictionary to `wandb.config()`. W&B will flatten the names using dots in the W&B backend.
* Config can be assigned when calling `.init()` or by direct access to `wandb.config` attribute:
```python
wandb.config = {'alpha': 0.5, 'gamma': 3}
```
* Config can also be defined in parts throughout the script:
```python
config = {'alpha': 0.5, 'gamma': 3}
run = wandb.init(project='test-project', config=config)
wandb.config['dropout'] = 0.2
wandb.config.update({'lr': 0.01, 'dropout': 0.3})
```
* Config can also be updated [after the run has finished](https://docs.wandb.ai/guides/track/config#set-the-configuration-after-your-run-has-finished)


Badly designed logging can make UI or even training slower than it can be. Here are the
[Limits and Performance hints](https://docs.wandb.ai/guides/track/limits)


To track metrics and artifacts, `wandb.log()` command is used. For example,
```python
wandb.log({'train_loss': 0.35, 'val_loss': 0.68})
```
* By default, when you call `wandb.log` it appends a new step to the history object and updates the summary object.
  * But you can control this behavior via the `step` parameter. This is useful, for example, if you want to log metrics
  in different parts of your program via multiple calls but all these calls describe the same step.


By default, the runs end when you call `wandb.init` again (this can be configured differently!)
or when you call `wandb.finish()` which accepts two optional parameters:
* `exit_code: int`: use non-zero value to indicate a failure;
* `quiet: bool`: set to True to minimize log output.

You can also use `wandb.init` as a context manager:
```python
with wandb.init(project='my-project') as run:
    run.log({'loss': 23.45})
```


You can access the current run via `wandb.run`, so you don't need to pass the run object around your code if you want to
access it from different functions.

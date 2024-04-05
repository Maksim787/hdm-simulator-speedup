import wandb


class WandbLogger:
    def __init__(self, config: dict, enabled: bool, project_name: str, run_name: str):
        self.enabled = enabled
        self.project_name = project_name
        self.run_name = run_name
        if self.enabled:
            wandb.login()
            wandb.init(project=project_name, name=run_name, config=config)

    def log(self, d: dict):
        if self.enabled:
            wandb.log(d)

    def finish(self):
        if self.enabled:
            wandb.finish()


def delete_runs_with_name(project_name: str, run_name: str = "debug"):
    # Initialize wandb API
    api = wandb.Api()

    # Fetch all runs in the specified project
    runs = api.runs(project_name)
    print(f"Found {len(runs)}")

    for run in runs:
        # Check if the run name matches the one you want to delete
        if run.name == run_name:
            print(f"Deleting run: {run.name} (ID: {run.id})")
            run.delete()


def seed_everything(seed: int):
    import random, os
    import numpy as np
    import torch

    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = True

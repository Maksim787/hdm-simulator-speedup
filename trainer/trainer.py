import torch
from pprint import pprint
from copy import deepcopy
from tqdm.auto import trange
from torch import nn

from trainer.dataset import get_dataloaders
from trainer.utils import seed_everything, WandbLogger
from trainer.models import MLP


class Trainer:
    get_dataloaders_result = None
    optimizers = {
        "Adam": torch.optim.Adam,
        "SGD": torch.optim.SGD,
    }
    models = {
        "MLP": MLP,
    }
    schedulers = {
        "CosineAnnealingLR": torch.optim.lr_scheduler.CosineAnnealingLR
    }

    def __init__(self, config: dict):
        # Save config
        config = deepcopy(config)
        seed_everything(config["trainer"]["seed"])
        self.config = config

        # Create logger
        self.logger = WandbLogger(config=config, **config["wandb"])

        # Create dataloaders
        self.train_loader, self.test_loader, in_features, out_features = get_dataloaders(**config["dataloaders"])

        # Model
        self.device = torch.device(config["trainer"]["device"])

        model_type = config["model"].pop("type")
        self.model = self.models[model_type](in_features=in_features, out_features=out_features, **config["model"]).to(self.device)
        if config["trainer"]["verbose"]:
            pprint(config)
            print(f"model = {self.model}")

        # Optimizer
        optimizer_type = config["optimizer"].pop("type")
        self.optimizer = self.optimizers[optimizer_type](self.model.parameters(), **config["optimizer"])

        # Scheduler
        scheduler_type = config["scheduler"].pop("type")
        self.scheduler = self.schedulers[scheduler_type](self.optimizer, **config["scheduler"]) if scheduler_type is not None else None

        # Loss function
        self.loss_fn = nn.MSELoss()

        # Training
        self.n_epochs = config["trainer"]["n_epochs"]

    def train(self):
        for epoch in trange(1, self.n_epochs + 1):
            # Log lr
            lr = self.optimizer.param_groups[0]["lr"]
            # Train loop
            train_stats = self.train_loop(epoch)
            # Validation loop
            validation_stats = self.validation_loop(epoch)
            # Update lr
            if self.scheduler is not None:
                self.scheduler.step()
            # Log results
            stats = {
                "lr": lr,
                **train_stats,
                **validation_stats
            }
            self.logger.log(stats)
        self.logger.finish()

    def train_loop(self, epoch: int) -> dict:
        self.model.train()
        total_loss = 0
        for x, y_true in self.train_loader:
            self.optimizer.zero_grad()

            x, y_true = x.to(self.device), y_true.to(self.device)

            y_pred = self.model(x).squeeze()
            assert y_true.ndim == 1 and y_pred.ndim == 1

            loss = self.loss_fn(y_true, y_pred)
            loss.backward()

            self.optimizer.step()

            total_loss += loss.item() * len(y_true)
        return {"train_loss": total_loss / len(self.train_loader.dataset)}

    @torch.no_grad()
    def validation_loop(self, epoch: int) -> dict:
        self.model.eval()
        total_loss = 0
        for x, y_true in self.test_loader:
            x, y_true = x.to(self.device), y_true.to(self.device)

            y_pred = self.model(x).squeeze()
            assert y_true.ndim == 1 and y_pred.ndim == 1

            loss = self.loss_fn(y_true, y_pred)

            total_loss += loss.item() * len(y_true)
        return {"test_loss": total_loss / len(self.test_loader.dataset)}

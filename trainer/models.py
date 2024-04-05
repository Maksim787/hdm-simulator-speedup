import torch
from torch import nn


class MLP(nn.Module):
    activations = {
        "relu": nn.ReLU(),
        "sigmoid": nn.Sigmoid(),
        "tanh": nn.Tanh(),
    }

    def __init__(self, in_features: int, out_features: int, layer_sizes: list[int], activation: str, batchnorm: bool) -> None:
        super().__init__()
        assert len(layer_sizes) >= 1

        # encoder/decoder
        encoder = nn.Linear(in_features, layer_sizes[0])
        decoder = nn.Linear(layer_sizes[-1], out_features)

        # activation
        activation = self.activations[activation]

        # layers
        layers = []
        for i in range(len(layer_sizes)):
            layers.append(activation)
            if batchnorm:
                layers.append(nn.BatchNorm1d(layer_sizes[i]))
            if i + 1 < len(layer_sizes):
                layers.append(nn.Linear(layer_sizes[i], layer_sizes[i + 1]))
        self.net = nn.Sequential(
            encoder,
            *layers,
            decoder,
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

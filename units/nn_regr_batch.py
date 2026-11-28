import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import matplotlib.pyplot as plt
import argparse
import sys

# --- Command-line arguments ---
parser = argparse.ArgumentParser(description="Fit neural networks with minibatch SGD.")
parser.add_argument("--n", "-n", type=int, default=256, help="Training sample size")
parser.add_argument("--layer_size", "-l", type=int, default=64, help="Units per hidden layer")
parser.add_argument("--n_epochs", "-e", type=int, default=2000, help="Number of training epochs")
parser.add_argument("--batch_size", "-b", type=int, default=32, help="Minibatch size (use n for full-batch)")
parser.add_argument("--lr", "-r", type=float, default=1e-3, help="Adam learning rate")
parser.add_argument("--seed", "-s", type=int, default=1, help="Random seed/replicate")
args = parser.parse_args()

n = args.n
layer_size = args.layer_size
n_epochs = args.n_epochs
batch_size = args.batch_size
lr = args.lr
seed = args.seed

# --- Data generation (mirrors R gam example) ---
def fun(x):
    return x**2 + 2*x - 5


# --- Model definitions ---
class OneDenseLayer(nn.Module):
    def __init__(self, layer_size=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, layer_size),
            nn.ReLU(),
            nn.Linear(layer_size, 1),
        )

    def forward(self, x):
        return self.net(x)


class TwoDenseLayers(nn.Module):
    def __init__(self, layer_size=256):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(1, layer_size),
            nn.ReLU(),
            nn.Linear(layer_size, layer_size),
            nn.ReLU(),
            nn.Linear(layer_size, 1),
        )

    def forward(self, x):
        return self.net(x)


# --- Training helper (minibatch SGD) ---
def train(model, X_train, y_train, X_test, y_test, n_epochs=2000, lr=1e-3, batch_size=32):
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()
    dataset = TensorDataset(X_train, y_train)
    loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    train_losses, test_losses, weight_norms = [], [], []
    for epoch in range(n_epochs):
        model.train()
        for X_batch, y_batch in loader:
            optimizer.zero_grad()
            loss = loss_fn(model(X_batch), y_batch)
            loss.backward()
            optimizer.step()
        if (epoch + 1) % 100 == 0:
            with torch.no_grad():
                model.eval()
                train_loss = loss_fn(model(X_train), y_train).item()
                test_loss = loss_fn(model(X_test), y_test).item()
                norm = sum(p.norm().item() ** 2 for p in model.parameters()) ** 0.5
            train_losses.append(train_loss)
            test_losses.append(test_loss)
            weight_norms.append(norm)
            if (epoch + 1) % 500 == 0:
                print(f"  epoch {epoch+1:5d}  train={train_loss:.4f}  test={test_loss:.4f}  |w|={norm:.2f}")
    return train_losses, test_losses, weight_norms

# --- Minibatch size (try 8, 32, 64, 256 = full batch) ---
# (set via --batch_size)

np.random.seed(seed)
x = np.linspace(-2, 2, n)
y = fun(x) + np.random.randn(n)

X_tensor = torch.tensor(x, dtype=torch.float32).unsqueeze(1)
y_tensor = torch.tensor(y, dtype=torch.float32).unsqueeze(1)

# --- Test data (independent draw, n_test = n // 2) ---
n_test = n // 2
x_test = np.linspace(-2, 2, n_test)
y_test = fun(x_test) + np.random.randn(n_test)

X_test_tensor = torch.tensor(x_test, dtype=torch.float32).unsqueeze(1)
y_test_tensor = torch.tensor(y_test, dtype=torch.float32).unsqueeze(1)

# --- True loss: noise variance (sigma^2 = 1) ---
true_loss = 1.0

# --- Oracle loss: MSE of true function on training data ---
_y_true_train = torch.tensor(fun(x), dtype=torch.float32).unsqueeze(1)
oracle_loss = nn.MSELoss()(_y_true_train, y_tensor).item()
print(f"Oracle loss (fun(x) vs y): {oracle_loss:.4f}")

# --- Fit grid for smooth prediction curve ---
x_grid = np.linspace(-2, 2, 500)
X_grid = torch.tensor(x_grid, dtype=torch.float32).unsqueeze(1)
y_true_grid = fun(x_grid)


def fit_and_plot(layer_size, n_epochs, batch_size, lr, seed):
    print(f"\n=== layer_size={layer_size}, n_epochs={n_epochs}, batch_size={batch_size}, lr={lr} ===")

    print("Training 1-layer network ...")
    model1 = OneDenseLayer(layer_size)
    train_losses1, test_losses1, weight_norms1 = train(
        model1, X_tensor, y_tensor, X_test_tensor, y_test_tensor,
        n_epochs=n_epochs, batch_size=batch_size, lr=lr,
    )
    model1.eval()
    with torch.no_grad():
        y_pred1 = model1(X_grid).squeeze().numpy()

    print("Training 2-layer network ...")
    model2 = TwoDenseLayers(layer_size)
    train_losses2, test_losses2, weight_norms2 = train(
        model2, X_tensor, y_tensor, X_test_tensor, y_test_tensor,
        n_epochs=n_epochs, batch_size=batch_size, lr=lr,
    )
    model2.eval()
    with torch.no_grad():
        y_pred2 = model2(X_grid).squeeze().numpy()

    record_every = 100
    epochs = np.arange(record_every, n_epochs + 1, record_every)
    titles = [f"1 Layer", f"2 Layers"]

    fig, axes = plt.subplots(3, 2, figsize=(12, 15))
    fig.suptitle(f"layer_size={layer_size}, n_epochs={n_epochs}, batch_size={batch_size}, lr={lr}",
                 y = .99)

    # Top row: scatter + fit
    for ax, y_pred, title in zip(axes[0], [y_pred1, y_pred2], titles):
        ax.scatter(x, y, s=15, alpha=0.5, label="Train data")
        ax.plot(x_grid, y_true_grid, color="gray", linestyle="--", label="True function")
        ax.plot(x_grid, y_pred, color="red", linewidth=2, label="NN fit")
        ax.set_title(title)
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

    # Bottom row: train/test loss over epochs
    for ax, trl, tel, title in zip(
        axes[1],
        [train_losses1, train_losses2],
        [test_losses1, test_losses2],
        titles,
    ):
        ax.plot(epochs, trl, label="Train loss")
        ax.plot(epochs, tel, label=f"Test loss (n={n_test})")
        ax.axhline(true_loss, color="black", linestyle="--", label="True loss (1.0)")
        ax.axhline(oracle_loss, color="green", linestyle="--", label=f"Oracle loss ({oracle_loss:.2f})")
        ax.set_title(f"{title} — loss over epochs")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("MSE loss")
        ax.set_ylim(0, 3)
        ax.legend()

    # Third row: weight norm over epochs
    max_norm = max(max(weight_norms1), max(weight_norms2))
    for ax, wn, title in zip(
        axes[2],
        [weight_norms1, weight_norms2],
        titles,
    ):
        ax.plot(epochs, wn)
        ax.set_title(f"{title} — weight norm over epochs")
        ax.set_xlabel("Epoch")
        ax.set_ylabel("L2 weight norm")
        ax.set_ylim(0, max_norm)

    plt.tight_layout()
    fname = f"nn_regr_batch_n{n}_{layer_size}_{n_epochs}_{batch_size}_lr{lr}_seed{seed}.png"
    plt.savefig(fname, dpi=150)
    print(f"  Plot saved to {fname}")
    if sys.flags.interactive:
        plt.show()

fit_and_plot(layer_size, n_epochs, batch_size, lr, seed)

import numpy
import jax
import jax.numpy as jnp

from typing import Callable
from torch.utils.data import DataLoader


def one_hot(x: numpy.ndarray, k: int, dtype=jnp.float32):
    x_one_hot = jnp.array(x[:, None] == jnp.arange(k), dtype)
    return x_one_hot


def comp_loss_accuracy(
    model: callable,
    params: list[tuple[jax.Array]],
    loss: Callable,
    data_generator: DataLoader,
) -> tuple[float, float]:
    """Computes loss and accuray for provided model and data."""

    num_targets = len(data_generator.dataset.classes)

    running_loss = 0.0
    running_accuracy = 0.0
    running_counter = 0.0

    for images, targets in data_generator:
        targets = one_hot(x=targets, k=num_targets)

        images = jnp.atleast_2d(images)
        targets = jnp.atleast_2d(targets)

        preds = model(params, images)

        # Compute accuracy
        target_class = jnp.argmax(targets, axis=1)
        predicted_class = jnp.argmax(preds, axis=1)
        batch_accuracy = float(jnp.sum(target_class == predicted_class))

        # Compute loss
        batch_loss = loss(targets, preds)

        # Accumulating stats
        running_loss += batch_loss
        running_accuracy += batch_accuracy
        running_counter += len(images)

    total_loss = running_loss / running_counter
    total_accuracy = running_accuracy / running_counter

    return float(total_loss), float(total_accuracy)

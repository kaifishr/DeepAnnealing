import jax
import jax.numpy as jnp

from src.custom_types import Params


def init_params(key: jax.Array, dims: list[int]) -> Params:
    keys = jax.random.split(key=key, num=len(dims))
    return [
        _init_params(fan_in=fan_in, fan_out=fan_out, key=key)
        for fan_in, fan_out, key in zip(dims[:-1], dims[1:], keys)
    ]


def _init_params(
    fan_in: int, fan_out: int, key: jax.Array
) -> tuple[jax.Array, jax.Array]:
    w_key, _ = jax.random.split(key)
    scale = jnp.sqrt(2.0 / fan_in)
    w = scale * jax.random.normal(w_key, (fan_out, fan_in))
    b = jnp.zeros(shape=(fan_out,))
    return w, b


def forward(params: jax.Array, inputs: jax.Array) -> jax.Array:
    out = jax.lax.stop_gradient(inputs)
    *layers, last = params

    for w, b in layers:
        out = jnp.dot(w, out) + b
        out = jax.nn.tanh(out)
        # out = jax.nn.relu(out)
        # out = jnp.heaviside(out, 0.0)
        # out = jnp.sign(out)

    w, b = last
    logits = jnp.dot(w, out) + b
    return logits


model = jax.jit(jax.vmap(forward, in_axes=(None, 0)))

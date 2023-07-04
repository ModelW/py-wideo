# Installation

## Add `wideo` to your dependencies

With Poetry, run:

```shell
poetry add wideo
```

With pip, add:

```
wideo==<version>
```

To your `requirements.txt`.

## Use `wideo`

Simply add `wideo` to your installed apps in your Django settings:

```python
INSTALLED_APPS = [
    "[...]",  # Django & Wagtail
    "wideo",
    "[...]",  # Your own apps
]
```

## Set up encoding and cleanup tasks

See the full documentation [here](tasks).

## Optional: use custom presets

See the full documentation [here](custom-presets).

## Optional: use custom models

See the full documentation [here](custom-models).

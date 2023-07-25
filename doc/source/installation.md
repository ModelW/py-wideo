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

## Use the `wideo` app

Simply add `wideo` to your installed apps in your Django settings:

```python
INSTALLED_APPS = [
    "[...]",  # Django & Wagtail
    "wideo",
    "[...]",  # Your own apps
]
```

## Basic configuration

### `WIDEO_WORKING_DIR` (mandatory)

Video files can get very large, and thus are not kept in memory. This setting
should point to an empty directory that can be used by Wideo to do write and
read temporary files.

Choose carefully what directory to use! On Linux for example, it might seem
tempting to use something along the lines of `/tmp/wideo`. However, `/tmp` is
often mounted as `tmpfs`, which is a virtual filesystem that can actually reside
in-memory instead of being kept on disk. Therefore, anything under

### `WIDEO_CHUNK_SIZE` (optional)

Since, once again, video files can have an unwieldy size, it is necessary to cut
them down to small pieces in order to upload them. `WIDEO_CHUNK_SIZE` allows you
to choose exactly what size each chunk of the video files will be (5M by
default).

### `WIDEO_PARALLEL_WORK` (optional)

If you have enough memory and processing power, parallel processing of files can
be enabled by setting this variable to `True`. Videos will then be encoded
according to every enabled preset at the same time. If set to `False` or unset,
Videos will be encoded following each preset sequentially.

Note that ffmpeg can consume a very large amount of memory, which is why this
setting is disabled by default.

## Set up encoding and cleanup tasks

See the full documentation [here](tasks).

## Optional: use custom presets

See the full documentation [here](custom-presets).

## Optional: use custom models

See the full documentation [here](custom-models).

# Custom models

This package follows in the footsteps or the official `wagtailimages` module.
As such, one aspect that is replicated in this package is the ability to use
your own custom models in place of the default provided ones.

The different sections of this document describe the steps to use custom models.

## What each model is used for

I lied. Before customization, it's necessary to first explain what models are at
play and why.

### `UploadedVideo`

This model represents a raw, unencoded video that a user uploaded using the
Wagtail admin interface. It notably has a `FileField` pointing to the uploaded
file itself.

This model cannot (and doesn't need to) be overridden.

### `Video`

This is the model visible in the Wagtail admin. It has a reference to an
`UploadedVideo`, but has additional attributes such as a title, tags among
other things.

It inherits from `AbstractVideo`.

### `Render`

Like `UploadedVideo`, this model holds a `FileField`; however this one
references a video file that has been automatically encoded and stored by Wideo
and not uploaded by the user.

The default model also has a foreign key to a `Video` model, to keep track of
which user-uploaded video this final render is coming from.

It inherits from `AbstractRender`.

## Writing the models

You have to inherit from `AbstractVideo` and `AbstractRender`.

### `AbstractVideo`

This one is simple: just inherit from it, add your custom fields, and you're
done.

```python
from wideo.models import AbstractVideo

class CustomVideo(AbstractVideo):
    pass
```

### `AbstractRender`

When inheriting from `AbstractRender`, a `video` field has to be specified. It
must be a foreign key to a model inheriting from `AbstractVideo` (most likely,
you will have created one some minutes ago). The `on_delete` property of this
field should be set to `models.CASCADE`, as it is typically not very useful to
keep renders of videos that have been deleted.

In addition, it should be marked as a snippet in order to allow choosing videos
in the admin interface.

```python
from django.db import models
from wagtail.snippets.models import register_snippet
from wideo.models import AbstractRender

@register_snippet
class CustomRender(AbstractRender):
    video = models.ForeignKey(to=CustomVideo, on_delete=models.CASCADE)
```

## Updating the Django settings

Now that you have created custom models, Wideo will need to know about them.
This is done using the `WIDEO_VIDEO_MODEL` and `WIDEO_RENDER_MODEL` variables.
Set them to your custom video and custom render models respectively, with their
fully qualified name, just like your would set `WAGTAILIMAGES_IMAGE_MODEL`:

```python
WIDEO_VIDEO_MODEL = "my_awesome_app.models.AwesomeVideo"

WIDEO_RENDER_MODEL = "my_awesome_app.models.AwesomeRender"
```

## Referring to the video and render models

Again, just like `wagtailimages`, utility functions are provided to retrieve
custom models:
- `wideo.get_video_model()`
- `wideo.get_video_model_string()`
- `wideo.get_render_model()`
- `wideo.get_render_model_string()`

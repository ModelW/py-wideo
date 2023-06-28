# Installation

In order to install Wideo, you need to:
1. Add the `wideo` dependency to your `requirements.txt` or `poetry.toml` (and ensure `wagtail` and `celery` are also part of your dependencies)
2. Add `wideo` to `INSTALLED_APPS` in your Django settings
3. Optional: set `WIDEO_VIDEO_MODEL` and `WIDEO_RENDER_MODEL` to your own custom models
4. Optional: add `wideo.tasks.delete_orphan_uploaded_videos` in your `CELERY_BEAT_SCHEDULE` in order to clean up unused uploads

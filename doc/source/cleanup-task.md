# Cleanup task

In some cases, video files can be uploaded, but unused. For example, if a user
starts creating a new video model in the Wagtail admin, and uploads multiple
files before saving, only the last one will be used in the video model, while
all the previous ones will simply clutter the database and object
storage/filesystem.

In order to circumvent this issue, a Celery task is provided and ready to be
used with Celery Beat to regularly clean up all those unused files.

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    # Clean up uploads once a day
    "wideo.tasks.delete_orphan_uploaded_videos": {
        "task": "wideo.tasks.delete_orphan_uploaded_videos",
        "schedule": crontab(minute="0", hour="0"),
    },
}
```

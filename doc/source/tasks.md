# Tasks

Wideo makes use of some asynchronous tasks. They can be executed in two ways:

- Celery tasks (preferred)
- Cron jobs

## Video encoding

All videos uploaded by users should be encoded; this is one if the major points
of using Wideo after all.

### Celery tasks

If Celery is set up, these tasks will be started automatically. Internally, the
value of `CELERY_BROKER_URL` is checked; if it is not empty, the project is
considered to be using Celery and Wideo will try to launch Celery tasks to
encode videos.

### Cron jobs

If you are not using Celery, you can manually set up cron jobs to start the
following command:

```shell
python manage.py encode_videos
```

This will encode all videos that have not yet been encoded.

## Cleanup of orphan video uploads

In some cases, video files can be uploaded, but unused. For example, if a user
starts creating a new video model in the Wagtail admin, and uploads multiple
files before saving, only the last one will be used in the video model, while
all the previous ones will simply clutter the database and object
storage/filesystem.

### Celery tasks

A Celery task is provided and ready to be used with Celery Beat.

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

### Cron jobs

If you are not using Celery, you can manually set up cron jobs to start the
following command:

```shell
python manage.py delete_orphan_uploaded_videos
```

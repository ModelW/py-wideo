# Custom presets

## Default presets

By default, `wideo` will encode your videos according to the following presets:

| Preset name | Resolution | Format |
|-------------|------------|--------|
| 720P_H264   | 720p       | H264   |
| 1080P_H264  | 1080p      | H264   |
| 4K_H264     | 4k         | H264   |
| 720P_AV1    | 720p       | AV1    |
| 1080P_AV1   | 1080p      | AV1    |
| 4K_AV1      | 4k         | AV1    |

## Customization

You can customize the presets in you Django settings like so:

```python
# Here, we want only 4k videos, and we also want to customize the AV1 encoding
# to use the 'veryfast' ffmpeg preset to reduce encoding time.
# At the same time, the default 4K_H264 preset is used without any change by
# just specifying its name instead of a dict.
WIDEO_PRESETS = {
    "4K_H264": "4K_H264",
    "4K_AV1": {
        "ffmpeg_flags": [
            "-vf",
            f"\"scale='min(3840,iw)':min'(3840,ih)':force_original_aspect_ratio=decrease\"",
            "-preset",
            "veryfast",
        ],
        "extension": "webm",
    },
}
```

Customizing the presets can be a useful tool, however it means having to
manually specify the exact flags that will be passed to ffmpeg.
Wideo will try to keep sensible default presets so that in most cases, you won't
have to do this.

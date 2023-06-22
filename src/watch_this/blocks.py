from wagtail.blocks import BooleanBlock, StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class VideoBlock(StructBlock):
    video = SnippetChooserBlock(target_model="watch_this.video")
    autoplay = BooleanBlock(required=False)
    controls = BooleanBlock(required=False)

    class Meta:
        label = "Video"
        template = "watch_this/blocks/video.html"

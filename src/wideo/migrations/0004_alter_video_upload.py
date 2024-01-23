# Generated by Django 4.1.9 on 2024-01-23 12:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("wideo", "0003_uploadedvideochunk"),
    ]

    operations = [
        migrations.AlterField(
            model_name="video",
            name="upload",
            field=models.ForeignKey(
                help_text="The uploaded video file; its resolution should be a standard one to avoid issues",
                on_delete=django.db.models.deletion.PROTECT,
                to="wideo.uploadedvideo",
                verbose_name="file",
            ),
        ),
    ]

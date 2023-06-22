# Generated by Django 4.1.9 on 2023-06-21 13:09

import django.db.models.deletion
import watch_this.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("watch_this", "0001_initial"),
        ("cms", "0002_homepage"),
    ]

    operations = [
        migrations.AddField(
            model_name="homepage",
            name="video",
            field=watch_this.fields.VideoField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="watch_this.video",
            ),
        ),
    ]
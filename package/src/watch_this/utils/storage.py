import os
from uuid import UUID

from django.utils.text import slugify


def upload_to(instance, filename):
    """
    We want to make sure to upload the file to a place that isn't going to be
    problematic.

    - In order to limit the number of files in a single directory, we use the
      ID of the instance (which is a UUID4) in order to create a structure of
      directories (because most storage solutions have limits on the amount
      of files per folder).
    - The file name should be slugified (using Django's function) to make sure
      there is no problem with special characters.
    - The extension is also going to be normalized and common synonyms are
      going to be replaced by the most common one (like m4v -> mp4).

    Parameters
    ----------
    instance
        An instance that has a UUID for its pk field
    filename
        Name of the file we're uploading
    """

    file_root, file_ext = os.path.splitext(filename)
    file_ext = file_ext.lower()

    ext_map = {
        ".m4v": ".mp4",
    }

    file_ext = ext_map.get(file_ext, file_ext)
    slugified_name = slugify(file_root)

    instance_uuid = instance.pk
    assert isinstance(instance_uuid, UUID), "The instance's primary key must be a UUID"

    uuid_str = str(instance_uuid)
    dir_structure = os.path.join(uuid_str[:2], uuid_str[2:4], uuid_str[4:6])

    new_filename = f"{slugified_name}{file_ext}"
    return os.path.join(dir_structure, new_filename)

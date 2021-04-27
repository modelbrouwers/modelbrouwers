import os
import shutil

from django.core.exceptions import ImproperlyConfigured

from sorl.thumbnail import delete as thumb_delete

try:  # PIL
    import Image
except ImportError:  # Pillow 2.3.0
    from PIL import Image


ORIGINALS_FOLDER_NAME = "originals"


def rotate_img(image_field, degrees=90):
    """
    Util function to rotate the uploaded image.

    The original image is first copied to a folder containing all originals
    within an album, if it doesn't exist yet. The image in the album folder is
    then transformed and overwritten with PIL.
    """
    copy_original_photo(image_field.path)

    # update the KV store
    thumb_delete(image_field, delete_file=False)

    img = Image.open(image_field.path)
    new_size = (img.size[1], img.size[0])
    img = img.rotate(degrees, expand=True)
    img = img.resize(new_size)
    img.save(image_field.path)


def get_or_create_originals_folder(album_folder):
    originals_folder = os.path.join(album_folder, ORIGINALS_FOLDER_NAME)
    if not os.path.exists(originals_folder):
        try:
            os.makedirs(originals_folder)
        except OSError as err:
            raise ImproperlyConfigured(
                "Could not create directory: %s (%s)" % (originals_folder, err)
            )
    return originals_folder


def copy_original_photo(image_path):
    album_folder, filename = os.path.split(image_path)
    originals_folder = get_or_create_originals_folder(album_folder)
    destination = os.path.join(originals_folder, filename)
    if not os.path.exists(destination):
        shutil.copyfile(image_path, destination)
    return None

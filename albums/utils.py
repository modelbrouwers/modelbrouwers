import Image
import os
import itertools
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from models import Preferences
import unicodedata

def valid_ext(extension):
    """
    Validates if a file is in a given set of valid types.
    """
    if extension.lower() in settings.VALID_IMG_EXTENSIONS:
        return True
    return False

def exists(name):
    return os.path.exists(name)

def get_available_name(name, overwrite=False):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        file_root = file_root.replace('/', '-') #avoid / in filenames
        # If the filename already exists, add an underscore and a number (before
        # the file extension, if one exists) to the filename until the generated
        # filename doesn't exist.
        count = itertools.count(1)
        while exists(name) and not overwrite:
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s_%s%s" % (file_root, count.next(), file_ext))
        return name, dir_name

def save_to_path(img, upload_to, prefix, filename, ext, overwrite=False):
    fn = "%s%s" % (filename, ext)
    outfile = os.path.join(settings.MEDIA_ROOT, upload_to, prefix, fn)
    outfile, path_dir = get_available_name(outfile, overwrite=overwrite)
    
    #get the relative path for the database
    rel_path = outfile.replace(settings.MEDIA_ROOT, '', 1)[1:] # strip slash
    rel_folder = path_dir + '/'
    #if relative path doesn't exist, create it
    if not os.path.exists(rel_folder):
        try:
            os.makedirs(rel_folder)
        except OSError, err:
            raise ImproperlyConfigured('Could not create directory: %s (%s)' % (rel_folder, err))
    #Make sure folder is writable
    if not os.access(rel_folder, os.W_OK):
        raise ImproperlyConfigured('Could not write to directory: %s' % rel_folder)
    img.save(outfile.encode('utf-8'))
    return (rel_path, img)

def resize(image, sizes_data=[(1024, 1024, '1024_'), (800, 800, '')], thumb_dimensions=settings.THUMB_DIMENSIONS, upload_to='albums/', overwrite=False):
    """
    Resizes an image to multiple sizes and saves it to disk.
    
    :param image        : Django UploadedFile(can be in memory or temporary file)
    :param sizes_data   : a list of 3-tupples (max_width, max_height, prefix)
    :param upload_to    : path relative to settings.MEDIA_ROOT where the file will be stored
    :returns            : list with tupples (relative path, width, height) of the image,
                          or None if the file is invalid.
    """
    img = Image.open(image)
    width, height = float(img.size[0]), float(img.size[1]) #original sizes
    f = os.path.split(image.name)[1]
    filename, ext = os.path.splitext(f)
    
    if valid_ext(ext):
        img_data = [] # to return -> gets saved in db
        sizes_data.append(thumb_dimensions)
        for size in sizes_data:
            max_width = size[0]
            max_height = size[1]
            prefix = size[2]
            
            ratio = min(max_width/width, max_height/height)
            if ratio < 1.0: #resizing required
                size = (int(round(ratio * width)), int(round(ratio * height)))
                img = img.resize(size, Image.ANTIALIAS) #resized image
            rel_path, img = save_to_path(img, upload_to, prefix, filename, ext.lower(), overwrite=overwrite)
            if not prefix == thumb_dimensions[2]: #don't save the thumb in the database
                img_data.append((rel_path, img.size[0], img.size[1]))
        return img_data
    return None

def admin_mode(user, preferences=None):
    if preferences:
        p = preferences
    else:
        p = Preferences.get_or_create(user)
    if (user.has_perm('albums.see_all_albums') or user.has_perm('albums.edit_album')) and p.apply_admin_permissions:
        return True
    return False

def can_switch_admin_mode(user):
    if user.has_perm('albums.see_all_albums') or user.has_perm('albums.edit_album') or user.is_superuser:
        return True
    return False

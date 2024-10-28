import os
from PIL import Image
from django.db.models.fields.files import ImageField, ImageFieldFile

def resize_gif(path, thumb_width, thumb_height, save_as=None):
    """
    Resizes the GIF to a given size.
    """
    parts = path.split('.')
    parts[-2] = parts[-2] + '_thumb'
    save_as = '.'.join(parts)
    
    if path.split('.')[-1].lower() != 'gif':
        raise ValueError("It's not a GIF file.")
    
    all_frames = extract_and_resize_frames(path, thumb_width, thumb_height)

    if len(all_frames) == 1:
        all_frames[0].save(save_as, optimize=True)
    else:
        all_frames[0].save(save_as, optimize=True, save_all=True, append_images=all_frames[1:], loop=1000)

def analyse_image(path):
    """
    Pre-process pass over the image to determine the mode (full or additive).
    Necessary as assessing single frames isn't reliable. Need to know the mode before processing all frames.
    """
    im = Image.open(path)
    results = {'size': im.size, 'mode': 'full'}
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results

def extract_and_resize_frames(path, thumb_width, thumb_height):
    """
    Iterate the GIF, extracting each frame and resizing them.

    Returns:
        An array of all frames.
    """
    mode = analyse_image(path)['mode']
    im = Image.open(path)
    thumb_size = (thumb_width, thumb_height)
    all_frames = []
    p = im.getpalette()
    last_frame = im.convert('RGBA')

    try:
        while True:
            if im.mode == 'P' and not im.getpalette():
                im.putpalette(p)

            new_frame = Image.new('RGBA', im.size)

            if mode == 'partial':
                new_frame.paste(last_frame)

            new_frame.paste(im, (0, 0), im.convert('RGBA'))
            new_frame.thumbnail(thumb_size, Image.LANCZOS)
            background = Image.new('RGBA', thumb_size, (0, 0, 0))
            box = (int((thumb_size[0] - new_frame.size[0]) / 2), int((thumb_size[1] - new_frame.size[1]) / 2))
            background.paste(new_frame, box)
            all_frames.append(background)

            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    return all_frames

class ThumbnailGifFieldFile(ImageFieldFile):
    def _add_thumb(self, s):
        parts = s.split('.')
        parts[-2] = parts[-2] + '_thumb'
        if parts[-1].lower() != 'gif':
            raise ValueError("It's not a GIF file.")
        return '.'.join(parts)

    @property
    def thumb_path(self):
        return self._add_thumb(self.path)

    @property
    def thumb_url(self):
        return self._add_thumb(self.url)

    def save(self, name, content, save=True):
        super().save(name, content, save)
        resize_gif(self.path, self.field.thumb_width, self.field.thumb_height, self.thumb_path)

    def delete(self, save=True):
        if os.path.exists(self.thumb_path):
            os.remove(self.thumb_path)
        super().delete(save)

class ThumbnailGifField(ImageField):
    attr_class = ThumbnailGifFieldFile

    def __init__(self, verbose_name=None, thumb_width=128, thumb_height=128, **kwargs):
        self.thumb_width, self.thumb_height = thumb_width, thumb_height
        super().__init__(verbose_name, **kwargs)

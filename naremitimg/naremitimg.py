from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
from PIL import ImageOps

from StringIO import StringIO
import hashlib
import pickle
import os
import urllib2

from django.conf import settings
from django.http import HttpResponse

# attempt to import requests
try:
    import requests
    has_requests = True
except:
    has_requests = False

class NaremitIMG:
    format = 'JPEG'
    functions = []
    cache = 0

    def __init__(self, params):
        self.params = params

        # extract cache value
        if 'cache' in self.params:
            try:
                self.cache = int(self.params['cache']) > 0
            except:
                pass

        # load image
        if 'file' in self.params:
            self.load_from_file()
        elif 'uri' in self.params:
            self.load_from_uri()
        else:
            raise Exception('No source image defined')

        # extract mimetype
        self.format = self.im.format
        self.size = self.im.size
        if 'format' in self.params:
            self.format = self.params['format'].upper()

        # process functions
        if 'p' in self.params:
            p = self.params['p'].strip('|').strip()
            if len(p) > 0:
                self.functions = p.split('|')
                for p in self.functions:
                    args = p.split(',')
                    command = args.pop(0)
                    self.im = self.process(command, args)

    def download(self, url):
        if has_requests:
            r = requests.get(url)
            return r.content
        else:
            r = urllib2.urlopen(url)
            return f.read()

    def process(self, command, args):
        # autocontrast
        if command == 'autocontrast':
            return ImageOps.autocontrast(self.im)

        # blur
        if command == 'blur':
            return self.im.filter(ImageFilter.BLUR)

        # brightness
        if command == 'brightness':
            try:
                return ImageEnhance.Brightness(self.im).enhance(float(args[0]))
            except:
                raise Exception('Invalid brightness argument')

        # color
        if command == 'color':
            try:
                return ImageEnhance.Color(self.im).enhance(float(args[0]))
            except:
                raise Exception('Invalid color argument')

        # colorize
        if command == 'colorize':
            try:
                return ImageOps.colorize(
                    ImageOps.grayscale(self.im),
                    black='%s' % args[0],
                    white='%s' % args[1]
                )
            except:
                raise Exception('Invalid colorize arguments')

        # contour
        if command == 'contour':
            return self.im.filter(ImageFilter.CONTOUR)

        # contrast
        if command == 'contrast':
            try:
                return ImageEnhance.Contrast(self.im).enhance(float(args[0]))
            except:
                raise Exception('Invalid contrast argument')

        # crop
        if command == 'crop':
            try:
                return self.im.crop(tuple([int(a) for a in args]))
            except:
                raise Exception('Invalid crop arguments')

        # cropratio
        if command == 'cropratio':
            try:
                # get sizes
                width = float(self.im.size[0])
                height = float(self.im.size[1])
                orig_ratio = width / height
                target_ratio = float(args[0])

                # crop
                if orig_ratio > target_ratio:
                    # same height, change width
                    target_width = int(round(height * target_ratio))
                    left = int(round((width / 2) - (target_width / 2)))
                    return self.im.crop((
                        left,
                        0,
                        left + target_width,
                        int(height),
                    ))
                elif target_ratio > orig_ratio:
                    # same width, change height
                    target_height = int(round(width / target_ratio))
                    top = int(round((height / 2) - (target_height / 2)))
                    return self.im.crop((
                        0,
                        top,
                        int(width),
                        top + target_height
                    ))
                else:
                    return self.im

            except:
                raise Exception('Invalid cropratio arguments')

        # emboss
        if command == 'emboss':
            return self.im.filter(ImageFilter.EMBOSS)

        # equalize
        if command == 'equalize':
            return ImageOps.equalize(self.im)

        # fliphoriz
        if command == 'fliphoriz':
            return self.im.transpose(Image.FLIP_LEFT_RIGHT)

        # flipvert
        if command == 'flipvert':
            return self.im.transpose(Image.FLIP_TOP_BOTTOM)

        # gblur
        if command == 'gblur':
            try:
                return self.im.filter(ImageFilter.GaussianBlur(radius=int(args[0])))
            except:
                raise Exception('Invalid gblur argument')

        # grayscale
        if command == 'grayscale':
            return ImageOps.grayscale(self.im)

        # invert
        if command == 'invert':
            return ImageOps.invert(self.im)

        # posterize
        if command == 'posterize':
            try:
                return ImageOps.posterize(self.im, int(args[0]))
            except:
                raise Exception('Invalid posterize argument')

        # resize
        if command == 'resize':
            try:
                return self.im.resize(
                    tuple([int(a) for a in args]),
                    resample=Image.ANTIALIAS
                )
            except:
                raise Exception('Invalid resize arguments')

        # resizepc
        if command == 'resizepc':
            try:
                x, y = self.im.size
                return self.im.resize(
                    (int(x * float(args[0])), int(y * float(args[1]))),
                    resample=Image.ANTIALIAS
                )
            except:
                raise Exception('Invalid resize arguments')

        # rotate
        if command == 'rotate':
            try:
                return self.im.rotate(int(args[0]))
            except:
                raise Exception('Invalid rotate argument')

        # sharpness
        if command == 'sharpness':
            try:
                return ImageEnhance.Sharpness(self.im).enhance(float(args[0]))
            except:
                raise Exception('Invalid sharpness argument')

        # solarize
        if command == 'solarize':
            try:
                return ImageOps.solarize(self.im, int(args[0]))
            except:
                raise Exception('Invalid solarize argument')

        # fallback
        raise Exception('Invalid function name "%s"' % command)

    def load_from_file(self):
        try:
            self.im = Image.open(self.params['file'])
        except:
            raise Exception('Image not found or of invalid format')

    def load_from_uri(self):
        save_local_copy = False
        tmp_folder = getattr(settings, 'NAREMITIMG_TMP_FOLDER', '/tmp/')

        # construct remote image url
        url = self.params['uri']
        if 'domain' in self.params:
            domain = self.params['domain']
            try:
                url = '%s%s' % (settings.NAREMITIMG[domain], url)
            except:
                raise Exception('Domain "%s" not found in config' % domain)

        if self.cache:
            tmp_file = '%snaremitimg_%s' % (tmp_folder, hashlib.sha224(url).hexdigest())
            if not os.path.isfile(tmp_file):
                with open(tmp_file, 'wb') as f:
                    f.write(self.download(url))
            self.im = Image.open(tmp_file)
            return

        # load image
        try:
            content = self.download(url)
            self.im = Image.open(StringIO(content))
        except:
            raise Exception('Image not found or of invalid format')

    def response(self):
        r = HttpResponse(content_type='image/%s' % self.format.lower())
        try:
            saved = False
            if 'optimize' in self.params:
                try:
                    self.im.save(r, self.format, optimize=1)
                    saved = True
                except:
                    pass
            if not saved:
                self.im.save(r, self.format)
        except:
            raise Exception('Invalid image format defined')
        return r
NaremitIMG
==========

NaremitIMG is tiny Django app which enables dynamic image manipulation on the fly. This could be used, for example, in conjunction with an online image editing tool, or to create thumbnails or to serve responsive images via a CDN. This project is deliberately simple. 

Example usage:

    mywebsite.com/path/to/naremitimg?uri=http://mywebsite.com/images/frog.jpg&p=cropratio,1|resize,100,100|grayscale

The code takes a _source image_ from a URL or a location on the webserver's filesystem, manipulates as per your instructions, then returns the _output image_. 

Installation
------------
The following assumes you have Django and either the Pillow (recommended) or PIL (not so much) imaging libraries installed and working.

Because the Pillow installation process can vary between different webserver environments, NaremitIMG does not attempt to create a dependency. Instead please just know that it won't work without one of these packages installed. See [Pillow installation documentation](http://pillow.readthedocs.org/en/latest/installation.html).

Once this is done:

 1. Get the code:<br />`pip install django-naremitimg`<br /><br />
 2. Add `'naremitimg'` to your `INSTALLED_APPS` in your Django project's `settings.py` file<br /><br />
 3. Add an entry to your `urls.py` file as follows:<br />`url(r'^path/to/naremitimg$', 'naremitimg.views.img')`

There are some optional settings which can be applied (see the "domain" section below). Be sure your Django project has an [appropriate cache settings](https://docs.djangoproject.com/en/dev/topics/cache/) if you wish to take advantage of the caching functionality.

Quickstart
----------
Once installation is complete, open a web browser and point it to (obviously substitute the path for the machine you are testing this on):
`http://localhost/path/to/naremitimg?uri=http://naremit.com/naremit.gif`

Assuming you have a working web connection and everything in installed correctly, you should see our "N" logo in your browser window. Not very exciting, but if you've got this far, it is all working. Excellent.

Parameters
----------
All parameters are passed in via GET request in the querystring. These are:

#### Defining the source image:
(At least one of `uri` or `path` must be present)

 - `uri`: (optional) The web address of the _source image_.<br /><br />
 - `domain`: (optional) The domain from which to retrieve the _source image_. See the "domain" section below.<br /><br />
 - `file`: (optional) The filesystem path of the _source image_, e.g. `file=/var/www/images/dog.gif`.<br /><br />_By using the `file` method you do expose this path in your webserver's file structure to the outside world. If you server is secured appropriately this shouldn't be a problem but do consider this carefully on public facing systems. A chat with your friendly SysAdmin or InfoSec guy/gal is probably a good idea if you aren't 100% sure._

#### Image Manipulation:

 - `format`: (optional) Define the filetype you wish NaremitIMG to output, e.g. 'JPEG', 'PNG', etc. If not specified, the _output image_ format will match that of the _source image_.<br /><br />
 - `p`: (optional, but silly to leave out) The processing (or manipulations) you would like to perform on the image. See "Image Processing" below.

#### Other:

 - `cache`: (optional) The length of time (in seconds) the _source image_ should be held in the Django cache for. This is useful if you are making a series of modifications to the same image, i.e. an online image manipulation tool for example.

Image Processing
----------------
NaremitIMG can chain multiple processes together to manipulate images. Processes are separated by the '|' (pipe) symbol and are processed one at a time in the order provided. Some processing commands accept additional parameters separated using commas. For example...

    p=cropratio,1|resize,100,100|grayscale

...performs the following manipulations:

 1. Crop the image to a square shape (using the `cropratio` command), then,
 2. resizes the output to 100x100 pixels (using the `resize` command), then,
 3. removes colour information (using the `grayscale` command).

The available commands are as follows:

#### Autocontrast `USAGE: autocontrast`

#### Blur `USAGE: blur`
See "Gaussian Blur" below for more powerful blurring options.

#### Brightness `USAGE: brightness,[FLOAT]`
    Example: ?p=brightness,0.75
This command accepts one floating-point number&p=colorize,%23000,%23f00 parameter. A number less than 1.0 darkens the image and a number greater than 1.0 brightens it. A value of 0 returns a completely black image.

#### Color `USAGE: color,[FLOAT]`
    Example: ?p=color,1.1
This command accepts one floating-point number parameter. A number less than 1.0 reduces color information from the image and a number greater than 1.0 increases it. A value of 0 removes all color information and is equivalent to the "grayscale" command below.

#### Colorize `USAGE: colorize,[BACKGROUND COLOR],[FOREGROUND COLOR]`
    Examples:
        ?p=colorize,black,red
        ?p=colorize,%23000,%23f00 (note the '%23' replacement for the '#' sign when dealing with hex colors)
Colorizes the image between the provided colors. Easier for you to try it than for me to explain. :)
    
#### Contour `USAGE: contour`

#### Contrast `USAGE: contrast,[AMOUNT - FLOAT]`
    Example: ?p=contrast,1.2
This command accepts one floating-point number parameter. A number less than 1.0 reduces the contrast of the image and a number greater than 1.0 increases it. A value of 0 returns a completely gray image.

#### Crop `USAGE: crop,[X1 - INTEGER],[Y1 - INTEGER],[X2 - INTEGER],[Y2 - INTEGER]`
    Example: ?p=crop,100,100,400,300
Crop the image within the coordinates (from the top left corner) specified.

#### Crop Ratio `USAGE: cropratio,[RATIO - FLOAT]`
    Example: ?p=cropratio,1.4
Crops the image from the center to match the image ratio provided to it. Image ratio is calculated as (width / height), meaning a landscape image is greater than 1, a square image is 1 exactly, and a portrait image has a ratio of less than 1. 

Use in conjuction with `resize` to create fixed size images, e.g. to create 80x120 thumbnails, use:
    ?p=cropratio,0.6666666666|resize,80,120
    
#### Emboss `USAGE: emboss`

#### Equalize `USAGE: equalize`

#### Flip Horizontal `USAGE: fliphoriz`

#### Flip Vertical `USAGE: flipvert`

#### Gaussian Blur `USAGE: gblur,[PIXELS - INTEGER]`
    Example: ?p=gblur,2
Apply a Gaussian blur to the image. The second parameter is required and specifies the blur distance in pixels. 

#### Invert `USAGE: invert`

#### Posterize `USAGE: posterize,[AMOUNT - INTEGER]`
    Example: ?p=posterize,2
Reduce the number of bits for each color channel.

#### Resize `USAGE: resize,[WIDTH - INTEGER],[HEIGHT - INTEGER]`
    Example: ?p=resize,600,400
Resize an image to fixed pixel dimensions. Especially useful in conjunction with `cropratio`.

#### Resize Percentage `USAGE: resizepc,[WIDTH %AGE - FLOAT],[HEIGHT %AGE - FLOAT]`
    Example: ?p=resize,0.5,0.5
Resize an image to a percentage of its original size, e.g. to make an image 25% the size of the original, use `resizepc,0.25,0.25`

#### Rotate `USAGE: rotate,[ANGLE - INTEGER]`
    Example: ?p=rotate,90
Rotate an image through a given number of degrees.

#### Sharpness `USAGE: sharpness,[AMOUNT - INTEGER]`
    Example: ?p=sharpness,0.5
This command accepts one floating-point number parameter. A number less than 1.0 reduces the sharpness of the image and a number greater than 1.0 increases it.

#### Solarize `USAGE: solarize,[AMOUNT - INTEGER]`
    Example: ?p=solarize,20
Invert all pixel values above the given threshold.

Domain
------
The `domain` parameter is useful if you wish to hide the domain of the _source image_ from prying eyes. So instead of a URL such as...

    mywebsite.com/path/to/naremitimg?uri=http://mysecretplace.example.com/images/dog.gif

...you code specify...

    mywebsite.com/path/to/naremitimg?domain=secret&uri=dog.gif

Then, in your `settings.py` file, add the following:

    NAREMITIMG= {
        'secret': 'http://mysecretplace.example.com/images/',
    }
    
The code then simply appends the two strings together, e.g. `"%s%s" % (domain, uri)` to create the full URL. You can add as many entries to this dictionary as you like.
  
Contribute
----------
This project needs more testing, units tests and for the documentation to be moved to a 'readthedocs' Sphinx style format for easier use. All help is welcomed and gratefully appreciated, however big or small.

Before submitting a pull request, please ensure the docs are updated to reflect the changes you have made. We rely on your feedback so please report any bugs or comments, good or bad, via https://github.com/naremit/NaremitIMG/issues. 

Learn More
----------
NaremitIMG was developed original by [Naremit, a digital agency based in Bangkok, Thailand](http://naremit.com). 

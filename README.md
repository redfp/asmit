# Asmit

### Description

A small image toolbox written in Python. Can be used to blur, dim,
resize, crop, enlarge, copy or convert an image. Requires
ImageMagick. Basic use cases include:

- Creating a wallpaper from an image;
- Creating an avatar from an image;
- Creating an album art from an image.

> Q: Why not just use a bare imagemagick CLI?
> 
> A: Too hard for me to remember all the commands.

The idea was born out of need of some application which could create
static phone wallpapers like Muzei does (with blur and decreased
brightness), without having to do it manually. Remaining functionality
was conceived after several similar frustrations.

### Installation

This script can be used without any installation whatsoever, so just
copy it wherever is convenient for you. Do not forget to run:

``` sh
$ pip install -r requirements.txt
$ chmod +x asmit.py
```

If you do not have a `/usr/bin/python3` binary, edit the first line of
the script accordingly.

### Usage

```
./asmit.py [-h | --help | -?]
    Display this message and exit.

./asmit.py <input_filename> [-v | --verbose]
                           [-s | --show]
                           [(-b | --blur) <percent>]
                           [(-d | --dim) <percent>]
                           [(-c | --crop) [(<W>x<H> | <W>:<H>) ?= 1:1]]
                           [(-l | --enlarge) [<W>:<H> ?= 1:1]
                                             [<blur_percent> ?= 50]]
                           [(-r | --resize) (min | max) <side>]
                           [<output_filename>]
    Flags:
        -v, --verbose -- If present, ./asmit.py will output more info
                           during execution.
    Variables:
        <input_filename>: String  -- Initial image.
        <percent>: Integer        -- A percentage
                                       (usually should be between 0 and 100).
        <W>: Integer              -- Width of an image or a ratio
                                       (depending on a separator).
        <H>: Integer              -- Height of an image or a ratio
                                       (depending on a separator).
        <blur_percent>: Integer   -- A percentage used for blur during
                                       enlargement.
        <side>: Integer           -- Minimum or maximum
                                       (depending on a previous argument)
                                       side of resulting image.
        <output_filename>: String -- Resulting image. It should contain at
                                       least one dot ('.').
    Commands:
        -s, --show
                    -- Display current image.
        -b, --blur <percent>
                    -- Blur by <percent>%.
        -d, --dim <percent>
                   -- Decrease brightness by <percent>%.
        -c, --crop [(<W>x<H> | <W>:<H>) ?= 1:1]
                    -- Centered crop. If <W>x<H> were given, it will crop image
                         to specified rectangle in the center. If <W>:<H> were
                         given, it will crop the image to fit it into specified
                         aspect ratio. If the argument is omitted, it will be
                         replaced by 1:1.
        -l, --enlarge [<W>:<H> ?= 1:1] [<blur_percent> ?= 50]
                       -- Enlarge the image to fit in specified aspect ratio
                            by blurring the background by specified
                            <blur_percent>. If <W>:<H> is omitted, 1:1 is used
                            instead. Default value for <blur_percent> is 50.
        -r, --resize (min | max) <side>
                      -- Resize one side of the image, while keeping the aspect
                           ratio. Selecting min will resize the image so that
                           the smallest side would be <side> pixels, and "max"
                           will ensure that the largest side is <side> pixels.
        <output_filename>
         -- Save result to <output_filename>.
    Also:
        You can combine commands in any way you want, they would be applied
        sequentially. However, initial image path should always be the first
        argument (because you cannot apply commands to nothing).
```

### Examples:

Crop a picture to a square 1000x1000 image:

``` sh
$ ./asmit.py input.png -c -r max 1000 ouput.png
```

Crop a picture to 16:9 aspect ratio, save it to `output_cropped.png`,
then blur it by 10%, decrease brightness by 30% and save the result to
`output_blurred.png`.

``` sh
$ ./asmit.py input.png -c 16:9 output_cropped.jpg -b 10 -d 30 output_blurred.png
```

Enlarge a picture to 1:1 aspect ratio while blurring the background by
50%, show it, enlarge it to 2:1 aspect ratio without blur, show it,
and crop it back to 1:1 (and show it). The resulting image is not
saved anywhere.

``` sh
$ ./asmit.py input.png -l -s -l 0 2:1 -s -c 1:1 -s
```

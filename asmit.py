#!/usr/bin/python3

from wand.image import Image
from wand.display import display
from sys import argv
from os import path


VERBOSE = False
USAGE = f"""A small image toolbox.
Usage:
{argv[0]} [-h | --help | -?]
    Display this message and exit.

{argv[0]} <input_filename> [-v | --verbose]
                           [-s | --show]
                           [(-b | --blur) <percent>]
                           [(-d | --dim) <percent>]
                           [(-c | --crop) [(<W>x<H> | <W>:<H>) ?= 1:1]]
                           [(-l | --enlarge) [<W>:<H> ?= 1:1]
                                             [<blur_percent> ?= 50]]
                           [(-r | --resize) (min | max) <side>]
                           [<output_filename>]
    Flags:
        -v, --verbose -- If present, {argv[0]} will output more info
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
"""


def vprint(*args, **kwargs):
    if VERBOSE:
        print(*args, **kwargs)


def get_new_size_given_ratio(
    old_width: int,
    old_height: int,
    new_ratio_width: int,
    new_ratio_height: int,
    fit: bool = True,
) -> (int, int):
    w = old_width
    h = old_height
    if fit == (new_ratio_width / new_ratio_height < w / h):
        w = (h * new_ratio_width) // new_ratio_height
    else:
        h = (w * new_ratio_height) // new_ratio_width
    return w, h


def blur(image: Image, percent: int) -> None:
    vprint("[INFO] Blurring image...")
    image.blur(sigma=percent)
    vprint("[INFO] Blurred.")


def dim(image: Image, percent: int) -> None:
    vprint("[INFO] Dimming image...")
    image.brightness_contrast(brightness=-percent)
    vprint("[INFO] Dimmed.")


def crop_to_ratio(image: Image, width: int = 1, height: int = 1) -> None:
    vprint("[INFO] Cropping to ratio...")
    w, h = get_new_size_given_ratio(
        old_width=image.width,
        old_height=image.height,
        new_ratio_width=width,
        new_ratio_height=height,
        fit=True,
    )
    vprint("[INFO] Calculated ratio.")
    return crop_to_rect(image=image, width=w, height=h)


def crop_to_rect(image: Image, width: int, height: int) -> None:
    vprint("[INFO] Cropping to rectangle...")
    image.crop(width=width, height=height, gravity="center")
    vprint("[INFO] Cropped.")


def enlarge(
    image: Image, width: int = 1, height: int = 1, blur_percentage: int = 50
) -> None:
    vprint("[INFO] Enlarging image...")
    w, h = get_new_size_given_ratio(
        old_width=image.width,
        old_height=image.height,
        new_ratio_width=width,
        new_ratio_height=height,
        fit=False,
    )
    with image.clone() as im:
        crop_to_ratio(image, width=width, height=height)
        image.resize(width=w, height=h)
        blur(image, blur_percentage)
        image.composite(im, gravity="center")

    vprint("[INFO] Enlarged.")


def resize(image: Image, side: int, fit: bool = True):
    vprint("[INFO] Resizing image...")
    w = image.width
    h = image.height
    if fit == (w > h):
        h = (side * h) // w
        w = side
    else:
        w = (side * w) // h
        h = side
    image.resize(width=w, height=h)
    vprint("[INFO] Resized.")


if __name__ == "__main__":
    if len(argv) == 1 or argv[1] in ("-h", "--help", "-?"):
        print(USAGE)
        exit(0)
    input_filename = argv[1]
    if not path.isfile(input_filename):
        print(f"[ERROR] Not a file: {input_filename}")
        exit(1)
    if len(argv) == 2:
        print(
            "[WARN] No commands were passed after an image.\n"
            f"Consult `{argv[0]} --help` for usage."
        )
    with Image(filename=input_filename) as image:
        i = 2
        while i < len(argv):
            arg = argv[i]
            if arg in ("-v", "--verbose"):
                VERBOSE = True
                vprint("[INFO] Verbose mode on.")
            elif arg in ("-s", "--show"):
                vprint("[INFO] Display.")
                display(image)
            elif arg in ("-b", "--blur"):
                i += 1
                if argv[i].isdecimal():
                    percent = int(argv[i])
                    vprint(f"[INFO] Blur {percent}%.")
                    blur(image=image, percent=percent)
                else:
                    print(
                        "[ERROR] Wrong argument to blur: expected <percent>:"
                        f" Int, received {argv[i]}"
                    )
                    exit(1)
            elif arg in ("-d", "--dim"):
                i += 1
                if argv[i].isdecimal():
                    percent = int(argv[i])
                    vprint(f"[INFO] Dim {percent}%.")
                    dim(image=image, percent=percent)
                else:
                    print(
                        "[ERROR] Wrong argument to dim: expected <percent>:"
                        f" Int, received {argv[i]}"
                    )
                    exit(1)
            elif arg in ("-c", "--crop"):
                i += 1
                if i >= len(argv):
                    wh = "1:1"
                else:
                    wh = argv[i].lower()
                wa = True
                if "x" in wh and wh.count("x") == 1:
                    w, h = wh.split("x")
                    if w.isdecimal() and h.isdecimal():
                        w, h = int(w), int(h)
                        vprint(f"[INFO] Crop to rectangle {w}x{h}")
                        crop_to_rect(image=image, width=w, height=h)
                        wa = False
                elif ":" in wh and wh.count(":") == 1:
                    w, h = wh.split(":")
                    if w.isdecimal() and h.isdecimal():
                        w, h = int(w), int(h)
                        vprint(f"[INFO] Crop to ratio {w}:{h}")
                        crop_to_ratio(image=image, width=w, height=h)
                        wa = False
                if wa:
                    i -= 1
                    vprint("[INFO] Crop to ratio 1:1")
                    crop_to_ratio(image=image, width=1, height=1)
            elif arg in ("-l", "--enlarge"):
                fa = "1:1"
                sa = "50"
                fa_set = False
                sa_set = False
                for j in range(2):
                    i += 1
                    if i < len(argv):
                        if argv[i].isdecimal() and not sa_set:
                            sa = int(argv[i])
                            sa_set = True
                            i += 1
                        elif (
                            ":" in argv[i]
                            and argv[i].count(":") == 1
                            and all([e.isdecimal() for e in argv[i].split(":")])
                            and not fa_set
                        ):
                            fa = argv[i]
                            fa_set = True
                            i += 1
                    i -= 1
                w, h = map(int, fa.split(":"))
                percent = int(sa)
                vprint(f"[INFO] Enlarge to ratio {w}:{h} by with {percent}% blur.")
                enlarge(image=image, width=w, height=h, blur_percentage=percent)
            elif arg in ("-r", "--resize"):
                i += 1
                if argv[i].lower() not in ("min", "max"):
                    print(
                        "[ERROR] Wrong argument to resize: expected 'min' or"
                        f" 'max', received {argv[i]}"
                    )
                    exit(1)
                fit = argv[i] == "max"
                i += 1
                if argv[i].isdecimal():
                    side = int(argv[i])
                    vprint(f"[INFO] Resize fit={fit} {side}.")
                    resize(image=image, side=side, fit=fit)
                else:
                    print(
                        "[ERROR] Wrong argument to resize: expected <side>:"
                        f" Int, received {argv[i]}"
                    )
                    exit(1)
            elif "." in arg:
                filename = path.normpath(arg)
                image.save(filename=filename)
                vprint(f"[INFO] Saved to {filename}.")
            else:
                print(
                    f"[ERROR] Unknown command or misplaced argument: {arg}.\n"
                    f"Try `{argv[0]} --help`."
                )
                exit(1)
            i += 1

import os

import pandas as pd
import numpy as np
import math
from PIL import Image

IMAGE_SIZE = 28
IMAGE_COUNT = 10
IMAGE_SCALE = 4


# region filler
def lerp(t, a, b):
    return a + (b - a) * t


lerp_v = np.vectorize(lerp)


def map_range(t, a, b, c, d):
    return (t - a) / (b - a) * (d - c) + c


def clamp(t, a, b):
    return min(max(t, a), b)


def gammaToLinear(c):
    if c >= 0.04045:
        return math.pow(((c + 0.055) / 1.055), 2.4)
    else:
        return c / 12.92


def linearToGamma(c):
    if c >= 0.0031308:
        return 1.055 * math.pow(c, 1 / 2.4) - 0.055
    else:
        return 12.92 * c


def rgbToOklab(r, g, b):
    r = gammaToLinear(r / 0xFF)
    g = gammaToLinear(g / 0xFF)
    b = gammaToLinear(b / 0xFF)
    # This is the Oklab math:
    l = 0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b
    m = 0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b
    s = 0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b
    # Math.crb (cube root) here is the equivalent of the C++ cbrtf function here: https://bottosson.github.io/posts/oklab/#converting-from-linear-srgb-to-oklab
    l = l ** (1 / 3)
    m = m ** (1 / 3)
    s = s ** (1 / 3)
    return (
        l * +0.2104542553 + m * +0.7936177850 + s * -0.0040720468,
        l * +1.9779984951 + m * -2.4285922050 + s * +0.4505937099,
        l * +0.0259040371 + m * +0.7827717662 + s * -0.8086757660,
    )


def oklabToSRGB(L, a, b):
    l = L + a * +0.3963377774 + b * +0.2158037573
    m = L + a * -0.1055613458 + b * -0.0638541728
    s = L + a * -0.0894841775 + b * -1.2914855480
    # The ** operator here cubes; same as l_*l_*l_ in the C++ example:
    l = l**3
    m = m**3
    s = s**3
    r = l * +4.0767416621 + m * -3.3077115913 + s * +0.2309699292
    g = l * -1.2684380046 + m * +2.6097574011 + s * -0.3413193965
    b = l * -0.0041960863 + m * -0.7034186147 + s * +1.7076147010
    # Convert linear RGB values returned from oklab math to sRGB for our use before returning them:
    r = 0xFF * linearToGamma(r)
    g = 0xFF * linearToGamma(g)
    b = 0xFF * linearToGamma(b)
    # OPTION: clamp r g and b values to the range 0-0xFF; but if you use the values immediately to draw, JavaScript clamps them on use:
    r = clamp(r, 0, 0xFF)
    g = clamp(g, 0, 0xFF)
    b = clamp(b, 0, 0xFF)

    # OPTION: round the values. May not be necessary if you use them immediately for rendering in JavaScript, as JavaScript (also) discards decimals on render:
    r = round(r)
    g = round(g)
    b = round(b)

    return (r, g, b)


def hexToRGB(s: str):
    hx = s.replace("#", "")
    # NOTE: This can be removed for brevity if you stick with 6-character codes:
    # if (hx.length === 3) {hx = hx[0] + hx[0] + hx[1] + hx[1] + hx[2] + hx[2];}
    num = int(hx, 16)
    return (num >> 16, (num >> 8) & 0xFF, num & 0xFF)


def rgbToInt(r, g, b):
    return r << 16 | g << 8 | b


def rgbToHex(r, g, b):
    return "#" + "%06x" % rgbToInt(r, g, b)


def mapPalette(t: int, palette: np.ndarray):
    if t == 0xFF:
        return palette[-1]
    t0 = map_range(t, 0x00, 0xFF, 0.0, 1.0)
    n = np.shape(palette)[0]
    k = t0 * (n - 1)
    i = math.floor(k)
    j = k - i
    return lerp_v(j, palette[i], palette[i + 1])


# endregion

dirname = os.path.dirname(__file__)
filepath = os.path.join(dirname, "fashion-mnist_test.csv")
df = pd.read_csv(filepath, index_col="label")

colors = [
    "#2e222f",
    "#3e3546",
    "#625565",
    "#966c6c",
    "#ab947a",
    "#694f62",
    "#7f708a",
    "#9babb2",
    "#c7dcd0",
    "#ffffff",
    "#6e2727",
    "#b33831",
    "#ea4f36",
    "#f57d4a",
    "#ae2334",
    "#e83b3b",
    "#fb6b1d",
    "#f79617",
    "#f9c22b",
    "#7a3045",
    "#9e4539",
    "#cd683d",
    "#e6904e",
    "#fbb954",
    "#4c3e24",
    "#676633",
    "#a2a947",
    "#d5e04b",
    "#fbff86",
    "#165a4c",
    "#239063",
    "#1ebc73",
    "#91db69",
    "#cddf6c",
    "#313638",
    "#374e4a",
    "#547e64",
    "#92a984",
    "#b2ba90",
    "#0b5e65",
    "#0b8a8f",
    "#0eaf9b",
    "#30e1b9",
    "#8ff8e2",
    "#323353",
    "#484a77",
    "#4d65b4",
    "#4d9be6",
    "#8fd3ff",
    "#45293f",
    "#6b3e75",
    "#905ea9",
    "#a884f3",
    "#eaaded",
    "#753c54",
    "#a24b6f",
    "#cf657f",
    "#ed8099",
    "#831c5d",
    "#c32454",
    "#f04f78",
    "#f68181",
    "#fca790",
    "#fdcbb0",
]
clothes_types = [
    "T-shirt",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

colors = np.array(colors)
hexToRGB_v = np.vectorize(hexToRGB)
rgbToHex_v = np.vectorize(rgbToHex)
rgbToInt_v = np.vectorize(rgbToInt)
rgbToOklab_v = np.vectorize(rgbToOklab)
oklabToSRGB_v = np.vectorize(oklabToSRGB)

for idx in df.index.unique():
    sub_df = df.loc[idx]
    sub_df = sub_df.iloc[: IMAGE_COUNT**2]

    final_img = Image.new("RGB", (IMAGE_COUNT * IMAGE_SIZE, IMAGE_COUNT * IMAGE_SIZE))

    k = 0
    for i, image in sub_df.iterrows():
        x = (k % IMAGE_COUNT) * IMAGE_SIZE
        y = (k // IMAGE_COUNT) * IMAGE_SIZE
        k = k + 1
        palette = np.random.choice(colors, 2)

        r, g, b = hexToRGB_v(palette)
        ok = rgbToOklab_v(r, g, b)
        ok_v = np.array(ok)
        palette = ok_v.T

        palette_swapped = np.array([mapPalette(i, palette) for i in image])
        palette_swapped_rgb = np.array(oklabToSRGB_v(*palette_swapped.T))
        final_mapping = np.array(
            np.split(palette_swapped_rgb.T, IMAGE_SIZE), dtype=np.uint8
        )
        img = Image.fromarray(final_mapping, mode="RGB")

        final_img.paste(img, (x, y))

    scale_factor = IMAGE_SIZE * IMAGE_COUNT * IMAGE_SCALE
    final_img = final_img.resize((scale_factor, scale_factor), Image.Resampling.BOX)
    final_img.save("%s.jpeg" % clothes_types[idx])

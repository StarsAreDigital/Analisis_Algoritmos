import base64
import os
from io import BytesIO

import numpy as np
import pandas as pd
from _tmap import VectorFloat
from faerun import Faerun
from PIL import Image
from tmap.layout_generators.builtin_layout_generator import (
    LSHForest,
    Minhash,
    layout_from_lsh_forest,
)
import matplotlib.pyplot as plt

cmap = plt.get_cmap("viridis")
norm = plt.Normalize()


def map_range(x, a, b, c, d):
    return (x - a) / (b - a) * (d - c) + c


dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "fashion-mnist_test.csv")

df = pd.read_csv(file_path, index_col="label")

dims = 1024
enc = Minhash(28 * 28, 42, dims)

faerun = Faerun(clear_color="#111111", view="front", coords=False)

legend_labels = [
    "T-shirt/top",
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

for idx in df.index.unique():
    print(f"processing idx {idx} ({legend_labels[idx]})")
    sub_df = df.loc[idx]

    lf = LSHForest(dims * 2, 128)

    tmp = []
    labels = []
    print("Generating image labels")
    for _, image in sub_df.iterrows():
        tmp.append(VectorFloat(image / 255))
        arr = np.uint8(np.split(np.array(image), 28))
        img = Image.fromarray(arr)
        buffered = BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        labels.append("data:image/bmp;base64," + img_str.decode("utf-8"))

    tmp = [VectorFloat(image / 255) for _, image in sub_df.iterrows()]
    lf.batch_add(enc.batch_from_weight_array(tmp))
    lf.index()
    print("Generating lsh")
    x, y, s, t, _ = layout_from_lsh_forest(lf)

    faerun.add_scatter(
        "FMNIST",
        {
            "x": x,
            "y": y,
            "c": sub_df.index.to_numpy(),
            "labels": labels,
        },
        colormap="RdPu",
        shader="smoothCircle",
        point_scale=2.5,
        max_point_size=10,
    )
    faerun.add_tree("FMNIST_TREE", {"from": s, "to": t}, point_helper="FMNIST")

    faerun.plot(f"fmnist{idx}", template="url_image")

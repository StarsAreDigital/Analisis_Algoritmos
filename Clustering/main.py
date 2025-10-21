import os

import numpy as np
import pandas as pd
from _tmap import VectorFloat
from matplotlib import pyplot as plt

# from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from tmap.layout_generators.builtin_layout_generator import (
    LSHForest,
    Minhash,
    layout_from_lsh_forest,
)

dirname = os.path.dirname(__file__)
file_path = os.path.join(dirname, "fashion-mnist_test.csv")
plt.style.use("dark_background")

df = pd.read_csv(file_path, index_col="label")

dims = 1024
enc = Minhash(28 * 28, 42, dims)

fig, axs = plt.subplots(2, 5)
fig.set_size_inches(12, 8)
fig.tight_layout()

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
    sub_df = df.loc[idx]

    lf = LSHForest(dims * 2, 128)
    tmp = [VectorFloat(image / 255) for _, image in sub_df.iterrows()]
    lf.batch_add(enc.batch_from_weight_array(tmp))
    lf.index()
    x, y, s, t, _ = layout_from_lsh_forest(lf)
    # x, y: VectorArray
    # s, t: IntArray

    axs[idx // 5, idx % 5].set_aspect("equal")
    axs[idx // 5, idx % 5].set_title(legend_labels[idx])
    # axs[idx // 5, idx % 5].scatter(
    #     x, y, c=np.random.randint(0, len(df.index.unique()), len(sub_df.index))
    # )
    axs[idx // 5, idx % 5].scatter(x, y, c=np.full(len(sub_df.index), f"C{idx}"))

plt.show()

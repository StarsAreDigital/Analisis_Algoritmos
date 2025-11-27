import numpy as np

import pandas as pd

from layer import Layer, Convolutional, MaxPooling, Reshape, Dense
from activation import Softmax, Sigmoid
from network import train, predict
from loss import binary_cross_entropy, binary_cross_entropy_prime


# Limit to 2 classes
def preprocess(x: np.ndarray, y: np.ndarray, limit: int):
    # index0 = np.where(y == 0)[0][:limit]
    # index1 = np.where(y == 1)[0][:limit]
    # indexes = np.hstack((index0, index1))
    # rng = np.random.default_rng()
    # indexes = rng.permutation(indexes)
    # x, y = x[indexes], y[indexes]

    x, y = x[:limit], y[:limit]

    x = x.reshape((-1, 1, 28, 28))
    x = x.astype(np.float32) / 255

    y = np.identity(np.max(y) + 1)[y]
    y = np.expand_dims(y, -1)

    return x, y


classes = 10
network: list[Layer] = [
    Convolutional((1, 28, 28), 3, 5),
    MaxPooling((5, 26, 26), 2),
    Sigmoid(),
    Reshape((5, 13, 13), (5 * 13 * 13, 1)),
    Dense(5 * 13 * 13, classes),
    Softmax(),
]

print("Loading training dataset...", end=" ")
df = pd.read_csv("fashion-mnist_train.csv", index_col=0)
print("Done!")
x_train = df.to_numpy(np.uint8)
y_train = np.array(df.index.values.tolist(), np.uint8)
print("Preprocessing...", end=" ")
x_train, y_train = preprocess(x_train, y_train, 1000)
print("Done!")

print("Loading testing dataset...", end=" ")
df = pd.read_csv("fashion-mnist_test.csv", index_col=0)
print("Done!")
x_test = df.to_numpy(np.uint8)
y_test = np.array(df.index.values.tolist(), np.uint8)
print("Preprocessing...", end=" ")
x_test, y_test = preprocess(x_test, y_test, 10)
print("Done!")

# fig, axes = plt.subplots(5, 5)
# for ax in axes.flatten():
#     ax.set_xticks([])
#     ax.set_yticks([])
# for i, (x, y) in enumerate(zip(x_train, y_train)):
#     idx = np.unravel_index(i, axes.shape)
#     axes[idx].imshow(x[0])
#     axes[idx].set_title(str(y))
# plt.show()

train(network, binary_cross_entropy, binary_cross_entropy_prime, x_train, y_train, 100)

out_shape = y_test.shape
out_shape[0] += 1
out_shape[1] += 1

results = np.zeros(out_shape)
results[0, 0] = "Real"
results[0, 1:] = np.arange(classes)
for i, (x, y) in enumerate(zip(x_test, y_test)):
    out = predict(network, x)
    print(f"pred: {np.argmax(out)}, true: {np.argmax(y)}, probs: {out}")
    results[i, 0] = np.argmax(y)
    results[i, 1:] = out

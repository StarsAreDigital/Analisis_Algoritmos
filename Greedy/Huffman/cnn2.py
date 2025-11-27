import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

ALPHA = 0.001


def ReLu(input_volume):
    input_volume[input_volume < 0] *= ALPHA
    return input_volume


def deLeReLu(input_volume):
    input_volume[input_volume < 0] = ALPHA
    return input_volume


class Convolutional:
    def __init__(
        self,
        image_dim=(1, 16, 16),
        kernels=(2, 1, 3, 3),
        padding=1,
        stride=1,
        bias=0.1,
        eta=0.01,
    ):
        assert image_dim[0] == kernels[1]

        self.image_dim = (
            image_dim[0],
            image_dim[1] + 2 * padding,
            image_dim[2] + 2 * padding,
        )
        self.specs = kernels
        self.padding = padding
        self.stride = stride
        self.eta = eta
        self.iteration = 0
        self.bias = []
        self.cache = 0

        self.filters = np.random.rand(*kernels) * 0.1

        for _ in range(kernels[0]):
            self.bias.append(bias)

    def pad(self, image):
        p = self.padding
        new_img = np.pad(
            image,
            ((0, 0), (p, p), (p, p)),
            constant_values=0,
        )
        return new_img

    def out_dimension(self, f_y, f_x):
        depth, height, width = self.image_dim
        out_H = (height - f_y + 1) / self.stride
        out_W = (width - f_x + 1) / self.stride
        out_H = int(out_H)
        out_W = int(out_W)

        return depth, out_H, out_W

    def iterate_img(self, image, f_y, f_x, stride):
        _, height, width = image.shape
        for i in range(0, height - f_y + 1, stride):
            for j in range(0, width - f_x + 1, stride):
                yield image[:, i : i + f_y, j : j + f_x], i, j

    def forward(self, image):
        if self.padding != 0:
            image = self.pad(image)

        self.cache = image

        n_kernels, _, f_y, f_x = self.specs
        _, out_H, out_W = self.out_dimension(f_y, f_x)

        out = np.zeros((n_kernels, out_H, out_W))

        for kernel in range(n_kernels):
            for region, i, j in self.iterate_img(image, f_y, f_x, self.stride):
                out[kernel, i, j] = np.sum(self.filters[kernel] * region)

        return ReLu(out)

    def bp(self, d_out_vol):
        d_out_vol = deLeReLu(d_out_vol)

        image = self.cache
        n_kernels, f_d, f_y, f_x = self.specs
        d_input = np.zeros(self.image_dim)
        d_filters = np.zeros(self.specs)
        d_bias = []

        for kernel in range(n_kernels):
            for region, i, j in self.iterate_img(image, f_y, f_x, self.stride):
                d_filters[kernel] += d_out_vol[kernel, i, j] * region
                


img = Image.open("cilantro.jpg")
img = img.convert("L")
arr = np.asarray(img)
arr = np.expand_dims(arr, 0)

layer = Convolutional(arr.shape, kernels=(16, 1, 3, 3), padding=1)
res = layer.forward(arr)
layer.bp(res)
input()
fig, axes = plt.subplots(4, 4, figsize=(6, 6))
for i, layer in enumerate(res):
    r = i // 4
    c = i % 4
    axes[r, c].imshow(layer, cmap="inferno")
    axes[r, c].set_xticks([])
    axes[r, c].set_yticks([])
plt.show()

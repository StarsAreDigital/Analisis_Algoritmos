import numpy as np

from scipy import signal


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward(self, input):
        pass

    def backward(self, output_gradient, learning_rate):
        pass


class Convolutional(Layer):
    def __init__(self, input_shape, kernel_size, depth):
        input_depth, input_height, input_width = input_shape
        self.depth = depth
        self.input_shape = input_shape
        self.input_depth = input_depth
        self.output_shape = (
            depth,
            input_height - kernel_size + 1,
            input_width - kernel_size + 1,
        )
        self.kernels_shape = (depth, input_depth, kernel_size, kernel_size)
        self.kernels = np.random.randn(*self.kernels_shape)
        self.biases = np.random.randn(*self.output_shape)

    def forward(self, input):
        self.input = input
        self.output = np.copy(self.biases)
        for i in range(self.depth):
            for j in range(self.input_depth):
                self.output[i] += signal.correlate2d(
                    self.input[j], self.kernels[i, j], "valid"
                )
        return self.output

    def backward(self, output_gradient, learning_rate):
        kernels_gradient = np.zeros(self.kernels_shape)
        input_gradient = np.zeros(self.input_shape)

        for i in range(self.depth):
            for j in range(self.input_depth):
                kernels_gradient[i, j] = signal.correlate2d(
                    self.input[j], output_gradient[i], "valid"
                )
                input_gradient[j] += signal.convolve2d(
                    output_gradient[i], self.kernels[i, j], "full"
                )

        self.kernels -= learning_rate * kernels_gradient
        self.biases -= learning_rate * output_gradient
        return input_gradient


class MaxPooling(Layer):
    def __init__(self, input_shape, size):
        depth, input_height, input_width = input_shape
        self.input_shape = input_shape
        self.depth = depth
        self.size = size
        self.output_shape = (
            depth,
            int(np.ceil(input_height / size)),
            int(np.ceil(input_width / size)),
        )

    def forward(self, input):
        self.input = input
        self.output = np.zeros(self.output_shape)
        for d in range(self.depth):
            for i in range(self.output_shape[1]):
                for j in range(self.output_shape[2]):
                    i_input = i * self.size
                    j_input = j * self.size
                    self.output[d, i, j] = np.max(
                        self.input[d, i_input : i_input + self.size, j_input : j_input + self.size]
                    )
        return self.output

    def backward(self, output_gradient, learning_rate=0):
        input_gradient = np.zeros(self.input_shape)
        for d in range(self.depth):
            for i in range(self.output_shape[1]):
                for j in range(self.output_shape[2]):
                    i_input = i * self.size
                    j_input = j * self.size
                    subarea = self.input[
                        d, i_input : i_input + self.size, j_input : j_input + self.size
                    ]
                    idx = np.nanargmax(subarea)
                    y_offset, x_offset = np.unravel_index(idx, subarea.shape)
                    input_gradient[d, i_input + y_offset, j_input + x_offset] = (
                        output_gradient[d, i, j]
                    )
        return input_gradient


class Dense(Layer):
    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(output_size, input_size)
        self.bias = np.random.randn(output_size, 1)

    def forward(self, input):
        self.input = input
        return np.dot(self.weights, self.input) + self.bias

    def backward(self, output_gradient, learning_rate):
        weights_gradient = np.dot(output_gradient, self.input.T)
        input_gradient = np.dot(self.weights.T, output_gradient)
        self.weights -= learning_rate * weights_gradient
        self.bias -= learning_rate * output_gradient
        return input_gradient


class Reshape(Layer):
    def __init__(self, input_shape, output_shape):
        self.input_shape = input_shape
        self.output_shape = output_shape

    def forward(self, input):
        return np.reshape(input, self.output_shape)

    def backward(self, output_gradient, learning_rate):
        return np.reshape(output_gradient, self.input_shape)

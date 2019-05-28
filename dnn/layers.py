import numpy as np
from loss import *

class Layer():
    def __init__(self):
        pass

    def forward(self, input):
        pass

    # @property
    # def self_gradient(self):
    #     return 0
    #
    # @property
    # def model_gradient(self):
    #     return 0

    @property
    def params(self):
        return 0

    def update_model_gradient(self, grad):
        pass


class Dense(Layer):
    def __init__(self, hidden_unit, input_shape, activation):

        '''
        :param hidden_unit:   # of hidden units
        :param input_shape:   input shape
        :param activation:    Activation Class
        '''

        super().__init__()
        # Normal initialization
        self.n, self.p = input_shape  # input_tensor shape
        self.m = hidden_unit

        self.w = np.random.normal(0, 1, (self.p, self.m))
        self.b = np.random.normal(0, 1, (self.n, self.m))

        self.activation = activation

    def forward(self, input_tensor):
        # Forward Propagation
        self.input_tensor = input_tensor
        output = np.matmul(self.input_tensor, self.w) + self.b
        output = self.activation.forward(output)

        self.calculate_self_gradient()

        return output

    def calculate_self_gradient(self):
        # Calculate Self Gradients
        self.grad_w = np.matmul(self.input_tensor.T, self.activation.gradient)
        self.grad_b = self.activation.gradient

        # Model gradients ready for back-prop
        self.model_gradient = self.self_gradient['w']
        # model gradient 就是我要往后传播的东西

    # @property
    # def self_gradient(self):
    #     '''
    #     这个gradient只是自己的 gradient，不是 model 里的。
    #     :return:
    #     '''
    #     return

    # @property
    # def model_gradient(self):
    #     '''
    #     model gradient 就是本层需要向下一层传播的gradient，
    #     这里完全不需要b， 只需要w
    #     :return:
    #     '''
    #     return self._grad

    def update_model_gradient(self, grad):
        '''

        :param grad: 链式法则传过来的上一层的gradient
        :return:
        '''
        # print("Update Model Gradient")
        # print(self.model_gradient.shape)
        # print(grad.shape)
        self.model_gradient = np.matmul(self.model_gradient, grad)

    @property
    def params(self):
        return {'w': self.w,
                'b': self.b}

    @property
    def self_gradient(self):
        return {"w": self.grad_w,
                "b": self.grad_b}


class Input(Layer):
    def __init__(self, input_shape):
        super().__init__()
        self.n, self.p = input_shape  # input_tensor shape

    def forward(self, input_tensor):
        self.input_tensor = input_tensor
        return input_tensor

# -*- coding: utf-8 -*-

import tensorflow as tf

layers = tf.keras.layers
models = tf.keras.models

from yolo.bodynet import Bodynet
from yolo.headnet import Headnet

# Yolo v3
class Yolonet(tf.keras.Model):
    def __init__(self, n_features=255):
        super(Yolonet, self).__init__(name='')
        
        self.body = Bodynet()
        self.head = Headnet()

        self.num_layers = 106
        self._init_vars()

    def call(self, input_tensor, training=False):
        s3, s4, s5 = self.body(input_tensor, training)
        f5, f4, f3 = self.head(s3, s4, s5, training)
        return f5, f4, f3

    def get_variables(self, layer_idx, suffix=None):
        if suffix:
            find_name = "layer_{}/{}".format(layer_idx, suffix)
        else:
            find_name = "layer_{}/".format(layer_idx)
        variables = []
        for v in self.variables:
            if find_name in v.name:
                variables.append(v)
        return variables

    def _init_vars(self):
        import numpy as np
        sample = tf.constant(np.random.randn(1, 224, 224, 3).astype(np.float32))
        self.call(sample, training=False)


if __name__ == '__main__':
    import numpy as np
    tf.enable_eager_execution()
    inputs = tf.constant(np.random.randn(1, 256, 256, 3).astype(np.float32))
    
    # (1, 256, 256, 3) => (1, 8, 8, 1024)
    yolonet = Yolonet()
    f5, f4, f3 = yolonet(inputs)
    print(f5.shape, f4.shape, f3.shape)


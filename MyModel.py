
from tensorflow.keras import Model, layers

class MyModel(Model):
  def __init__(self):
    super(MyModel, self).__init__()
    self.d1 = layers.Dense(9, activation='relu')
    self.d2 = layers.Dense(32, activation = 'relu')
    self.d3 = layers.Dense(32, activation = 'relu')
    self.d4 = layers.Dense(9, activation='softmax')
    

  def call(self, x):
    x = self.d1(x)
    x = self.d2(x)
    x = self.d3(x)
    return self.d4(x)


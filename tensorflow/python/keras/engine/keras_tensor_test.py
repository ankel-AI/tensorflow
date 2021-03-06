# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""InputSpec tests."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from tensorflow.python.framework import dtypes
from tensorflow.python.framework import ops
from tensorflow.python.framework import sparse_tensor
from tensorflow.python.framework import tensor_shape
from tensorflow.python.framework import tensor_spec
from tensorflow.python.keras import layers
from tensorflow.python.keras import testing_utils
from tensorflow.python.keras.engine import keras_tensor
from tensorflow.python.ops import array_ops
from tensorflow.python.platform import test


class KerasTensorTest(test.TestCase):

  def test_repr(self):
    kt = keras_tensor.KerasTensor(
        type_spec=tensor_spec.TensorSpec(shape=(1, 2, 3), dtype=dtypes.float32))
    expected_repr = "<KerasTensor: shape=(1, 2, 3) dtype=float32>"
    self.assertEqual(expected_repr, str(kt))
    self.assertEqual(expected_repr, repr(kt))

    kt = keras_tensor.KerasTensor(
        type_spec=tensor_spec.TensorSpec(shape=(2,), dtype=dtypes.int32),
        inferred_shape_value=[2, 3])
    expected_repr = (
        "<KerasTensor: shape=(2,) dtype=int32 inferred_value='[2, 3]'>")
    self.assertEqual(expected_repr, str(kt))
    self.assertEqual(expected_repr, repr(kt))

    kt = keras_tensor.KerasTensor(
        type_spec=sparse_tensor.SparseTensorSpec(
            shape=(1, 2, 3), dtype=dtypes.float32))
    expected_repr = (
        "<KerasTensor: type_spec=SparseTensorSpec("
        "TensorShape([1, 2, 3]), tf.float32)>")
    self.assertEqual(expected_repr, str(kt))
    self.assertEqual(expected_repr, repr(kt))

    with testing_utils.use_keras_tensors_scope(True):
      inp = layers.Input(shape=(3, 5))
      kt = layers.Dense(10)(inp)
      expected_repr = (
          "<KerasTensor: shape=(None, 3, 10) dtype=float32 (Symbolic value 0 "
          "from symbolic call 0 of layer 'dense')>")
      self.assertEqual(expected_repr, str(kt))
      self.assertEqual(expected_repr, repr(kt))

      kt = array_ops.reshape(kt, shape=(3, 5, 2))
      expected_repr = ("<KerasTensor: shape=(3, 5, 2) dtype=float32 (Symbolic "
                       "value 0 from symbolic call 0 of layer 'tf.reshape')>")
      self.assertEqual(expected_repr, str(kt))
      self.assertEqual(expected_repr, repr(kt))

      kts = array_ops.unstack(kt)
      for i in range(3):
        expected_repr = ("<KerasTensor: shape=(5, 2) dtype=float32 "
                         "(Symbolic value %s from symbolic call 0 "
                         "of layer 'tf.unstack')>" % i)
        self.assertEqual(expected_repr, str(kts[i]))
        self.assertEqual(expected_repr, repr(kts[i]))

if __name__ == "__main__":
  ops.enable_eager_execution()
  tensor_shape.enable_v2_tensorshape()
  test.main()

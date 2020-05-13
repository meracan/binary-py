
import binarypy
import numpy as np

def f1d(format):
  print("Testing {}".format(format))
  output="test/output.bin"
  binarypy.write(output,{"title":"tilename","variables":{"variableA":{"data":np.arange(0,100,dtype=format)}}})
  results=binarypy.read(output)
  np.testing.assert_array_equal(results['variables']["variableA"]['data'],np.arange(0,100,dtype=format))

def f2d(format):
  print("Testing {}".format(format))
  output="test/output.bin"
  binarypy.write(output,{"title":"tilename","variables":{"variableA":{"data":np.arange(0,100,dtype=format)},"variableB":{"data":np.arange(0,400,dtype=format).reshape(200,2)}}})
  results=binarypy.read(output)
  np.testing.assert_array_equal(results['variables']["variableB"]['data'],np.arange(0,400,dtype=format).reshape(200,2))


def test_binarypy():
  f1d("u2")
  f1d("u4")
  f1d("u8")
  f1d("i2")
  f1d("i4")
  f1d("i8")
  f1d("f4")
  f1d("f8")
  
  
  f2d("u2")
  f2d("u4")
  f2d("u8")
  f2d("i2")
  f2d("i4")
  f2d("i8")
  f2d("f4")
  f2d("f8")  
  
if __name__ == "__main__":
  test_binarypy()  
import os
import binpy
import numpy as np

def f1d(format):
  print("Testing {}".format(format))
  buffer=binpy.write({"variableA":np.arange(0,100,dtype=format)})
  results=binpy.read(buffer)
  np.testing.assert_array_equal(results["variableA"],np.arange(0,100,dtype=format))

def f2d(format):
  print("Testing {}".format(format))
  buffer=binpy.write({"variableA":np.arange(0,100,dtype=format),"variableB":np.arange(0,400,dtype=format).reshape(200,2)})
  results=binpy.read(buffer)
  np.testing.assert_array_equal(results["variableB"],np.arange(0,400,dtype=format).reshape(200,2))


def test_binpy():
  f1d("u1")
  f1d("u2")
  f1d("u4")
  f1d("u8")
  f1d("i1")
  f1d("i2")
  f1d("i4")
  f1d("i8")
  f1d("f4")
  f1d("f8")
  
  
  f2d("u1")
  f2d("u2")
  f2d("u4")
  f2d("u8")
  f2d("i1")
  f2d("i2")
  f2d("i4")
  f2d("i8")
  f2d("f4")
  f2d("f8")  
  
def test_file():
  filename="test.bin"
  format="u2"
  
  with open(filename,"wb") as f:
    buffer=binpy.write({"variableA":np.arange(0,100,dtype=format)})
    f.write(buffer)
  
  with open(filename,"rb") as f:
    results=binpy.read(f)
    np.testing.assert_array_equal(results["variableA"],np.arange(0,100,dtype=format))
  
  os.remove(filename)
  
if __name__ == "__main__":
  # test_binpy()
  test_file()
  
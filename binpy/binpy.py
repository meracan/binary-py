from struct import unpack,pack
import numpy as np
import io
dtypeToFormat={
  "int8":"b",
  "int16":"h",
  "int32":"i",
  "int64":"q",
  "uint8":"B",
  "uint16":"H",
  "uint32":"I",
  "uint64":"Q",
  "float32":"f",
  "float64":"d",
}

formatToDtype={
  "b":"int8",
  "h":"int16",
  "i":"int32",
  "q":"int64",
  "B":"uint8",
  "H":"uint16",
  "I":"uint32",
  "Q":"uint64",
  "f":"float32",
  "d":"float64",
}



def read(input, return_header=False):
  
  if isinstance(input,io.BufferedReader):f=input
  else:f=io.BytesIO(input)
  
 
  endian = ">"
  placeholder=f.read(2)
  one,=unpack(endian+'H',placeholder)
  if one!=1:
    endian="<"
    one,=unpack(endian+'H',placeholder)
    if one!=1:
      raise Exception("Not a binary file from binarypy or binaryjs")
  
  # Header 
  nvar,=unpack(endian+'B',f.read(1))
  
  variables={}
  for _ in range(nvar):
    name,format,size,ndim=unpack(endian+'16s1sIB',f.read(16+1+4+1))
    name=name.decode('ascii').rstrip('\x00')
    format=format.decode('ascii').rstrip('\x00')
    
    buf=f.read(ndim*4)
    shape=np.frombuffer(buf,dtype="uint32",count=ndim)
    
    _t=formatToDtype[format]
    itemsize=np.dtype(_t).itemsize
    
    buf=f.read(size*itemsize)
    data=np.frombuffer(buf,dtype=_t,count=size).reshape(shape)
    
    variables[name]=data
  
  if not isinstance(input,io.BufferedReader):f.close()
  return variables      
    


# def write(output,obj):
def write(variables,filePath=None):  
  """
  {
    variableA:np.ndarray,
    variableB:np.ndarray,
  }
  """
  if filePath is None:f=io.BytesIO()
  else:f=open(filePath,"rb")
    
  endian = ">"
  
  # Header 
  nvar = len(variables)
  f.write(pack(endian+'HB',1,nvar))
  
  for name in variables:
    data=variables[name]
    if not isinstance(data,np.ndarray):raise Exception("Needs to be an ndarray")
    ndim=data.ndim
    shape=data.shape
    size=data.size
    format=dtypeToFormat[data.dtype.name].encode()
    f.write(pack(endian+'16s1sIB',name[:16].encode(),format,size,ndim))
    # print(np.array(shape,dtype="I").tobytes())
    
    f.write(np.array(shape,dtype="I").tobytes())
    f.write(data.tobytes())
  
  if filePath is None:buffer=f.getvalue()
  else:buffer=None
  f.close()
  return buffer
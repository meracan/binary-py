from struct import unpack,pack
import numpy as np
import io

# formatToDtype={
#   "b":"int8",
#   "h":"int16",
#   "i":"int32",
#   "q":"int64",
#   "B":"uint8",
#   "H":"uint16",
#   "I":"uint32",
#   "Q":"uint64",
#   "f":"float32",
#   "d":"float64",
# }
formatToDtype={
  "b":"i1",
  "h":"i2",
  "i":"i4",
  "q":"i8",
  "l":"i8",
  "B":"u1",
  "H":"u2",
  "I":"u4",
  "Q":"u8",
  "L":"u8",
  "f":"f4",
  "d":"f8",
  "M":"f8",
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
    name,_type,size,ndim=unpack(endian+'64s1sIB',f.read(64+1+4+1))
    name=name.decode('utf-8').rstrip('\x00')
    _type=_type.decode('utf-8').rstrip('\x00')
    
    buf=f.read(ndim*4)
    shape=np.frombuffer(buf,dtype="{}u4".format(endian),count=ndim)
    
    _t="{}{}".format(endian,formatToDtype[_type])
    itemsize=np.dtype(_t).itemsize
    
    buf=f.read(size*itemsize)
    data=np.frombuffer(buf,dtype=_t,count=size).reshape(shape)
    if _type=="M":data=data.astype("datetime64[ms]")
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
  else:f=open(filePath,"wb")
    
  endian = ">"
  
  # Header 
  nvar = len(variables)
  f.write(pack(endian+'HB',1,nvar))
  # print(variables)
  for name in variables:
    data=variables[name]
   
    if not isinstance(data,np.ndarray):raise Exception("Needs to be an ndarray")
    ndim=data.ndim
    shape=data.shape
    size=data.size
    format=data.dtype.char.encode("utf-8")
    f.write(pack(endian+'64s1sIB',name[:64].encode("utf-8"),format,size,ndim))
    
    
    f.write(np.array(shape,dtype="{}I".format(endian)).tobytes())
    if data.dtype.char=="M":f.write(data.astype('datetime64[ms]').astype("{}{}".format(endian,"d")).tobytes())
    else:f.write(data.astype("{}{}".format(endian,data.dtype.char)).tobytes())
  
  if filePath is None:buffer=f.getvalue()
  else:buffer=None
  f.close()
  return buffer
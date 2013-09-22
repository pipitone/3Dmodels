#!/usr/bin/env python
import sys
binary=False
arg1=sys.argv[1]
if arg1 == '-b': 
  from struct import *
  binary=True
  obj = open(sys.argv[2])
else:
  obj = open(arg1)
_, _, _, _, _, _, np = obj.readline().strip().split()
np = int(np)
vertices=[]
normals=[]
triangles=[]

# np vertices as (x,y,z)
min_x, min_y, min_z = 0, 0, 0
for i in range(np):
  x, y, z = map(float,obj.readline().strip().split()) 
  min_x, min_y, min_z = min(x,min_x), min(y,min_y), min(z,min_z)
  vertices.append((x, y, z))
# move object to the positive quadrant
for i in range(np): 
  x,y,z = vertices[i]
  vertices[i] = (x-min_x,y-min_y,z-min_z)

assert obj.readline().strip() == ""
# np normals as (x,y,z)
for i in range(np):
  normals.append(tuple(map(float,obj.readline().strip().split())))

assert obj.readline().strip() == ""
nt=int(obj.readline().strip().split()[0]) # number of triangles
_, _, _, _, _ = obj.readline().strip().split()
assert obj.readline().strip() == ""
# rest of the file is a list of numbers
points = map(int, "".join(obj.readlines()).strip().split())
points = points[nt:]  # ignore these.. (whatever they are)
for i in range(nt): 
  triangles.append((points.pop(0), points.pop(0), points.pop(0)))

stream = sys.stdout
if binary:
  stream.write(pack('<80xI',nt))
else:
  stream.writeln("solid surface")
for triangle in triangles: 
  x1, y1, z1 = vertices[triangle[0]]
  x2, y2, z2 = vertices[triangle[1]]
  x3, y3, z3 = vertices[triangle[2]]
  # normal = (v2 - v1)x(p3-p1)
  # normal = (  (y2-y1)*(z3-z1)-(y3-y1)*(z2-z1), 
  #            (z2-z1)*(x3-x1)-(x2-x1)*(z3-z1), 
  #            (x2-x1)*(y3-y1)-(x2-x1)*(y2-y1) )
  if binary:
    stream.write(pack('<12f2x',0,0,0,x1,y1,z1,x2,y2,z2,x3,y3,z3))
  else:
    stream.writelin("\tfacet normal {0:e} {1:e} {2:e}".format(0, 0, 0))
    stream.writelin("\t\tstreamer loop")
    stream.writelin("\t\t\tvertex {0:e} {1:e} {2:e}".format(x1, y1, z1))
    stream.writelin("\t\t\tvertex {0:e} {1:e} {2:e}".format(x2, y2, z2))
    stream.writelin("\t\t\tvertex {0:e} {1:e} {2:e}".format(x3, y3, z3))
    stream.writelin("\t\tendloop")
    stream.writelin("\tendfacet")
if not binary:
  stream.writelin("endsolid surface")

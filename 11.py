import cmath
import importlib
import sys
xx=[3,3,4,4,1,1,2,2]
yy=[1,2,1,2,3,4,3,4]
u1=[1.2,3.6]
u2=[3.4,1.8]
dis1=[0,0,0,0,0,0,0,0]
dis2=[0,0,0,0,0,0,0,0]
type1=[]
type2=[]
for n in range(8):
    x=xx[n]
    y=yy[n]
    print(n,x,y)
    dis1[n] =((x-u1[0])**2+(y-u1[1])**2)**0.5
    dis2[n] =((x - u2[0]) ** 2 + (y - u2[1]) ** 2)**0.5
    if dis1[n] <= dis2[n]:
       type1.append(n)
    else:
        type2.append(n)
print(dis1,"\n",dis2)
print(type1,"\n",type2)

sumx=0
sumy=4
for n in type1:
    sumx+=xx[n]
    sumy+=yy[n]
print(sumx/(len(type1)+1),sumy/(len(type1)+1))
sumx=3
sumy=3
for n in type2:
    sumx+=xx[n]
    sumy+=yy[n]
print(sumx/(len(type2)+1),sumy/(len(type2)+1))


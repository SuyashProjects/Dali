from numpy import sum,arrary,amax
from .models import Station

x=[]
for i in range(0,30):
    lol=Station.objects.filter(id=i+1).values('time')[0]['time']
    x.append(lol)
print(x)
l=([[41,40,43,41,44,41,45,40,42,43],[ 54,51,53,51,55,50,52,48,51,52],[44,47,46,49,48,45,41,50,42,49]])
a=array(l)
print("Array of Station TAKT Times:")
print(a)
print("Array of Quantities:")
q=([10,20,30])
print(q)

Total_Quant=sum(q)
print(Total_Quant)

TT1=amax(a[0,:10])
print("TAKT TIME of SKU 1:")
print(TT1)
TT2=amax(a[1,:10])
print("TAKT TIME of SKU 2:")
print(TT2)
TT3=amax(a[2,:10])
print("TAKT TIME of SKU 3:")
print(TT3)

Total_Time=0

for i in range(0,10):
    if(i==0):
        Total_Time=Total_Time+a[0,0]
    else:
        Total_Time=Total_Time+amax(a[0,:(i+1)])

Total_Time=Total_Time+(TT1*(q[0]-1))+(TT2*q[1])+(TT3*q[2])

print("Total Time being used(in mins):")
print(Total_Time/60)

Shift_Time=420*60

Rem_Time=Shift_Time-Total_Time

print("Total Time remaining(in mins):")
print(Rem_Time/60)

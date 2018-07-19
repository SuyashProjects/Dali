from numpy import sum,array,amax,zeros,unique

def main(Sequence,tl,forsub):
 tSKU=[]
 StnTime=array(tl)
 Seq=array(Sequence)
 for key in forsub:
  tSKU.append(key[0])
 SKU=array(tSKU)
 Total_Order=len(Seq)
 Num_SKU=len(unique(Seq))
 Line=zeros(10)
 Time=zeros(10)
 Total_Time=0
 float(Total_Time)
 j=9
 for i in range(0,Total_Order+j):
  if(i>(Total_Order+j-10)):
   while(j!=0):
    Line[j]=Line[j-1]
    j=j-1
   j=9
   Line[0]=0
   print(Line)
   for k in range(0,10):
    for l in range(0,Num_SKU):
     if(Line[k]==SKU[l]):
      Time[k]=StnTime[l][k]
      break
     elif(Line[k]==0):
      Time[k]=0
      break
   Takt_Time=amax(Time)
   print(Takt_Time)
   Total_Time=Total_Time+Takt_Time
  else:
   while(j!=0):
    Line[j]=Line[j-1]
    j=j-1
   j=9
   Line[0]=Seq[i]
   print(Line)
   for k in range(0,10):
    for l in range(0,Num_SKU):
     if(Line[k]==SKU[l]):
      Time[k]=StnTime[l][k]
      break
     elif(Line[k]==0):
      Time[k]=0
      break
   Takt_Time=amax(Time)
   print(Takt_Time)
   Total_Time=Total_Time+Takt_Time
 print(Total_Time)
 return round(Total_Time/60,2)

def sub(forsub,Total_Order):
 tsku=[]
 tq=[]
 tr=[]
 tskips=[]
 tstrips=[]
 li=[]
 for key in forsub:
  tsku.append(key[0])
  tq.append(key[1])
  tr.append(key[2])
  tskips.append(key[3])
  tstrips.append(key[4])
 SKU=array(tsku)
 sz=len(tsku)
 Quants=array(tq)
 qTemp=array(tq)
 TQuant=Total_Order
 Ratio=array(tr)
 Rtemp=array(tr)
 Skips=array(tskips).astype(int)
 Strips=array(tstrips).astype(int)
 j=0
 while(TQuant>0):
  if(j==sz):
   j=0
  elif(qTemp[j]==0):
   j=j+1
  elif((Rtemp[j]>=1) and (qTemp[j]>=1)):
   if(Strips[j]==1):
    li.append(0)
   li.append(SKU[j])
   TQuant=TQuant-1
   Rtemp[j]=Rtemp[j]-1
   qTemp[j]=qTemp[j]-1
   if(Skips[j]==1):
    li.append(0)
  elif(Rtemp[j]==0):
   Rtemp[j]=Ratio[j]
   j=j+1
 return li

from numpy import sum,array,amax,zeros,unique

def main(tSeq,tl,forsub):
 tSKU=[]
 StnTime=array(tl)
 Seq=array(tSeq)
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
 Quants=array(tq)
 Ratio=array(tr)
 SKU=array(tsku)
 Skips=array(tskips).astype(int)
 Strips=array(tstrips).astype(int)
 TQuant=sum(Quants)
 Seq=zeros(3*Total_Order)
 sz=len(SKU)
 j=0
 Rtemp=Ratio
 qTemp=Quants
 Stemp=SKU
 S1temp=Skips
 S2temp=Strips
 while(TQuant>0):
  if(j==sz):
   j=0
  elif(qTemp[j]==0):
   j=j+1
  elif((Rtemp[j]>=1) and (qTemp[j]>=1)):
   ##For Strips
   if(S2temp[j]==1):
    li.append(0)
   ## For Sequencing
   li.append(Stemp[j])
   TQuant=TQuant-1
   Rtemp[j]=Rtemp[j]-1
   qTemp[j]=qTemp[j]-1
   ##For Skip
   if(S1temp[j]==1):
    li.append(0)
  elif(Rtemp[j]==0):
   Rtemp[j]=Ratio[j]
   j=j+1
 return li

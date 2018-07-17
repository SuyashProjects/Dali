from numpy import sum,array,amax,zeros,unique

def main(tSeq,tq,tl):
   a=array(tl)
   q=array(tq)
   Seq=array(tSeq)
   Line=zeros(10)
   sz=len(Seq)
   Time=zeros(10)
   Total_time=0
   j=9
   for i in range(69):
       if(i>59):
           while(j!=0):
               Line[j]=Line[j-1]
               j=j-1
           j=9
           Line[0]=0
           print(Line)
           for k in range(0,10):
               if(Line[k]==1):
                   Time[k]=a[0][k]
               elif(Line[k]==2):
                   Time[k]=a[1][k]
               elif(Line[k]==3):
                   Time[k]=a[2][k]
               else:
                   Time[k]=0
           TKTME=amax(Time)
           print(TKTME)
           Total_time=Total_time+TKTME
       else:
           while(j!=0):
               Line[j]=Line[j-1]
               j=j-1
           j=9
           Line[0]=Seq[i]
           print(Line)
           for k in range(0,10):
               if(Line[k]==1):
                   Time[k]=a[0][k]
               elif(Line[k]==2):
                   Time[k]=a[1][k]
               elif(Line[k]==3):
                   Time[k]=a[2][k]
               else:
                   Time[k]=0
           TKTME=amax(Time)
           print(TKTME)
           Total_time=Total_time+TKTME
   return Total_time

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
 Quants=array(tq)
 Ratio=array(tr)
 Skips=array(tskips).astype(int)
 Strips=array(tstrips).astype(int)
 TQuant=Total_Order
 Seq=zeros(3*TQuant)
 sz=len(SKU)
 j=0
 Rtemp=Ratio
 qTemp=Quants
 Stemp=array(tsku)
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
         ##For Skips
         if(S1temp[j]==1):
             li.append(0)
     elif(Rtemp[j]==0):
         Rtemp[j]=Ratio[j]
         j=j+1
 return li

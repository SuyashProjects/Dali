from numpy import sum,array,amax,zeros,unique

def main(tSeq,tq,tl):
   tl=tl
   a=array(tl)
   tq=tq
   q=array(tq)
   tSeq=tSeq
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
   print("Total Time taken:")
   print(Total_time)
   return Total_time

def sub(tq,tr,tsku,tskips,tstrips):
   tempQuants=tq
   Quants=array(tempQuants)

   tempRatio=tr
   Ratio=array(tempRatio)

   tempSKU=tsku
   SKU=array(tempSKU)

   tSkips=tskips
   Skips=array(tSkips)
   Skips=Skips.astype(int)

   tStrips=tstrips
   Strips=array(tStrips)
   Strips=Strips.astype(int)

   TQuant=sum(tempQuants)

   Seq=zeros(3*TQuant)

   sz=len(tempSKU)


   j=0

   Rtemp=array(tempRatio)

   qTemp=array(tempQuants)

   Stemp=array(tempSKU)

   S1temp=array(tSkips)

   S2temp=array(tStrips)

   li=[]

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

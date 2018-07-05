from numpy import sum
from numpy import array
from numpy import amax
from numpy import zeros

def main(Sequence3):
   tl=([[41,40,43,41,44,41,45,40,42,43],
       [54,51,53,51,55,50,52,48,51,52],
       [44,47,46,49,48,45,41,50,42,49]])
   a=array(tl)
   print("Array of Station TAKT Times:")
   print(a)
   tq=([10,20,30])
   q=array(tq)
   print("Array of Quantities:")
   print(q)
   tSeq=Sequence3
   Seq=array(tSeq)
   Line=zeros(10)
   sz=len(Seq)
   print(Seq)
   print(sz)
   Time=zeros(10)
   Total_time=0
   j=9
   print("Dynamic Line Instances along with TAKT Times:")
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
   print("")
   print("Total Time taken:")
   print(Total_time)
   return Total_time

#PASTE AFTER SEQUENCE
  #Ratio Function
       #WIP
      Ratio1=1
      Ratio2=2
      SKU1=1
      SKU2=2
      Seq=[]
      temp=[]
      for x in range (0,Total_Order):
       for i in range(SKU_Count):
        for y in range(0,Ratio1):
         Seq.append(SKU1)
        for y in range(0,Ratio2):
           Seq.append(SKU2)
      for value in Seq:
          b=Config.objects.filter(SKU=value).values()
          temp.append(b)
      print (temp)

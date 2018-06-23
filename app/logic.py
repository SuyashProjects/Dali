#PASTE AFTER SEQUENCE
  #Ratio Function
       #WIP
      Ratio1=1
      Ratio2=2
      SKU1=1
      SKU2=2
      Seq=[]
      a=Config.objects.all().values('SKU')
      print(a)
      for x in range (0,Total_Order):
       for i in range(a):
        for y in range(0,Ratio1):
         Seq.append(SKU1)
        for y in range(0,Ratio2):
           Seq.append(SKU2)
      print(Seq)

      list1=[]
      list2=[]
      Total_Color=list(Config.objects.aggregate(Count('color',distinct=True)).values())[0]
      Colors=list(Config.objects.values('color').annotate(Color_Count=Count('color')).order_by('-Color_Count'))
      a=Config.objects.values('SKU','color').order_by('color')
      b=Config.objects.values('SKU')
      print(b)
      print(a)
      for key in Colors:
       a=Config.objects.filter(color=key).values('color')
      print(a)


      for i in range(0,SKU_Count):
        SKU5=Config.objects.filter(SKU=i+1).values('SKU','color')[0]['SKU']
        list1.append(SKU5)
        print(list1)
      newlist = sorted(list1, key=itemgetter('color'))
      print(newlist)

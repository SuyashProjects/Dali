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





      SKU5=Config.objects.values_list('SKU', flat=True).order_by('color')
      print(SKU5)
      for i in SKU5:
          list1.append(Config.objects.filter(SKU=SKU5[i-1]).values('SKU')[0]['SKU'])
          print(list1)
          list2.append(Config.objects.filter(SKU=SKU5[i-1]).values('ratio')[0]['ratio'])
          print(list2)
      t=list(zip(list1, list2))
      print(t)

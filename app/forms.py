from django import forms
from .models import Constraint,Config,Seq,Station,Shift

class Form1(forms.ModelForm):
    model = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    tank = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    class Meta:
        model = Config
        fields = ('model','variant','color','tank','time','description')

class Edit(forms.ModelForm):
    SKU = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1,'class':'form-control'}))
    model = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    tank = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    class Meta:
        model = Config
        fields = ('SKU','model','variant','color','tank','time','description')

class Delete(forms.ModelForm):
    SKU = forms.IntegerField(widget=forms.TextInput(attrs={'min': 1,'class':'form-control'}))
    class Meta:
        model = Config
        fields = ('SKU',)

class Form2(forms.ModelForm):
    SKU = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 1,'class':'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    ratio = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    constraints = forms.ModelMultipleChoiceField(queryset=Constraint.objects.values_list('name', flat=True), widget=forms.CheckboxSelectMultiple(),required=False)
    class Meta:
        model = Config
        fields = ('SKU','quantity','ratio','constraints')

class Form3(forms.ModelForm):
    time1 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    time2 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    time3 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    class Meta:
        model = Shift
        fields = ('time',)

class StnForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(StnForm, self).__init__(*args, **kwargs)
       self.fields['SKU'].empty_label = "Select SKU"

    SKU = forms.ModelChoiceField(queryset=Config.objects.values_list('SKU', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    stn1 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn2 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn3 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn4 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn5 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn6 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn7 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn8 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn9 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    stn10 = forms.IntegerField(widget=forms.NumberInput(attrs={'min': 0,'class':'form-control'}))
    class Meta:
        model = Station
        fields = ('SKU','stn1','stn2','stn3','stn4','stn5','stn6','stn7','stn8','stn9','stn10')

from django import forms
from .models import Config

class Form1(forms.ModelForm):
    model = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    tank = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Config
        fields = ('model','variant','color','time','tank')

class Form2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
       super(Form2, self).__init__(*args, **kwargs)
       self.fields['model'].empty_label = "Select Model"
       self.fields['model'].queryset = Config.objects.none()
       self.fields['variant'].empty_label = "Select Variant"
       self.fields['color'].empty_label = "Select Color"
       self.fields['tank'].empty_label = "Select Fuel Tank Type"

    SKU = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    model = forms.ModelChoiceField(queryset=Config.objects.values_list('model', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    variant = forms.ModelChoiceField(queryset=Config.objects.values_list('variant', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    color = forms.ModelChoiceField(queryset=Config.objects.values_list('color', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    tank = forms.ModelChoiceField(queryset=Config.objects.values_list('tank', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    class Meta:
        model = Config
        fields = ('SKU','model','variant','color','quantity','tank')

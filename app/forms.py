from django import forms
from .models import Config,Constraint,Shift,Station

class Form1(forms.ModelForm):
    model = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    tank = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Config
        fields = ('model','variant','color','tank','time','description')

class Form2(forms.ModelForm):
    SKU = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    ratio = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    constraints = forms.ModelMultipleChoiceField(queryset=Constraint.objects.values_list('name', flat=True), widget=forms.CheckboxSelectMultiple(),required=False)
    class Meta:
        model = Config
        fields = ('SKU','quantity','ratio','constraints')

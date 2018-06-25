from django import forms
from .models import Config,Constraint

class Form1(forms.ModelForm):
    model = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    time = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    tank = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    class Meta:
        model = Config
        fields = ('model','variant','color','time','tank','description')

class Form2(forms.ModelForm):
    SKU = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    ratio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    constraints = forms.ModelMultipleChoiceField(queryset=Constraint.objects.values_list('name', flat=True), widget=forms.CheckboxSelectMultiple())
    class Meta:
        model = Config
        fields = ('SKU','quantity','ratio','constraints')

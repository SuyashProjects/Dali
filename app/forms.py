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
    model = forms.ChoiceField(widget=forms.TextInput(attrs={'class':'form-control'}))
    variant = forms.ChoiceField(widget=forms.TextInput(attrs={'class':'form-control'}))
    color = forms.ChoiceField(widget=forms.TextInput(attrs={'class':'form-control'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    constraints = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class':'form-control'}),
        choices='',
    )
    def __init__(self, *args, **kwargs):
        super(Form2, self).__init__(*args, **kwargs)
        self.fields['model'] = forms.ModelChoiceField(
            queryset=Config.objects.only('model')
        )
    class Meta:
        model = Config
        fields = ('model','variant','color','quantity','constraints')

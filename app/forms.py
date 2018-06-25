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
    def __init__(self, *args, **kwargs):
       super(Form2, self).__init__(*args, **kwargs)
       self.fields['model'].empty_label = "Select Model"
       self.fields['variant'].empty_label = "Select Model First"
       self.fields['variant'].queryset = Config.objects.none()
       self.fields['color'].empty_label = "Select Variant First "
       self.fields['color'].queryset = Config.objects.none()
       self.fields['tank'].empty_label = "Select Color First"
       self.fields['tank'].queryset = Config.objects.none()
       if 'model' in self.data:
            try:
                model = int(self.data.get('model'))
                self.fields['variant'].queryset = Config.objects.filter(model=model).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
       elif self.instance.pk:
            self.fields['variant'].queryset = self.instance.model.variant_set.order_by('name')

    SKU = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}),required=False)
    model = forms.ModelChoiceField(queryset=Config.objects.values_list('model', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    variant = forms.ModelChoiceField(queryset=Config.objects.values_list('variant', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    color = forms.ModelChoiceField(queryset=Config.objects.values_list('color', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    tank = forms.ModelChoiceField(queryset=Config.objects.values_list('tank', flat=True),widget=forms.Select(attrs={'class':'form-control'}))
    quantity = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    constraints = forms.ModelMultipleChoiceField(queryset=Constraint.objects.values_list('name', flat=True), widget=forms.CheckboxSelectMultiple())


    class Meta:
        model = Config
        fields = ('SKU','model','variant','color','quantity','tank')

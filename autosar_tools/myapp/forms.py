from django import forms
from django.forms import formset_factory

class UploadForm(forms.Form):
    file = forms.FileField(
                    widget=forms.FileInput(attrs={
                        'class': 'custom-file-input',
                    }),)

class FrameForm(forms.Form):
    name = forms.CharField(
                    max_length=100,
                    widget=forms.TextInput(attrs={
                        'type':'text',
                    	'class': 'form-control verify-if-change',
                        'placeholder': 'Name',
                        'aria-required' : 'true',
                        'data-bv-notempty' : 'true',
                        'required data-bv-notempty-message':'Required',
                        # 'oninput' : 'inputChanged()',
                    }))
    cyclicity = forms.FloatField(
                    widget=forms.NumberInput(attrs={
                    	'class': 'form-control',
                        'placeholder': 'Cyclicity', 'step': "0.001",
                        'required data-bv-notempty-message':'Required',
                    }),
                    min_value=0)

FrameFormSet = formset_factory(FrameForm)

class GenerateCForm(forms.Form):
    floating_point_numbers = forms.BooleanField(
                    widget=forms.CheckboxInput(attrs={
                        'type':'checkbox',
                        'checked':'',
                    }))
    bit_fields = forms.BooleanField(
                    widget=forms.CheckboxInput(attrs={
                        'type':'checkbox',
                        'checked':'',
                    }))
    generate_fuzzer = forms.BooleanField(
                    widget=forms.CheckboxInput(attrs={
                        'type':'checkbox',
                        'checked':'',
                    }))


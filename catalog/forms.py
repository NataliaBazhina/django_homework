from django import forms
from django.forms import BooleanField

from catalog.models import Product, Version

class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field, in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'


    def clean_product_name(self):
        cleaned_data = self.cleaned_data['product_name']

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                          'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Данное название не подходит')

        return cleaned_data

    def clean_product_description(self):
        cleaned_data = self.cleaned_data['product_description']

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                          'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Данное описание не подходит')

        return cleaned_data

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = ('version_number', 'name', 'version_flag')


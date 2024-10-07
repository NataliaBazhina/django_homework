from django.forms import ModelForm, forms

from catalog.models import Product


class ProductForm(ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def clean_first_name(self):
        cleaned_data = self.cleaned_data['product_name']

        forbidden_words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                          'радар']

        for word in forbidden_words:
            if word in cleaned_data:
                raise forms.ValidationError('Данное название не подходит')

        return cleaned_data
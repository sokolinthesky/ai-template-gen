from django import forms
from .models import Category, Item


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'New Category'})
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'value']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'New Item'}),
            'value': forms.TextInput(attrs={'placeholder': 'Value'})
        }

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)
        # Customize the description field to be a larger textarea
        self.fields['value'].widget = forms.Textarea(attrs={
            'class': 'form-control',
            'style': 'width: 100%; height: 100px;'
        })

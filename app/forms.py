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
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'New Item'})
        }
from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label='', widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Ваше имя', 'required': True
        })
    )
    contact_info = forms.CharField(
        label='', widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Ваш Email или номер телефона', 'required': True
        })
    )
    content = forms.CharField(
        label='', widget=forms.Textarea(attrs={
            'class': 'form-control', 'placeholder': 'Текст сообщения', 'required': True, 'rows': 9
        })
    )

    class Meta:
        model = Contact
        fields = ['name', 'contact_info', 'content']

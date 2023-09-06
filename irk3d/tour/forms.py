from django import forms
from .models import Contact
from django.core.validators import EmailValidator, RegexValidator
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    name = forms.CharField(
        label='', widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Ваше имя', 'required': True
        })
    )
    contact_info = forms.CharField(
        label='', widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Ваш Email или номер телефона', 'required': True
        }),
    )
    content = forms.CharField(
        label='', widget=forms.Textarea(attrs={
            'class': 'form-control', 'placeholder': 'Текст сообщения', 'required': True, 'rows': 9
        })
    )

    class Meta:
        model = Contact
        fields = ['name', 'contact_info', 'content']

    def clean_contact_info(self):
        data = self.cleaned_data['contact_info']
        email_validator = EmailValidator()
        phone_validator = RegexValidator(regex=r'^\+?8?1?(-?\d){6,15}$')

        try:
            email_validator(data)
        except ValidationError as e:
            try:
                phone_validator(data)
            except ValidationError as e:
                raise ValidationError("Напишите действительный адрес электронной почты или номер телефона(начиная с 8 или +7, или городской. без пробелов)")

        return data

from django import forms
from .models import Contact
from django.core.validators import EmailValidator, RegexValidator, URLValidator
from django.core.exceptions import ValidationError
from re import search

STOP_WORDS = ('http', '.com', '.ua', '.ru', 'базы')


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
                raise ValidationError(
                    "Напишите действительный адрес электронной почты или номер телефона(начиная с 8/+7/7 "
                    "или городской. без пробелов)"
                )
        return data

    def clean_content(self):
        data = self.cleaned_data['content']

        for stop_word in STOP_WORDS:
            if stop_word in data:
                raise ValidationError("Сообщение не должно содержать ссылки")
        if not bool(search(r'[а-яА-Я]', data)):
            raise ValidationError("STOP SPAM!")

        return data

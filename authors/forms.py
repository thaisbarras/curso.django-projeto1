#from django.forms import Form, ModelForm
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        #alterando labels
        labels={
            'password': 'Digite sua senha',
        }

        #
        help_texts = {
            'email': 'O email precisa ser válido'
        }

        #
        error_messages = {
            'username': {
                'required': 'Este campo não pode ser deixado em branco',
                'max_length': "Este campo deve possuir mais de 3 caracteres",
                #geral
                'invalid': 'This fiels is invalid'
            }
        }

        #
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Insira o username aqui'
                #pode alterar classes por aqui
                #'class': 'input text-input outra-coisa'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira sua senha aqui'
            })
        }
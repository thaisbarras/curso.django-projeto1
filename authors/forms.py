#from django.forms import Form, ModelForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


class RegisterForm(forms.ModelForm):
    # Utilizando o inicializados para adicionar ao invez de substituir atributo dos campos
    # A vantagem é não estar sobreescrevend e sim adicionando coisas ao Widget qie já existe (por padrão)
    def __init__(self, *args, **kwars):
        super().__init__(*args, **kwars)
        self.fields['username'].widget.attrs['placeholder'] = 'Ex.: thaisbarras'

        # fazendo o mesmo, porém utulizando uma função para simplificar
        add_placeholder(self.fields['email'], 'Ex.: thaisbarras@example.com')
        add_placeholder(self.fields['first_name'], 'Ex.: Thaís')
        add_placeholder(self.fields['last_name'], 'Ex.: Barras')
        add_attr(self.fields['username'], 'css', 'a-css-class')


    # sobrescrevendo campo sem usar classe Mets
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
          }),
        error_messages={
            'required': 'Este campo não deve ficar em branco'
        },
        help_text=(
            'A senha deve conter pelo menos uma letra maiúscula,'
            'uma letra minúscula e um número. O tamanho deve ser maior que 8 caracteres'
        )
    )

    # Criando um novo campo
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirme sua senha'
          })
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        # alterando labels
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
                # geral
                'invalid': 'This fiels is invalid'
            }
        }

        #
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Insira o username aqui'
                # pode alterar classes por aqui
                # class': 'input text-input outra-coisa'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Insira sua senha aqui'
            })
        }

    # validando um campo em específico
    # Sempre utiliza clean_nomedocampo
    def clean_password(self):
        # pegando dados do formulário
        # self.data pega os dados crus do formulário, assim como eles vêm do BD
        # self.cleaned_data são os campos já tratados pelo Django
        data = self.cleaned_data.get("password")

        if 'atenção' in data:
            raise ValidationError(
                'Não digite %(value)s na senha',
                code='invalid',
                params={'value': '"atenção"'}
            )

        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')

        if 'John Doe' in data:
            raise ValidationError(
                'Não digite %(value)s no campo first name',
                code='invalid',
                params={'value': '"John Doe"'}
            )

        return data
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout #Verificar autenticação no Django
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import RegisterForm, LoginForm



def register_view(request):
    #request.session['number'] = request.session.get('number') or 1
    #request.session['number'] += 1
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form,
        'form_action': reverse('authors:register_create'),
    })

def register_create(request):
    if not request.POST:
        raise Http404()
    
    POST = request.POST
    request.session['register_form_data'] = POST
    
    form = RegisterForm(request.POST)

    if form.is_valid():
        #pegando a instância do model e não salvo no bd
        user = form.save(commit=False)

        #salvar password criptografado na base de dados
        user.set_password(user.password)

        # Agora sim salvo na base de dados
        user.save()
        messages.success(request, 'Seu usuário foi criado com sucesso, por favor, faça seu login')
        
        #limpar sessão
        #del() detela a chave de um dicionário
        del(request.session['register_form_data'])
        return redirect(reverse('authors:login'))

        
        
        #FInge que salvou os dados, mas só pega os dados
        #isso é comum quando, depois que tudo foi validado, se quer enviar mais algum valor para o formulário
        #form = form.save(commit)
        #data.outro_campo = 'outro_valor'



    return redirect('authors:register') #GET

def login_view(request):
    form = LoginForm()

    return render(request, 'authors/pages/login.html',{
        'form': form,
        'form_action': reverse('authors:login_create')
    })

def login_create(request):
    if not request.POST:
        raise Http404()
    
    form = LoginForm(request.POST)
    login_url = reverse('authors:login')

    if form.is_valid():
        authenticated_user = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticated_user is not None:
            messages.success(request, 'Your are logged in.')
            login(request, authenticated_user)
        else:
            messages.error(request, 'Invalid credentials')
    else:
        messages.error(request, 'Invalid username or password')

    return redirect(login_url)

#LOGOUT SIMPLES
#@login_required(login_url='authors:login', redirect_field_name='next')
#def logout_view(request):
#    logout(request)
#    return redirect(reverse('authors:login'))


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request):
    if not request.POST:
        return redirect(reverse('authors:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('authors:login'))

    logout(request)
    return redirect(reverse('authors:login'))
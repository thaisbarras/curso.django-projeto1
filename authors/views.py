from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages

from .forms import RegisterForm

def register_view(request):
    #request.session['number'] = request.session.get('number') or 1
    #request.session['number'] += 1
    register_form_data = request.session.get('register_form_data', None)
    form = RegisterForm(register_form_data)
    return render(request, 'authors/pages/register_view.html', {
        'form': form
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

        
        
        #FInge que salvou os dados, mas só pega os dados
        #isso é comum quando, depois que tudo foi validado, se quer enviar mais algum valor para o formulário
        #form = form.save(commit)
        #data.outro_campo = 'outro_valor'



    return redirect('authors:register') #GET
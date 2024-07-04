from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password







@api_view(['GET']) # aqui significa que a gente vai dizer que a função api_view só aceita o método get, definimos dessa maneira, colocando o get em uma lista.
# OBS: usar o interpretador da sua venv (ctrl + shift + p > python selector interpreter > python 3.10.. (venv:venv) )
def get_users(request):

    if request.method == 'GET':

        users = User.objects.all()                          # Pega todos os objetos da tabela Users do banco de dados e retorna um queryset (que é uma lista de objetos)

        serializer = UserSerializer(users, many=True)       # Serialize converte um objeto em Json (many(parâmetro) - porque são vários objeto (queryset))

        return Response(serializer.data)                    # retorna o serialized data (objeto convertido em xml ou json)
    
    return Response(status=status.HTTP_400_BAD_REQUEST)     # se tentar retornar algo diferente de um Get, retorna o erro 400.



@api_view(['GET', 'PUT'])
def get_by_nick(request, nick):

    try: # tenta pegar o User pela primary key "nick"
        user = User.objects.get(pk=nick)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND) # se não encontrar, retornar o erro 404

    if request.method == 'GET':

        serializer = UserSerializer(user) # pega o json com a informação do 'user
        return Response(serializer.data) # retorna os dados serializados

    if request.method == 'PUT': # atualizando usuário por urs

        serializer = UserSerializer(user, data=request.data) # vai pegar o "user" pela url, e passar para "data=request.data".

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(status=status.HTTP_400_BAD_REQUEST)




# Criação do Crud ---------
@api_view(['GET','POST','PUT','DELETE']) # o put e post é o que método que faz aparecer aqueles campos para escrever texto na api
def user_manager(request):

# ACESSOS

    if request.method == 'GET': # verifica se o request usa o método 'GET'

        try:
            if request.GET['user']:                         # Verifica se há um parâmetro chamado 'user' (/?user=xxxx&...)

                user_nickname = request.GET['user']         # se existir, pegar o user_nickname (está usando essa variável porque é a primary key)

                try:
                    user = User.objects.get(pk=user_nickname)   # Tenta pegar o objeto do banco de dados
                except:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                serializer = UserSerializer(user)           # Serialize(transforma) o objeto em um json
                return Response(serializer.data)            # Returna a informação em json
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    

# CRIANDO DADOS

    if request.method == 'POST':

        new_user = request.data
        
        serializer = UserSerializer(data=new_user)

        if serializer.is_valid(): # is_valid é um método que verifica que os dados são válidos
            serializer.save() # se sim, atribui esses dados e salva no banco de dados
            return Response(serializer.data, status=status.HTTP_201_CREATED) # retorna o próprio objeto, e o status http 201 created, que é o código confirmando a crianção dos dados no banco de dados.
            # isso é útiu para verificar se o usuário está tentando criar um nick que é igual a ao nick de outro usuário já cadastrado.
        return Response(status=status.HTTP_400_BAD_REQUEST) # se os dados não forem válidos, retorna o bad request

#def new(request):
#    return render(request, 'user/user_password', {'form': SenhaUser})

#def create(request):
#    forms = SenhaUser(request.POST)
#    if not forms.is_valid():
#        return render(request, 'user/user_password', {'form': SenhaUser})
#    
#    c = forms.save(commit=False)
#    c.senha = make_password(c.senha)
#    c.save()
#    return HttpResponseRedirect('/')
#'''

# EDITAR DADOS (PUT)

    if request.method == 'PUT':

        nickname = request.data['user_nickname'] # pega os dados do request buscando por "user_nickname(PK)"

        try:
            updated_user = User.objects.get(pk=nickname) # o request pega o dado pelo user_nckname, e recebe a atualização desses dados ligados a PK.
        except:                                          # e retorna um dicionário, assim podendo acessar os parâmetros jason dele.
            return Response(status=status.HTTP_404_NOT_FOUND) # se o usuário tentar modificar a chave primária(o que não pode), retorna erro 404, dizendo que o parâmetro que está querendo ser auterado não existe.
            # OBS: e também, ele usa a PK como parâmetro chave do request, por isso não pode ser alterado.
        

        serializer = UserSerializer(updated_user, data=request.data) # o serializaer vai pegar o novo objeto "updated_user" e colocar no esses novos dados no "data-request.data"

        if serializer.is_valid(): # vai verificar se é valido
            serializer.save() # se sim, salva os dados
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) # retorna os dados atualizados
        
        return Response(status=status.HTTP_400_BAD_REQUEST) # se não for válido, retorna erro 400.




# DELETAR DADOS (DELETE)

    if request.method == 'DELETE':

        try:
            user_to_delete = User.objects.get(pk=request.data['user_nickname'])
            user_to_delete.delete()
            return Response(status=status.HTTP_202_ACCEPTED)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)




































# OBS: O NICKNAME É A PRIMARY KEY, SE EDITAR ELA, A API IRÁ CRIAR OUTRO DADO, PORQUE NÃO EXISTE PRIMARYKEY IGUAL. 
# SE ISSO ACONTECER, VAI SER COMO SE ESTIVESSE DANDO UM POST E CRIANDO OUTRO DADO COM O NICKNAME DIFERENTE, PORÉM, COM AS OUTRAS INFORMAÇÕES IGUAL AO OUTRO DADO.










# def databaseEmDjango():

#     data = User.objects.get(pk='breno_drc')          # OBJETO - pk=primary key (pega esse valor do vanco de dados)

#     data = User.objects.filter(user_age='25')           # QUERYSET - filtro de dados (filtra e pega todos os dados que tem 'age=25'), como esse filtro retorna mais de um objeto, ele se torna um QUERYSET

#     data = User.objects.exclude(user_age='25')          # QUERYSET - é parecido com o filtro, só que ele vai retornar todos os objetos que não possuem um parâmetro pedido.(exemplo, ele vai retornar todos os objeto em que a idade não é 25 (age='25'))

#     data.save() # salva o objetos

#     data.delete() # deleta os objetos



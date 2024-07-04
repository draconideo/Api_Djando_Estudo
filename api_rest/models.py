from django.db import models
from django import forms # método para criar um hash na senha (mudar o número por asterisco)

# aplicação de cadastro de usuário
# aqui, criamos as tabelas do bando de dados, como se fosse um CREATE do SQL.

class User(models.Model):
    
    user_nickname = models.CharField(primary_key=True, max_length=100, default='') #default, é um valor que precisamos definir, mesmo que seja somente um espaço vazio, para não dar algum erro.
    user_name = models.CharField(max_length=150, default='')
    user_email = models.EmailField(default='')
    user_age = models.IntegerField(default=0)
    #user_password = forms.CharField(max_length=16, blank=False, null=False, widget=forms.PasswordInput) # senha de no máximo 16 caracteres, não pode deixar em branco.

    

    def __str__(self): #método mágico do python.
        return f'Name: {self.user_name} | E-mail: {self.user_email}'
    # método mágico, porque quando formos printar a classe, ele vai chamar por padrão essa função, mesmo que a gente não chame a função, que vai estar
    # retornando a string -> f'Nickname: {self.user_nickname} | E-mail: {self.user_email}'

class SenhaUser(forms.ModelForm):
        user_password = forms.CharField(widget=forms.PasswordInput)
        class Meta:
            model = User
            fields = '__all__'



#class UserTasks(models.Model):
#   user_nickname = models.CharField(max_length=100, default='')
#   user_task = models.CharField(max_length=255, default='')



# OBS: os dados são Key sensitive.
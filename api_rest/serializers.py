# O serializer é o que vai transmitir os dados para o front end depois do tratamento.

from rest_framework import serializers

from .models import User
#o ponto em models, significa que o arquivo models está na mesma pasta, e o ponto é um comando que indica exatamente para pegar o arquivo da mesma pasta.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

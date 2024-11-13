from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User

class SnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = ['id', 'title', 'code', 'linenos', 'language', 'style']
class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all(), required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'snippets']

    def create(self, validated_data):
        snippets_data = validated_data.pop('snippets', [])
        user = User.objects.create(**validated_data)
        user.snippets.set(snippets_data)
        return user
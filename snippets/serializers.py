from rest_framework import serializers
from .models import Snippet
from django.contrib.auth.models import User

class SnippetSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')
    class Meta:
        model = Snippet
        fields = ['url', 'id', 'highlight', 'owner',
                 'title', 'code', 'linenos', 'language', 'style']
class UserSerializer(serializers.ModelSerializer):

    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'snippets']

    def create(self, validated_data):
        snippets_data = validated_data.pop('snippets', [])
        user = User.objects.create(**validated_data)
        user.snippets.set(snippets_data)
        return user
from rest_framework import generics, permissions, renderers, viewsets
from .models import Snippet
from django.contrib.auth.models import User
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django_filters import rest_framework as filters
from .filters import SnippetFilter


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
       'users': reverse('user-list', request=request, format=format),
       'snippets': reverse('snippet-list', request=request, format=format)
   }
)

class SnippetViewSet(viewsets.ModelViewSet):
   queryset = Snippet.objects.all()
   serializer_class = SnippetSerializer
   permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                         IsOwnerOrReadOnly]
   filter_backends = (filters.DjangoFilterBackend,)
   filterset_class = SnippetFilter

   @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
   def highlight(self, request, *args, **kwargs):
       snippet = self.get_object()
       return Response(snippet.highlighted)

   def perform_create(self, serializer):
       serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
   queryset = User.objects.all()
   serializer_class = UserSerializer


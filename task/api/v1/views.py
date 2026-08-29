from rest_framework import viewsets


from .paginations import DefaultPagination
from ...models import Task
from .serializers import TaskModelSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from .filters import CustomFilterBackend
from .permissions import IsOwner


class TaskModelViewSet(viewsets.ModelViewSet):

    serializer_class = TaskModelSerializer
    permission_classes = [IsOwner]
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['title','description']
    ordering_fields = ['done','created_at']
    filterset_class = CustomFilterBackend
    pagination_class = DefaultPagination
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
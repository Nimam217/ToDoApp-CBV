from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from .paginations import DefaultPagination
from ...models import Task
from .serializers import TaskModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .filters import CustomFilterBackend
from .permissions import IsOwner

from django.core.cache import cache

class TaskModelViewSet(viewsets.ModelViewSet):
    serializer_class = TaskModelSerializer
    permission_classes = [IsOwner]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    search_fields = ["title", "description"]
    ordering_fields = ["done", "created_at"]
    filterset_class = CustomFilterBackend
    pagination_class = DefaultPagination

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):

        query_params = request.GET.urlencode()

        cache_key = f"task_list:{request.user.id}:{query_params}"

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return Response(cached_data)

        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            response = self.get_paginated_response(serializer.data)

            cache.set(
                cache_key,
                response.data,
                10 * 60,
            )

            return response

        serializer = self.get_serializer(queryset, many=True)

        cache.set(
            cache_key,
            serializer.data,
            10 * 60,
        )

        return Response(serializer.data)


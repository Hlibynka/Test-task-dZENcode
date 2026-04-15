from django.shortcuts import render
from rest_framework import viewsets
from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(parent__isnull=True)

        # Sorting
        sort_by = self.request.query_params.get('sort_by', '-created_at')
        allowed_sort_fields = [
            'user_name', '-user_name',
            'email', '-email',
            'created_at', '-created_at'
        ]

        if sort_by in allowed_sort_fields:
            queryset = queryset.order_by(sort_by)

        return queryset

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from .tasks import process_new_comment_task
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import status
from captcha.models import CaptchaStore
from captcha.helpers import captcha_image_url
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from .models import Comment
from .serializers import CommentSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


@api_view(['GET'])
def get_captcha(request):
    hashkey = CaptchaStore.generate_key()
    image_url = captcha_image_url(hashkey)
    return Response({
        'captcha_key': hashkey,
        'captcha_image': request.build_absolute_uri(image_url)
    })

class CommentPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['user_name', 'email', 'created_at']
    ordering = ['-created_at']
    permission_classes = [IsAuthenticatedOrReadOnly]

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        captcha_key = request.data.get('captcha_key')
        captcha_value = request.data.get('captcha_value', '')

        # captcha check
        try:
            captcha = CaptchaStore.objects.get(hashkey=captcha_key, response=captcha_value.lower())
            captcha.delete()  # true - delete key
        except CaptchaStore.DoesNotExist:
            return Response({'captcha': ['Невірно введена CAPTCHA']}, status=status.HTTP_400_BAD_REQUEST)


        response = super().create(request, *args, **kwargs)
        cache.clear()
        process_new_comment_task.delay(response.data['id'])
        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            'comments_group',
            {
                'type': 'new_comment',
                'message': 'Оновіть список',
                'comment_id': response.data['id']
            }
        )

        return response

import bleach
from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'user_name', 'email', 'home_page', 'text',
            'created_at', 'image', 'txt_file', 'parent', 'replies'
        ]

    def get_replies(self, obj):
        children = obj.get_children()
        if children.exists():
            return CommentSerializer(children, many=True).data
        return []

    def validate_text(self, value):
        allowed_tags = ['a', 'code', 'i', 'strong']
        allowed_attrs = {'a': ['href', 'title']}

        cleaned_text = bleach.clean(
            value,
            tags=allowed_tags,
            attributes=allowed_attrs,
            strip=True
        )
        return cleaned_text

    def validate_txt_file(self, value):
        if value:
            if not value.name.lower().endswith('.txt'):
                raise serializers.ValidationError("Дозволено лише файли формату TXT.")

            if value.size > 100 * 1024:
                raise serializers.ValidationError("Розмір текстового файлу не повинен перевищувати 100 КБ.")
        return value

    def validate_image(self, value):
        if value:
            valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
            ext = value.name.split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Дозволені лише формати JPG, GIF, PNG.")
        return value
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Comment(MPTTModel):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    # Files
    image = models.ImageField(upload_to='comments_images/', blank=True, null=True)
    txt_file = models.FileField(upload_to='comments_files/', blank=True, null=True)

    # Cascade field
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['-created_at'] # LIFO

    def __str__(self):
        return f"Comment by {self.user_name} at {self.created_at}"
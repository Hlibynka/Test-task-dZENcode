from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys


class Comment(MPTTModel):
    user_name = models.CharField(max_length=100)
    email = models.EmailField()
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    image = models.ImageField(upload_to='comments_images/', blank=True, null=True)
    txt_file = models.FileField(upload_to='comments_files/', blank=True, null=True)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    class MPTTMeta:
        order_insertion_by = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user_name} at {self.created_at}"

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

            if img.width > 320 or img.height > 240:
                output_size = (320, 240)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)

                output = BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(output, format=img_format)
                output.seek(0)

                self.image = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    self.image.name,
                    f'image/{img_format.lower()}',
                    sys.getsizeof(output),
                    None
                )

        super().save(*args, **kwargs)
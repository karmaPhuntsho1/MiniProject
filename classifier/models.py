from django.db import models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    prediction = models.CharField(max_length=100, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prediction} - {self.uploaded_at}" 
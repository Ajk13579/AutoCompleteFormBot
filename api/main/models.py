from django.db import models


class CompletedTaskPicture(models.Model):
    user_id = models.CharField(max_length=200)
    path_for_picture = models.CharField(max_length=200)

from django.db import models


class CompletedTaskPicture(models.Model):
    task_id = models.CharField(max_length=36)
    path_for_picture = models.CharField(max_length=200)

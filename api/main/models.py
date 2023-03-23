from django.db import models


class CompletedTaskPicture(models.Model):
    STATUS_CHOICES = (
        (0, "Executed"),
        (1, "Done")
    )

    user_id = models.CharField(max_length=200, blank=True, null=True)
    path_for_picture = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default=0,
    )

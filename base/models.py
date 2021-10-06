from django.db import models
from django.contrib.auth.models import User # user model takes care of user functions, like username, email, password
# Create your models here.

#Task model
class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) #On delete = if a user is deleted all the data related to the user will be gone too. Null=true, means there can be an empty field
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False) #default false because when a item is created its not going to be complete
    created = models.DateTimeField(auto_now_add=True) #automatically set the tasks creation time

    def __str__(self):
        return self.title
    #order the task lisk by completed tasks, completed tasks are sent to the bottom of the list
    class Meta:
        ordering = ["complete"]
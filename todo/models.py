from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
	title = models.CharField(max_length=100, verbose_name='Title')
	memo = models.TextField(blank=True, verbose_name='Description')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Created')
	datecomplited = models.DateTimeField(null=True, blank=True, verbose_name='Complited')
	important = models.BooleanField(default=False, verbose_name='Important')
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

from django.contrib import admin
from .models import Todo



class TodoAdmin(admin.ModelAdmin):
	'''
	Класс для отображения поля created на странице администратора
	'''
	
	readonly_fields = ('created', )
	


admin.site.register(Todo, TodoAdmin)

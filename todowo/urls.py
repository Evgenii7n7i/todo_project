"""todowo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from todo import views


urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    # Страница регистрации
    path('signup/', views.signupuser, name='signupuser'),
    # Страница выхода пользователя
    path('logout/', views.logoutuser, name='logoutuser'),
    # Страница входа пользователя
    path('login/', views.loginuser, name='loginuser'),


    # Todo
    # Домашняя страница
    path('', views.home , name='home'),
    # Страница создания задания
    path('create/', views.createtodo, name='createtodo'),
    # Страница просмотра заданий пользователя
    path('current/', views.currenttodos, name='currenttodos'),
    # Страница просмотра завершённых задач
    path('completed/', views.completedtodos, name='completedtodos'),
    # Страница просмотра и изменения заданий пользователя
    path('todo/<int:todo_pk>', views.viewtodo, name='viewtodo'),
    # Путь(не страница, просто ссылка на функцию), для завершения задания пользователя
    path('todo/<int:todo_pk>/complete>', views.completetodo, name='completetodo'),
    # Путь (не страница, просто ссылка на функцию), для удаления записи пользователя
    path('todo/<int:todo_pk>/delete>', views.deletetodo, name='deletetodo'),
]
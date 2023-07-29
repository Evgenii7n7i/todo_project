from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
# Импорт декоратора который позволит доступ к функциям только 
# зарегистрированным пользователям
from django.contrib.auth.decorators import login_required


def home(request):
    '''
    Функция домашней страницы
    '''
    title = 'Домашняя страница'
    return render(request, 'todo/home.html', {'title': title})


def signupuser(request):
    '''
    Функция регистрации пользователя
    '''

    title = 'Регистрация'
	# Если запрос гет то:
    
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm, 'title': title})

    else:
    	# Если запрос пост, то:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')

            except IntegrityError:
            	return render(request, 'todo/signupuser.html', {'form': UserCreationForm(), 'error': 'Пользователь с таким именем уже существует!'})
        else:
            # Если пароли не совпадут, то:
            return render(request, 'todo/signupuser.html', 
	    	{'form': UserCreationForm(), 'error': 'Пароли не совпадают', 'title': title})



def loginuser(request):
    '''
    Функция входа пользователя
    '''

    title = 'Вход'
    # Если запрос гет то:
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', 
            {'form': AuthenticationForm(), 'title': title})

    else:
        # Если запрос пост, то:
        user = authenticate(request, username=request.POST['username'],
            password=request.POST['password'])
        
        # Если пользователь не определён:
        if user is None:
            return render(request, 'todo/loginuser.html', {'form': AuthenticationForm(), 'error': 'User and pass did not', 'title': title})
        
        # Если пользователь определён:
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    '''
    Функция выхода пользователя
    '''

    if request.method == 'POST':
        logout(request)
        return redirect('home')



@login_required
def createtodo(request):
    '''
    Функция для отображения модели на сайте 
    '''

    title = 'Добавить задание'
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'title': title})

    else:
        try:
            form = TodoForm(request.POST)

            # Данная форма сохраняет все данные введеные пользователем в БД
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', 
                {'form': TodoForm(), 'error': 'Превышено допустимое количество символов!', 'title': title})


@login_required
def currenttodos(request):
    '''
    Функция страницы пользователя:

    user=request.user - позволяет показывать данные из бд которые относятся непосредственно
    к пользователю
    datecomplited__isnull=True - убирает запись на странице сайта если дата окончания задания установлена
    '''

    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=True)
    title = 'Мои задания'
    context = {'todos': todos, 'title': title}
    return render(request, 'todo/currenttodos.html', context)


@login_required
def completedtodos(request):
    '''
    Функция страницы пользователя которая отображает завершённые задачи:

    user=request.user - позволяет показывать данные из бд которые относятся непосредственно
    к пользователю
    datecomplited__isnull=False - добавляет запись на странице сайта если дата окончания задания установлена
    '''

    todos = Todo.objects.filter(user=request.user, datecomplited__isnull=False).order_by('-datecomplited')
    title = 'Завершённые зачачи'
    context = {'todos': todos, 'title': title}
    return render(request, 'todo/completedtodos.html', context)    


@login_required
def viewtodo(request, todo_pk):
    '''
    Функция отображения и изменения динамиеских страниц пользователя :

    instance=todo - эта строка даёт понять что мы не создаём новую запись, 
    а только изменяем существующую.
    user=request.user - проверка на соответствия текущего пользователя и записи.
    Пользователь не сможет смотреть чужие записи путем адресной строки браузера
    '''
    
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    title = 'Текущее задание'

    if request.method == 'GET':
        form = TodoForm(instance=todo)
        context = {'todo': todo, 'form': form, 'title': title}
        return render(request, 'todo/viewtodo.html', context)

    else:
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            error = 'Информация введена не корректно!!!'
            context = {'todo': todo, 'error': error, 'form': form, 'title': title}
            return render(request, 'todo/viewtodo.html', context)


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecomplited = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')

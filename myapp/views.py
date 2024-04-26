from datetime import date, datetime, timedelta
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from taskmanager.settings import DEFAULT_FROM_EMAIL
from .forms import TaskForm, CategoryForm, TaskFormEdit
from .models import Task, Category
from .sevices import redirect_to_previous_page


def index(request):
    return render(request, 'myapp/index.html')



"""Вариант-1,Функция вывода списка задач БЕЗ ФИЛЬТРА"""

# @login_required
# def list_tasks(request):
#     # tasks = Task.objects.all()
#     tasks = Task.objects.filter(user=request.user)
#     return render(request, 'myapp/task/list_tasks.html', {'tasks': tasks})

"""Вариант-1,Функция вывода списка задач С ФИЛЬТРАМИ"""


@login_required  # декоратор разрешает доступ к вюхе только для авторизированных пользователей
def list_tasks(request):
    # Получаем параметры фильтрации из GET-запроса из фильтра
    category_id = request.GET.get('category')
    if category_id:
        try:
            category_id = int(category_id)
        except (ValueError, TypeError):
            pass
    status = request.GET.get('status')
    due_date = request.GET.get('due_date')
    priority = request.GET.get('priority')
    query = request.GET.get('query')  # Получаем поисковый запрос из GET-параметров

    reset = request.GET.get('reset')

    if reset == "true":
        # Выполнить сброс значений фильтров на исходные или пустые значения
        category_id = None
        status = None
        due_date = None
        priority = None
    # Формируем базовый QuerySet для задач для текущего
    # пользователя
    tasks = Task.objects.filter(user=request.user)
    categories = Category.objects.filter(user=request.user)

    if query:
        # Фильтруем задачи по совпадающим словам в поле description
        tasks = tasks.filter(Q(description__icontains=query) | Q(description__icontains=query.capitalize()))

    # Применяем фильтрацию по категории, если указана,
    # то есть если 'category_id' не равняеться NONE или пустой строки

    if category_id:
        tasks = tasks.filter(category_id=category_id)

    # Применяем фильтрацию по статусу, если указан
    if status:
        tasks = tasks.filter(completed=(status == 'Выполнено'))  # вывод результата фильтрации в зависимости
        # если условие равно TRUE или FALSE
    # Применяем фильтрацию по сроку выполнения, если указан
    if due_date:
        if due_date == 'Просроченные':
            tasks = tasks.filter(due_date__lt=datetime.now())
        elif due_date == 'Сегодня':
            tasks = tasks.filter(due_date=date.today())
        elif due_date == 'Не просроченные':
            tasks = tasks.filter(due_date__gt=date.today())

    # Применяем фильтрацию по приоритету, если указан
    if priority:
        if priority == 'высокий':
            tasks = tasks.filter(priority='высокий')
        elif priority == 'средний':
            tasks = tasks.filter(priority='средний')
        elif priority == 'низкий':
            tasks = tasks.filter(priority='низкий')


    # Определяем заголовок страницы в зависимости от фильтров
    # в зависимости от условия мы переапределяем постоянно переменную 'page_title'
    page_title = "Задачи"
    if category_id:
        category = Category.objects.get(id=category_id)
        page_title += f" - {category.name}"
    if status:
        page_title += f" - {status.capitalize()}"
    if due_date:
        page_title += f" - {due_date.capitalize()}"
    if priority:
        page_title += f" - {priority.capitalize()}"
    if page_title == "Задачи":
        page_title = "Все задачи"

    # Отправляем отфильтрованные задачи на страницу в контексте
    context = {
        'category_id': category_id,
        'status': status,
        'due_date': due_date,
        'priority': priority,
        'tasks': tasks,
        'categories': categories,
        'page_title': page_title
    }
    return render(request, 'myapp/task/list_tasks.html', context)


"""Вариант-1,Функция создания новой задачи"""


@login_required
def create(request):
    if request.method == 'POST':  # title: ['задача'], Например, request.POST['title'] вернет значение поля title
        form = TaskForm(request.POST,
                        user=request.user)  # user=request.user для того что бы не отображались чужие категории
        if form.is_valid():
            task = form.save(commit=False)  # не записывем сразу в базу данных
            task.user = request.user  # присваеваем новой задачи пользователя
            task.save()
            # messages.success(request, 'Задача успешно создана.')
            return redirect('list')
    else:
        form = TaskForm(user=request.user)
    return render(request, 'myapp/task/form_task.html', {'form': form})


"""Вариант-1,Функция редактирования задачи"""


@login_required
def edit(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        form = TaskFormEdit(request.POST, user=request.user, instance=task)
        # Здесь также используется user=request.user, чтобы форма -
        # -отображала только категории, принадлежащие текущему пользователю.
        # instance=task вставляем данные выбраной задачи в форму

        if form.is_valid():
            form.save()
            # messages.success(request, 'Задача успешно изменена.')
            return redirect('list')  # или так return redirect('/tasks/')
    else:
        form = TaskFormEdit(user=request.user, instance=task)
    return render(request, 'myapp/task/edit_task.html', {'form': form, 'task': task})


"""Вариант-1,Функция удаления задачи"""


@login_required
def delete(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    # messages.success(request, 'Задача удалена')
    return redirect_to_previous_page(request)


"""Вариант-2,Класс для вывода списка задач, на базе готового класса ListView без фильтров"""
# class TaskListView(ListView):
#     model = Task
#     template_name = 'myapp/task/list_tasks.html'
#     context_object_name = 'tasks'


"""Вариант-2,Класс для создания новой задачи, на базе готового класса CreateView"""
# class TaskCreateView(CreateView):
#     template_name = 'myapp/task/form_task.html'
#     success_url = '/tasks/' # или reverse_lazy('list')
#     form_class = TaskForm

"""Вариант-2,Класс для редактирования задачи, на базе готового класса UpdateView"""
# class TaskUpdateView(UpdateView):
#     template_name = 'myapp/task/edit_task.html'
#     success_url = '/tasks/' # или reverse_lazy('list')
#     form_class = TaskForm


"""Вариант-3,Класс для вывода списка задач, на базе класса View"""
# class TaskListView(View):
#     def get(self, request):
#         tasks = Task.objects.all()
#         return render(request, 'myapp/task/list_tasks.html', {'tasks': tasks})


"""Функция переключения статуса задачи"""


def toggle_status(request, id_task):
    task = get_object_or_404(Task, id=id_task)  # или так: task = Task.objects.get(id=id_task)
    task.completed = not task.completed
    task.save()
    return redirect_to_previous_page(request)
    # используем свою функцию из файла sevises.py  для перенаправляем на текущий адрес
        # что бы при смене статуса находясь в определенной категории задач
        # не перенаправлялось на общий список


"""Функция создания новой категории задач"""


@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            # messages.success(request, 'Категория успешно создана.')
            return redirect('list_categories')
    else:
        form = CategoryForm()
    return render(request, 'myapp/task/form_category.html', {'form': form})


"""Функция удаления категории задач"""


@login_required
def delete_category(request, id_category):
    category = get_object_or_404(Category, id=id_category)
    category.delete()
    # messages.success(request, 'Категория успешно удалена.')
    return redirect('list_categories')


"""Функция вывода списка категории задач"""


@login_required
def list_categories(request):
    categories = Category.objects.filter(user=request.user)
    return render(request, 'myapp/task/list_categories.html', {'categories': categories})


"""Функция редактирования категории задач"""


@login_required
def edit_category(request, id_category):
    category = Category.objects.get(id=id_category)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            # messages.success(request, 'Категория успешно изменена.')
            return redirect('/tasks/categories/')  # или так return redirect('list_categories')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'myapp/task/edit_category.html', {'form': form, 'category': category})


"""Функция вывода списка задач по выбранной категории с фильтром"""


@login_required
def task_list_by_category(request, id_category):
    # Получаем параметры фильтрации из GET-запроса
    status = request.GET.get('status')
    due_date = request.GET.get('due_date')
    priority = request.GET.get('priority')

    reset = request.GET.get('reset')

    if reset == "true":
        # Выполнить сброс значений фильтров на исходные или пустые значения
        status = None
        due_date = None
        priority = None

    category = get_object_or_404(Category, id=id_category)
    tasks = Task.objects.filter(category=category)
    # Применяем фильтрацию по статусу, если указан
    if status:
        tasks = tasks.filter(completed=(status == 'Выполнено'))

    # Применяем фильтрацию по сроку выполнения, если указан
    if due_date:
        if due_date == 'Просроченные':
            tasks = tasks.filter(due_date__lt=datetime.now())
        elif due_date == 'Сегодня':
            tasks = tasks.filter(due_date=date.today())
        elif due_date == 'Не просроченные':
            tasks = tasks.filter(due_date__gt=date.today())

     # Применяем фильтрацию по приоритету, если указан
    if priority:
        if priority == 'высокий':
            tasks = tasks.filter(priority='высокий')
        elif priority == 'средний':
            tasks = tasks.filter(priority='средний')
        elif priority == 'низкий':
            tasks = tasks.filter(priority='низкий')

    # Определяем заголовок страницы в зависимости от фильтров
    page_title = category.name
    if status:
        page_title += f" - {status.capitalize()}"
    if due_date:
        page_title += f" - {due_date.capitalize()}"
    if priority:
        page_title += f" - {priority.capitalize()}"

        # Отправляем отфильтрованные задачи на страницу
    context = {
        'status': status,
        'due_date': due_date,
        'priority': priority,
        'tasks': tasks,
        'category': category,
        'page_title': page_title,
    }
    return render(request, 'myapp/task/list_tasks.html', context)


"""Функция отправки отправки уведомления на почту если прошел или подходит срок выполнения задачь"""


@login_required
def send_notifications(request):
    tasks_due_soon = Task.objects.filter(user=request.user, completed=False,
                                         due_date__lte=datetime.now().date() + timedelta(days=1))

    task_descriptions = []
    for task in tasks_due_soon:
        task_descriptions.append(f'--- {task.description}')

    if task_descriptions:
        subject = 'Срочно нужно выполнить следующие задания.'
        message = 'Это напоминание о том, что срок выполнения  следующих задач скоро истекает:\n\n'
        message += '\n'.join(task_descriptions)
        send_mail(subject, message, DEFAULT_FROM_EMAIL, [request.user.email])
    return render(request, 'myapp/task/notifications_sent.html')






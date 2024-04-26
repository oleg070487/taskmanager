from django.urls import path
from . import views


urlpatterns = [
    path('', views.list_tasks, name='list'),  # вариант 1 на базе функции
    path('create/', views.create, name='create'),  # вариант 1 на базе функции
    path('create-category/', views.create_category, name='create_category'),  # вариант 1 на базе функции
    path('edit/<int:pk>/', views.edit, name='edit'),  # вариант 1 на базе функции
    path('delete/<int:pk>/', views.delete, name='delete'),  # вариант 1 на базе функции
    path('status/<int:id_task>/', views.toggle_status, name='status'),
    path('categories/', views.list_categories, name='list_categories'),
    path('category-delete/<int:id_category>/', views.delete_category, name='delete_category'),
    path('edit-delete/<int:id_category>/', views.edit_category, name='edit_category'),
    path('tasks-list-by-category/<int:id_category>/', views.task_list_by_category, name='tasks_list_by_category'),
    path('send_notifications/', views.send_notifications, name='send_notifications'),# отправка вручную уведомлений о сроке

    # path('', views.TaskListView.as_view(), name='list'),  # вариант 2 на базе класса
    # path('create/', views.TaskCreateView.as_view(), name='create'),  # вариант 2 на базе класса
    # path('edit/<int:pk>/', views.TaskUpdateView.as_view(), name='edit'),  # вариант 2 на базе класса
]


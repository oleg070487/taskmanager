from django import forms
from django.forms import TextInput, Select, DateInput, Textarea

from .models import Task, Category

"""Форма по созданию новой задачи"""


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category', 'priority']

        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст задачи'
            }),
            "category": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Категория',
            }),
            "due_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Срок выполнения',
                'type': 'date',
            }),
            "priority": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Приоритет',
            }),
        }

    # Данный код позволяет установить queryset для поля category в форме
    # TaskForm на основе текущего пользователя, переданного через аргумент user.
    # Это позволяет отображать только категории, принадлежащие данному пользователю
    # при использовании новой задачи в этой форме.

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Получаем текущего пользователя из аргументов
        # при создании нового экземппляра в форме
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(user=user)


class TaskFormEdit(TaskForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category', 'priority']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Заголовок'
            }),
            "description": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текст задачи'
            }),
            "category": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Категория',
            }),
            "due_date": DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Срок выполнения',
            }),
            "priority": Select(attrs={
                'class': 'form-control',
                'placeholder': 'Приоритет',
            }),
        }


"""Форма по созданию новой категории"""


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

        widgets = {
            "name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Категория'
            })}

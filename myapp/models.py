from django.contrib.auth.models import User
from django.db import models
from django.db.models import Case, When


class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    name = models.CharField('Имя', max_length=50)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITIES = [
        ('высокий', 'Высокий'),
        ('средний', 'Средний'),
        ('низкий', 'Низкий'),
    ]

    title = models.CharField('Заголовок', max_length=100)
    description = models.TextField('Текст задания')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='tasks', verbose_name='Категория')
    create = models.DateTimeField('Создано', auto_now_add=True)
    due_date = models.DateField('Срок выполнения')
    completed = models.BooleanField('Статус выполнения', default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    priority = models.CharField('Приоритет', max_length=20, choices=PRIORITIES, default='средний')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = [
            'completed',  # Сортировка по полю completed (невыполненные задачи будут первыми)
            Case(
                When(priority='высокий', then=0),
                When(priority='средний', then=1),
                When(priority='низкий', then=2),
              ),
            'due_date'
        ]

# Generated by Django 4.2.2 on 2023-06-26 15:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Текст задания')),
                ('create', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('due_date', models.DateField(verbose_name='Срок выполнения')),
                ('completed', models.BooleanField(default=False, verbose_name='Статус выполнения')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.category', verbose_name='Категория')),
            ],
        ),
    ]

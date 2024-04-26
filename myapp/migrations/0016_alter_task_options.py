# Generated by Django 4.2.2 on 2023-07-05 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_alter_task_options_task_priority'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['completed', models.Case(models.When(priority='высокий', then=0), models.When(priority='средний', then=1), models.When(priority='низкий', then=2), default=3, output_field=models.IntegerField()), 'due_date'], 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
    ]
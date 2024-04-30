from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from .models import Task
from taskmanager.celery import app


@app.task
def schedule_notifications():
    users = User.objects.all()

    for user in users:
        tasks_due_soon = Task.objects.filter(user=user, completed=False,
                                         due_date__lte=datetime.now().date() + timedelta(days=1))

        task_descriptions = []
        for task in tasks_due_soon:
            task_descriptions.append(f'--- {task.description}')

        if task_descriptions:
            subject = 'Срочно нужно выполнить следующие задания.'
            message = 'Это напоминание о том, что срок выполнения  следующих задач скоро истекает:\n\n'
            message += '\n'.join(task_descriptions)
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])



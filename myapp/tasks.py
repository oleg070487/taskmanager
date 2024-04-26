# import schedule
# import time
#
# from django.core.mail import send_mail
# from django.conf import settings
# from django.contrib.auth.models import User
# from datetime import date
# from .models import Task
#
# def send_notifications(recipient, message):
#     subject = "Уведомление о просроченных задачах"
#     sender = settings.DEFAULT_FROM_EMAIL
#
#     try:
#         send_mail(subject, message, sender, [recipient])
#         print("Уведомление отправлено успешно!")
#     except Exception as e:
#         print("Ошибка при отправке уведомления:", str(e))
#
# def schedule_notifications():
#     users = User.objects.all()
#     today = date.today()
#
#     for user in users:
#         overdue_tasks = Task.objects.filter(due_date__lt=today, user=user)
#         if overdue_tasks:
#             message = "Просроченные задачи:\n"
#             for task in overdue_tasks:
#                 message += f"- {task.title}\n"
#
#             send_notifications(user.email, message)
#
# schedule.every().day.at("15:19", "Europe/Chisinau").do(schedule_notifications)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)
from django.shortcuts import redirect

"""Моя функция для перенаправления на предыдущию страницу"""


def redirect_to_previous_page(request, default_redirect='list'):
    # получаем текущий url aдрес
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    else:
        return redirect(default_redirect)

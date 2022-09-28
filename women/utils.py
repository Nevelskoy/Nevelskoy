from django.db.models import Count

from .models import *
from django.core.cache import cache

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_page'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        ]

class DataMixin:
    paginate_by = 5
    def get_user_context(self, **kwargs):
        context = kwargs
        cats = cache.get('cats')            # кэширование следует включать только на конечном этапе разработки, чтобы мы могли отслеживать все нагрузки, возникающие в процессе отладки
        if not cats:
            cats = Category.objects.all()
            cache.set('cats', cats, 60)
        #cats = Category.objects.annotate(Count('women')) #annotate Count - из ORM позволяет получить количество постов в данной рубрике

        # отключаем пункт меню Добавить статью, для неавторизованных пользователей
        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
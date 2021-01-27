from django import template
from django.core.cache import cache
from django.core.paginator import Paginator
from news.models import News
from news.models import Category
from django.db.models import Count, F

register = template.Library()

# можем присваивать имя тега (name=), а можем нет тогда по умолчанию будет имя функции
@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)



# наш тег который подключает шаблон html. Работает очень интересно
# в декораторе мы используем register.inclusion_tag('path/name.html'), а в аргументах
# указываем путь и имя файла
# подключаем в шаблоне данный тег как {% show_categories %}
# смотрим что происходит, при этом обращаем внимание, от какого html файла он заимствуется
@register.inclusion_tag('news/list_categories.html')
def show_categories(arg1='hello', arg2='world'):

    categories = cache.get('categories') # получаем наши категории из кэша
    # а от куда мы берем ключ categories - я хз. cache ленивый объект (см. в косоль)
    # аа, я понял, ключ мы устанавливаем сами в set(), а потом по истичении 30 с он исчезает, ша

    print(f'\n\n№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№\n'
          f'cache - {cache}'
          f'\n№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№\n\n')
    if not categories:
        # если их нет то:
        categories = Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)

    #     и кэшируем их
        cache.set('categories', categories, 30)
# Но! все эти строчки можно заменить на одну функцию get_or_set('categories',
    # Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0), 30)

    # without cache:
    # Category.objects.annotate(cnt=Count('news', filter=F('news__is_published'))).filter(cnt__gt=0)


    return {'categories': categories, 'arg1' : arg1, 'arg2': arg2}



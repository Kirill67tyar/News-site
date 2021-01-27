from django.db import models
from django.db.models import F

from django.urls import reverse

class News(models.Model):

    title = models.CharField(max_length=50, verbose_name='Наименование')
    content = models.TextField(max_length=250, blank=True, verbose_name='Контент')
    created_it = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_it = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    # в upload_to можно поместить название функции где мы опишем логику сохранения файла
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True, verbose_name='Фото')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')
    # Очень важный момент: Если мы определяем первичный класс по ForeignKey после того          # related_name='get_news'
    # как определили вторичный класс (из вторичного привязываем к первичному)
    # то имя модели мы указываем в ковычках, как в этом случае
    # Просто для более раннего этот класс еще не определен, и ему не на что ссылаться

    # PROTECT в on_delete обеспечивает защиту от удаления данных
    # т.е. категория будет защищена от удаления

    # null - делает это поле не обязательным в бд
    views = models.IntegerField(default=0)


    def my_func(self):
        return 'Hello from models News'

    def get_absolute_url(self):
        return reverse('news:view_news', kwargs={'pk': self.pk})



    def __str__(self):
        return self.title.capitalize()

    # класс Meta не только для админки, но и для всей модели.
    # При обратной сортировке News.objects.all() - будет выдавать обратную сортировку (без ordered_by('-created_it'))
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = '-created_it',


class Category(models.Model):
    #                                         db_index - устанавливает индекс поля в бд,
    #                                         что делает обращение к этому полю быстрее
    title = models.CharField(max_length=50, db_index=True,
                             verbose_name='Наименование категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = 'title',

# важно называть этот метод именно так get_absolute_url
#     позволяет нам заходить в приложение через админку (и не только)
    def get_absolute_url(self):

        return reverse('news:category', kwargs={'pk': self.pk})
# функция reverse (в django!) и тег {% url 'namespace:path_name' element.pk %}
# по сути одно и тоже. Разница - тег используется в шаблоне, а функция в коде
# есть так-же анология с функцией redirect(), куда мы кладем весь url
# и <a href="url/shoh/dog/pes/"
# а дальше загляни в list_categories.html и посмотри куда ссылается ссылка a href
# функция reverse занимается построением ссылки на основе именованного адреса (namespace:path_name)


# модель влияет на три момента:
# 1) какой тип поля будет создан в бд (CHAR, и тд)
# 2)какая форма будет в шаблоне (текстовое поле, виджет и т.д.), делается через forms
# 3) влияет на правила валидации



#                         Миграции

# миграции - можно сказать контроль версий наших моделей
# миграции не всегда могут нормально работать (я уже в этом убедился)
# лучше заранее хорошо продумывать модели, таблицы в бд,
# т.к. при связках между таблицами, и возможно в других случаях - могут быть проблемы
# так что при миграциях нужно быть аккуратным
# Лучше менять модель минимально, а в идеале вообще не менять
# Важный момент - если установка какого-либо приложения из вне требует миграции -
# то оно использует какую-то (может свою) таблицу в бд

# Почему в Django нужно первым создавать модели юзера, и аккаунты?
# При первой миграции мы создаем бд на основе User, уже встроенной в Django,
# И если мы хотим переопределить User в дальнейшем,
# Нам придется грохнуть всю бд. Безболезненно это проходит редко, и записи в бд могут пострадать



# Object relation mapping - Объектно-ориентированное отображение
# позволяет нам работать с записями в бд как с объектами python
# каждая строчка в таблице - объект экземпляра класса модели, определенной в модели
# столбики в нашей таблице - это ничто иное как аттрибуты этого класса модели

# Модели в django по умолчанию являются ленивыми

# модуль connection из django очень полезен - отображает все запросы которые делались в бд через комманду
# connection.queries
# пошабить над ним
# а функция reset_queries может очистить запросы которые были (находится в django.db)

# objects - это менеджер объектов из бд


# Оказывается, мы можем использовать методы, определенные в модели - в самом шаблоне.
# Это в принципе логично, ведь объекты в QuerySet - экземпляры класса определенной модели,
# и методы к ним тоже можно определять и использовать в модели, экземплярами коей они являются.
# Уверен, что такие методы можно использовать во вьюшках (контроллерах).
# Но не знал, что эти методы также могут вызываться в шаблоне
# Маленькая ремарка - синтаксис вызова этих методов немного другой, чем в python,
# хотя почти такой-же: просто не ставь круглые скобочки после вызова, обращайся как к аргументам,
# а так все так же

# объявляя в модели поле того или иного типа, django не только создаст поле в таблице бд,
# но и будет использовать соответствующие валидаторы, чтобы валидировать эти поля,
# перед добавлением в базу данных
# То же самое будет происходить и приеме данных из формы. Тоже будет происходить процесс валидации
# на основе типов полей
# у модельных форм есть метод save() - который будет сохранять данные в бд
# НО у экземпляров обычных форм - метода save() нет
# также у форм есть метод .is_valid()
# Формы связанные с данными - наполененные формы, и отправленные на сервер
# Формы не связанные с данными - пустые формы


# разрешение на уровне базы для поля нулевое значение - null=True
# на уровне всех форм сделать это поле необязательными - blank=True
# on_delete=models.SET_NULL - означает «если объект на который мы ссылаемся, удалили, то обнули эту связь».


#                                           ORM
# Немного про ORM
# Как обратиться из более главной модели к подчиненной (по связи ForeignKey)
# через <name_model>_set
# К примеру Category.objects.get(title='Спорт').news_set.all() - выведет в queryset все новости закрепленные за этой категорией
# Почему там стоит all()? Видимо это ленивый метод. Можно и другие методы применять к примеру count()
# Это так назывемая обратная связь
# Мы можем также переопределить наш <name_model>_set - в поле гле присваиваем подчиненному классу - главный
# по связи ForeignKey - делается это через аргумент related_name
# вспомни про related_name (см. в tasks skillfactory)

# lookup'ы используются в filter, и эквивалентны WHERE в sql запросе
# к примеру filter(pk__gte=3) это как SELECT ... WHERE id >= 3; (под вопросом, так ли в sql больше или равно)
# В документации о них  в целом понятно.
# __contains и __icontains в кириллице - чувствительны к регистру
# а для английских слов - не чувствительны
# Когда ты работаешь с sql - регистр значения не имеет, но только не с кириллицей
# с кириллицей - регистр всегда играет роль
# В doc django написано что contains чувствительна к регистру, а icontains - нет
# но на практике я разницу не выявил

# lookup __in=[]. Model.objects.filter(pk__in=[1,2,3]) Инициирует SELECT ... WHERE id IN (1,2,3)

# >>> pk = News.objects.get(pk=13)
# >>> pk
# <News: Статья из формы>
# >>> News.objects.filter(pk=pk.pk)
# <QuerySet [<News: Статья из формы>]>
# >>> News.objects.filter(pk=pk.pk).exists()
# True

# методы earliest('some_field') и latest('some_field')
# latest - выдает записи по последнему изменению поля (скорее всего date, или datetime field),
# передаваеваемого в аргумент, т.е. какие изменения были недавно
# earliest - такой же принцип, но какие изменения были максимально давно

# получить новости двух категорий - News.objects.fitler(category_pk__in=[1,3])

# методы counts() и exists() - очень быстрые, но применяются только на queryset

# очень интересная функция - get_previous_by_<date/datetime-name_field>
# где date/datetime-name_field поле datetime или date
# работает не с queryset а с экземплярами модели, с помощью нее можно получить предыдущую
# n = News.objects.get(pk=10)    n.get_previous_by_created_it - покажет, какую создали перед ней
# get_next_by_<date/datetime-name_field> - такой-же принцип, но она показывают следующую, более свежую
# более того, хоть они и работают не с queryset, но могут принимать аргументы __gte, __lte

# Как обратиться к имени вторичной модели через первичную? А также - <name_model>__<name_field>
# где <name_model> - вторичная модель


#!!! from django.db.models import Q !!!

# | - or, & - and, ~ - not
# Q - очень интересно работает
# дело в том, что у filter, когда перечисляешь аргументы через запятую по умолчанию стоит булевая операция AND
# Q позволяет поменять эту операцию на or или даже not
# News.objects.filter(Q(pk__in=[23,25]) | Q(title__contains='хз'))


# aggregation
    # annotate - как-бы позволяет определить, какую переменную подсчета ты будешь использовать
    # Аггрегатные вычисления затрагивают значение определенного поля всех записей, и получают одно,
    # к примеру Min() - минимальное значение, Avg() - среднее арифметическое

# News.objects.aggregate(Max('views'), Min('views'))
# Выдаст значение минимального числа views и максимального числа views
# {'views__min': 0, 'views__max': 5445}
# обрати внимание, как создается ключ в словаре (имя поля, и имя функции)
# фокус покус, если передать в News.objects.aggregate(lol=Max('views'), kek=Min('views'))
# то в ответе создастся словарь со значениями lol и kek {'lol': 5445, 'kek': 0}
# можно их даже вычитать News.objects.aggregate(difference=Max('views') - Min('views'))
# эти функции нужно импортировать from django.db.models
# как получить сумму все views в каждом поле? - News.objects.aggregate(Sum('views'))

# Принципиальное различие aggregate и annotate:

# cats_aggregate = Category.objects.aggregate(Count('news')) - {'news__count': 17}

# cats_annotate = Category.objects.annotate(Count('news')) - QuerySet[1_obj, 2obj,...]
# Но у каждого этого obj появится поле news__count (поле, не метод)
# >>> for c in cats_annotate:
# ...     print(f'{c.title} - {c.news__count}')
# ...
# Спорт - 3
# Культура - 2
# Наука - 4
# Политика - 2
# Экономика - 4
# Тест - 0

# Aggregate - подсчитывает общее значение по полю или модели
# Annotate - возвращает QuerySet, но с новым полем
# Annotate может использоваться при денормализации
# Разумеется и там и там можно присваивать названия полям:
# c = Category.objects.annotate(lil = Count('news')) --- c[0].lil

# >>> N = News.objects.aggregate(data=Max('created_it'))
# >>> N
# {'data': datetime.datetime(2020, 9, 1, 7, 16, 35, 285575, tzinfo=<UTC>)} - дата создания последней новости

# Важный момент - можно вписывать поля, а можно модели - как минимум по связи ForeignKey и ManyToMany
# но если вписываешь модель, то писать нужно через нижний регистр

# --------------
# Интересный пример, который проясняет разницу между Count() и Max() и Sum():

# Max()
# >>> cats_max = Category.objects.annotate(max_views=Max('news__views'))
# >>> for i in cats_max:
# ...     print(f'{i.title} - {i.max_views}')
# ...
# Спорт - 4343
# Культура - 150
# Наука - 5445
# Политика - 13
# Экономика - 1508
# Тест - None

# Count()
# >>> cats_count = Category.objects.annotate(count_views=Count('news__views'))
# >>> for j in cats_count:
# ...     print(f'{j.title} - {j.count_views}')
# ...
# Спорт - 3
# Культура - 2
# Наука - 4
# Политика - 2
# Экономика - 4
# Тест - 0

# Sum()
# >>> cats_sum = Category.objects.annotate(sum_views=Sum('news__views'))
# >>> for i in cats_sum:
# ...     print(f'{i.title} - {i.sum_views}')
# ...
# Спорт - 4843
# Культура - 150
# Наука - 5511
# Политика - 13
# Экономика - 2696
# Тест - None

# Max в данном случае посчитала у какой news для этой категории максимальное количество views
# Sum - сложила все views для каждой категории
# А Count - вообще посчитала количество непосредственно полей, прикрепленных к каждой категории
# (всмысле количество экземпляров)
# Вот как то так

# Кстати annotate - возвращает QuerySet, который мы можем фильтровать дальше
# Если у нашей категории 0 записей, то как не выводить этот ноль?
# Cn = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
# >>> for i in cn:
# ...     print(f'{i.title} - {i.cnt}')
# ...
# Спорт - 3
# Культура - 2
# Наука - 4
# Политика - 2
# Экономика - 4
# Это к вопросу о дальнейшей фильтрации при annotate
# --------------------------

# метод values в django
# метод values в dj несколько отличается от такового в python. Он возвращает словарь,
# или QuerySet из словарей, в зависимости от того, работаем мы с одним объектом экземпляром
# или с несколькими:
# News.objects.values('title', 'views').get(pk=12) - {'title': 'Some title', 'views': 0}
# при работе с несколькими объектами модели он вернет QuerySet
# можно через values обращаться также к полю другой модели (связанной как либо)
# N = News.objects.values('title','views','category__title') где
# 'category_' - название поля в News
# '_title' - название поля в Category
# Его мякотка состоит в том, что он не требует запросов в базу данных,
# или требует, но по минимуму. Это называется денормализацией.
# Проитерируй в консоле News.objects.values('title', 'category__title') и
# News.objects.all() и через connection.queries сравни кол-во запросов

# Класс F
# как прибавить в нашей news.views еще один просмотр?
# можно так (не рекомендуется):
# n = News.objects.get(pk=12) >> n.views += 1 >> n.save()
# а можно так (рекомендуется):
# n = News.objects.get(pk=12) >> n.views = F('views') + 1
# импортируется класс F из django.db.models
# с помощью класса F можно получить запись в бд,
# где, допустим, название содержится в статье:
# News.objects.filter(content__icontains=F('title'))

# Часть вычислений мы можем перенести на сторону сервера.
# И делается это с помощью специальных функций Database Functions
# можно эти вычисления производить с помощью python, а можно с помощью Database Functions
# Вообще как правило не стоит бояться нагружать сервер.
# импортируются эти функции from django.db.models.functions import length
# Coalesce # (alt+enter)
# news = News.objects.annotate(len=Length('title')).all()
# у объектов news появится свойство len : news[0].len
# Важно помнить, что вычисления с такими функциями делаются на стороне сервера



# Загугли Performing raw SQL queries  в django documentation, и ознакомься с этим
# >>> News.objects.raw('SELECT * FROM news_news')
# <RawQuerySet: SELECT * FROM news_news>
# RawQuerySet - еще один тип данных запросов
# В этом методе raw() - мы можем писать абсолютно любые SQL запросы
# Важный момент - raw-запрос должен включать в себя pk, это обязательное поле
# и при этом в самом запросе должен быть не pk а id SELECT id, title, content FROM news_news
# самое интересное, что здесь работает отложенная загрузка полей, т.е.
# мы можем не доставать эти поля в запросе, но потом все равно к ним обращаться
# но это так себе практика, потому что на каждое обращение будет выполнен SQL запрос,
# чтобы обратиться к полю. Поэтому лучше загружать все нужные поля в SELECT сразу

# Жадные - это противоположность ленивым в программировании, т.е. сделай все сразу
# если метод жадный, то он делает все сразу
# разумеется в django есть жадные методы
# select_related - это как раз жадный метод (см. в контроллере HomeNews)



#                       Pagination (Пагинация)
# Пагинация - разбивка queryset на страницы.
# Если у нач 1000 новстей в queryset - показывать их на одной странице не рационально
# Есть класс Pagination (look in Pagination django doc)
# В документации очень хорошо про него написано

# Вкратце, как работать с классом:
    # >>> from django.core.paginator import Paginator
    # >>> objects = ['john', 'paul', 'george', 'ringo']
    # >>> p = Paginator(objects, 2)
    #
    # >>> p.count
    # 4
    # >>> p.num_pages
    # 2
    # >>> type(p.page_range)
    # <class 'range_iterator'>
    # >>> p.page_range
    # range(1, 3)
    #
    # >>> page1 = p.page(1)
    # >>> page1
    # <Page 1 of 2>
    # >>> page1.object_list
    # ['john', 'paul']
    #
    # >>> page2 = p.page(2)
    # >>> page2.object_list
    # ['george', 'ringo']
    # >>> page2.has_next()
    # False
    # >>> page2.has_previous()
    # True
    # >>> page2.has_other_pages()
    # True
    # >>> page2.next_page_number()
    # Traceback (most recent call last):
    # ...
    # EmptyPage: That page contains no results
    # >>> page2.previous_page_number()
    # 1
    # >>> page2.start_index() # The 1-based index of the first item on this page
    # 3
    # >>> page2.end_index() # The 1-based index of the last item on this page
    # 4
    #
    # >>> p.page(0)
    # Traceback (most recent call last):
    # ...
    # EmptyPage: That page number is less than 1
    # >>> p.page(3)
    # Traceback (most recent call last):
    # ...
    # EmptyPage: That page contains no results


#                           Регистрация | Авторизация
# В doc смотри про UserCreationForm
# аутентификация - проверка, есть ли вообще такой пользователь с введенным логином и паролем
# авторизация, если пользователь прошел аутентификацию, авторизация его к ресурсам, к которым он имеет право доступа

# функция authenticate(request, username=cleaned_data['username'], password=cleaned_data['password']) -
# возвращает объект пользователя по введенному логину и паролю. Это и есть атуентификация

# функция login(request, user) - авторизует пользователя полученного на предыдущем этапе. Это авторизация
# функция logout() -
# в проекте skillfactory очень хорошо расписано

# функция AuthenticationForm - освобождает от функции authentication, эта функция уже встроена в эту форму
# и эту валидацию форма будет проходить
# Но от метода login она таки не избавляет



#                                  Кэширование в Django
#                                Django's cache framework

# самое быстрое кэширование в Django это memcached
# и кэш в оперативной памяти
# есть кэширование в базу данных, для этого создается специальная таблица для хранения кэша (менее эффективный способ)

# есть кэширование в файловую систему
# мы поизучаем кэширование в файловую систему Filesystem caching



# Как что-то кэшировать на уровне контроллеров функций?
# используется декоратор @cache_page() :

# from django.views.decorators.cache import cache_page

# @cache_page(60 * 15, cache="special_cache")
# def my_view(request):
#     ...
# в аргументах - 60 * 15 - это количество времени в секундах



# но для class based views используется другой синтаксис кжширования
# тоже вызывается декоратор, но передается в другое место, а менно в url
# выглядит интересно:

# from django.views.decorators.cache import cache_page
#
# urlpatterns = [
#     path('foo/<int:code>/', cache_page(60 * 15)(my_view)),
# ]

# не забывай, что это передается декоратор в url а не функция или метод
# выглядит странно
# в корне проекта нужно создать папку django_cache
# именно туда она будет класть закэшированные файлы

# но кэшировать можно также через теги django

# смотри как мы закэшировали sidebar в base

# Возможно кэш нужно добавлять в конце приложения, чтобы во время разработки и проверки sql запросов
# он не вводил в заблуждение. На этапе разрабоки кэш отключается, чтобы всегда видеть актуальные данные



# API низкого уровня для кэширования
# The low-level cache API
# >>> from django.core.cache import caches

# там две основные функции set() и get()

# get() - получить кэш
# set() - установить его (закэшировать) (см. в doc как работают)

# есть get_or_set() - ну ты понял

# кароче, смотри в news_tags.py




#======================================== SETTINGS =================================================================

# Если импортировать settings то:
# from django.conf import settings

# в settings используются в основном константы, и часто эти константы из проекта в проект одни и те же


#  STATIC--------
# (уже есть) BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
# # константа BASE_DIR - ведет в корень проекта, корнем считается папка mysite (ну очевидно какая именно)

# STATIC_ROOT = os.path.join(BASE_DIR, 'static') STATIC_ROOT - указывает путь к папке, в которой будут храниться
# #                                              все статические файлы
# #                                              суть этой команды - собрать всю статику со всего приложения - в единое место
# #                                              происходит это уже на боевом сервере
#                                                используется комманда python manage.py collectstatic

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'mysite/static'),
# ]
# если статика где-то еще лежит, в STATICFILES_DIRS можно указать пути, от куда django будет забирать статику
# и собирать ее на одном уровне 'static', а не 'mysite/static', где настройки

# консольная команда python manage.py collectstatic собирает всю статику с приложения
# после этой команды появляется папка static  в корне проекта, куда скопированы вся статика проекта
# если что-то непонятно про подключение статики - пересмотри 22-й урок подробных курсов про джанго


# TEMPLATES---------

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [
#             os.path.join(BASE_DIR, 'templates')
#         ],# в этой конфигурации прописано, где django должен искать шаблоны
#
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#             ],
#         },
#     },
# ]

# В ключе DIRS мы прописываем os.path.join(BASE_DIR, 'templates') (нужно создать папку templates)
# os.path.join() - соединяет пути, а именно нашу корневую папку BASE_DIR и название другой папки


# MEDIA---------

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
#
# MEDIA_URL = '/media/'

# django умеет обрабатывать статику, умеет обрабатывать выгруженные файлы, но все это в режиме дебага
# Поэтому в url прописываем:
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# таким образом мы указываем где django брать выгруженные файлы
# Что в данном случае делать на боевом сервере я хз


# CACHES-----------

# для файлового кэширования
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': os.path.join(BASE_DIR, 'django_caches'),
#     }
# }
# а вообще любое (или почти любое) кэширование требует каких-то дополнительных настроек
# которые можно посмотреть в doc



#                                        НЕМНОГО ПРО ФОРМЫ

# Формы поиска чаще всего используют http метод get




#                                     МЕТОДЫ ХРАНЕНИЯ ДЕРЕВЬЕВ В БД

# Три основных:
# 1. Adjacency List (AL) - Смежный список
# 2. Matherialized Path (MP) - Материализованный путь
# 3. Nested Set (NS) - Вложенный набор (установленность)

# AL - самый распространенный.
# MP - хрантися полный путь от потомка к родителю
# Гугли и изучай, что это такое

# Мы будем заниматься NS
# https://postgres.men/database/postgresql/nested-sets-introduction/
# http://zabolotnev.com/mysql-nested-sets

# для nested set усть модуль mptt
# Вообще и для AL есть свой модуль

# в testapp мы работаем с паттерном NS уже готовой библиотеки mptt.
# Обрати там внимание, на модель, на админсайт, и на rubric.html,
# и на таблицу testapp_rubric в бд, там все подробно расписано, и понятно
# Но это работа с уже готовой библиотекой. А можно (и иногда даже нужно) писать самим

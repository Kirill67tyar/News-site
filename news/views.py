from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django import template
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, View, DetailView, CreateView
from news.models import News, Category
from . import forms
from news.utils import MyMixin
from django.contrib import messages
from django.core.mail import send_mail




# def register(request):
#     form = forms.MyyyyyyyyyyyyyyyyyyyyyyyyyyyyyUserRegisterForm()
#     return render(request, 'news/register.html', {'form': form,})



def sender_email(request):
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        print(f'\n\n&&&&&&&&&&&&&&&&&&&&&&&&&&&\n'
              f'request,POST - {request.POST}\n'  # request.POST - это QueryDict(словарь с ключами в виде полец формы)
              f'\n&&&&&&&&&&&&&&&&&&&&&&&&&&&\n\n')# и значением в виде того что ввели (что и отправляется на сервер)
        if form.is_valid():
            email = request.user.email
            cd = form.cleaned_data
            mail = send_mail(cd['subject'], cd['content'], settings.EMAIL_HOST_USER,
                      [email], fail_silently=True) # для пробы email можно прописать другой в str
            # функция send_email() возвращает цифры. Если она успешно отправила одно письмо, то это будет 1
            # если не отправила, то 0
            if mail:
                messages.info(request, 'Письмо отправлено')
                return redirect(reverse('news:home'))
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = forms.ContactForm()
    print(f'\n\n::::::::::::::::::::::::::::::::\n'
          f'request.user.email - {request.user.email}'
          f'\n:::::::::::::::::::::::::::::::::\n\n')
    return render(request, 'news/export.html', {'form': form})
# при отправке на почту гугли smtp yandex(заменить на любую другую почту)
# и возможно doc Django. 48 урок хоть и не полно, но не плохо показывает настройку отпраки писем из приложения





def register(request):
    if request.method == 'POST':
        form = forms.UserRegisterForm(request.POST)
        if form.is_valid(): # если мы используем встроенную форму UserCreationForm, то
            user = form.save()     # она будет работать с встроенной моделью User
                            # UserCreationForm связана с моделью User
            messages.success(request, 'Вы успешно зарегистрировались')
    #         таким образом, мы сохраняем в messages (какое-то хранилище сообщений) наше сообщение
    # есть и более сложный вариант (read in doc)
    #         далее в темплейте с помощью цикла выводим накопившиеся сообщения

            # wow. мы можем сразу залогинить зарегистрированного пользователя
            login(request, user)
            return redirect(reverse('news:home'))
        else:
            messages.error(request, 'Oops, что-то пошло не так')
    else:
        form = forms.UserRegisterForm()
    return render(request, 'news/register.html', {'form': form,})



def user_login(request):
    if request.method == 'POST':
        form = forms.UserLoginForm(data=request.POST)
        # обрати внимание, что присваиваешь именнованному аргументу data наш request.POST
        # скорее всего это потому что request.POST словарь, а AuthenticatedForm, имеет схожую логику
        # с ModelSerializer
        if form.is_valid():
            user = form.get_user() # с помощью метода get_user() - мы получаем пользователя.
            # Почему мы не можем добавить просто форму - не знаю.
            login(request, user)
            messages.info(request, 'Авторизация прошла успешно, милости просим=)')
            return redirect(reverse('news:home'))
        messages.error(request, 'Что-то пошло не так')
    else:
        form = forms.UserLoginForm

    return render(request, 'news/login.html', context={'form': form})


def user_logout(request):
    logout(request)
    return redirect(reverse('news:login'))


class HomeNews(LoginRequiredMixin, MyMixin, ListView):  # LoginRequiredMixin,
    paginate_by = 4 # указывает сколько объектов QuerySet выводить на страницу. Заменят Paginator(Queryset, 4)
    # после этого нам в шаблоне будут доступны paginator и page_obj в конткесте темплейта
    # у paginator и page_obj можно вызывать свойства Paginator класса (см. в doc Django)
    # ! методы в темплейт вызываются как и свойства - без скобок
    # page_obj - это скорее всего объект класса Paginator (не точно), т.е. одна из его страниц
    # для прояснения ситуации - посмотри, как пагинация передается в функции, а не классе (документация)
    # Хоть мы это и не выводим, но в шаблоне мы получаем в итоге QuerySet,
    # как после метода object_list(), который мы применяем конкретно к каждой странице шаблона

    model = News
    template_name = 'news/home_list_news.html'
    # если queryset простой, то необязательно использовать функцию get_queryset()
    queryset = News.objects.filter(is_published=True).select_related('category')
    context_object_name = 'news'
    mixin_prop = 'blablabla'

    login_url = reverse_lazy('news:login') #'/admin/' # можно прописывать для LoginRequiredMixin
    # но login_url и редиректит на этот адрес, что отстойно

    # raise_exception = True # вместо login_url или редиректа на страницу атентификации,
    # вызовет ошибку 403 если пользователь не аутентифицирован

# Таким образом можно сделать вывод, что LoginRequiredMixin не только редиректит,
# но ключевое - не дает зайти неавторизованному пользователю
# и может также вызвать ошибку 403

    # mixin_prop = 'Hello world!!'
    # extra_content = {'title': 'Главная'} # задать дополнительные (несложные, статичные) параметры в контекст
#                                         для динамических параметров его использовать не следует

# если задать в контекст сложные динамические параметры, или полностью его переопределить, то:
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(HomeNews, self).get_context_data(**kwargs)
        categories = Category.objects.annotate(cnt=Count('news')).filter(cnt__gt=0)
        context['title'] = self.get_title_upper('Главная страница') # использование нашего миксина
        context['categories'] = categories
        context['mixin_prop'] = self.view_get_prop() # использование нашего миксина

        print(f'\n\nDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD\n'
              f'context - {context}'
              f'\nDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD\n\n')
        return context

    # def get_queryset(self):
    #     queryset = News.objects.filter(is_published=True).select_related('category')
    #     # сравни количество sql запросов с select_related и без, и вспомни
    #     # что select_related() - жадный метод
    #     # Насколько это соотносится с денормализацией?
    #     return queryset



class NewsByCategory(LoginRequiredMixin, MyMixin, ListView):    # LoginRequiredMixin,
    paginate_by = 4
    model = News
    # template_name = 'news/category.html'
    template_name = 'news/home_list_news.html'
    context_object_name = 'news'
    allow_empty = False # не позволяет, выдавать пустой список и вызывает ошибку 404
    login_url = reverse_lazy('news:login')


    def get_queryset(self):
        queryset = super().get_queryset()
        return News.objects.filter(category_id=self.kwargs['pk'], is_published=True).select_related('category')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        category = Category.objects.get(pk=self.kwargs['pk'])
        context['category'] = category
        context['title'] = category.title
        return context


class ViewNews(LoginRequiredMixin, DetailView): # LoginRequiredMixin,
    model = News
    template_name='news/view_news.html'
    context_object_name = 'news_item'
    login_url = reverse_lazy('news:login')
    # pk_url_kwarg = 'news_id' # нужен, если как-то не стандартно называется pk в url
#     Скорее всего в DetailView автоматически используется get_object_or_404
#   Попробуй зайти через url на несуществующую новость


class CreateNews(LoginRequiredMixin, CreateView):   # LoginRequiredMixin,
    form_class = forms.NewsModelForm #     CreateView надо связать с какой-то формой а не моделей:
    template_name = 'news/add_news.html'
    login_url = reverse_lazy('news:login')
    # success_url = reverse_lazy('news:home') # success_url с reverse здесь не работает. А теперь мякотка:
#     функцию reverse здесь использовать нельзя, здусь нужно использовать reverse_lazy
# reverse_lazy используется только тогда, когда до него дойдет очередь
#     Но если success_url здесь не использовать
#     редирект будет происходит благодаря get_absolute_url описанного в модели,
#     который получает url каждой конкретной новости
# класс унаследованный от CreateView - одно из тех мест, где джанго ожидает get_absolute_url
# именно с таким названием
# Таким образом модели могут отвечать и за редирект


def index(request):
    print('\n\n###############################################',
          'Кишки request (dir(request))',
          *dir(request),
          '###############################################\n\n',sep='\n')

    # news = News.objects.all()
    news = News.objects.order_by('-created_it')
    categories = Category.objects.all()

    context = {
        'news' : news,
        'title': 'список новостей',
        # 'categories': categories, # отныне эти переменные в контексте не нужны, \
                                    # т.к. у нас есть соответствующий тег
    }

    return render(request, 'news/home_list_news.html', context)


def get_category(request, pk):

    news = News.objects.filter(category_id=pk) # category_id - одно из полей в таблице news_news, созданное благодаря
    categories = Category.objects.all()         # связи ForeignKey
    category = Category.objects.get(pk=pk)
    ctx = {
        'news': news,
        # 'categories': categories,
        'category': category,
    }

    return render(request, template_name='news/category.html', context=ctx)





def index1(request, pk=None):

    news = News.objects.order_by('-created_it')
    categories = Category.objects.all()
    category = None

    context = {
        'news': news,
        # 'categories': categories, вместо ключа в словаре - тег
        'title': 'список новостей',
        'category': category
    }

    if pk != None:
        news = news.filter(category_id=pk)
        category = Category.objects.get(pk=pk)
        context['news']  = news
        context['category'] = category
        return render(request, 'news/category.html', context=context)

    return render(request, template_name='news/home_list_news.html', context=context)



def view_news(request, news_id):
    # news_item = News.objects.get(pk=news_id)
    news_item = get_object_or_404(News, pk=news_id)
    ctx = {
        'news_item': news_item,
    }

    return render(request, 'news/view_news.html', context=ctx)



def add_news(request):
    if request.method == 'POST':
        # form = forms.NewsForm(request.POST)
        form = forms.NewsModelForm(request.POST)
        print(f'\n\n################################\n'
              f'request.POST - {request.POST}'
              f'\n##################################\n\n')
        if form.is_valid():
            # если форма прошла валидацию, то у формы появляется такое свойство, как словарь cleaned_data
            # а валидацию она проходит исходя из параметров, которые мы установили в модели
            print(f'\n\n*********************************\n'
                  f'form.cleaned_data - {form.cleaned_data}'
                  f'\n************************************\n\n')
            # data = form.cleaned_data    # for usual forms
            # news = News(**data)
            # news.save()
            # OR
            # news = News.objects.create(**data)  # for usual forms
            # присваиваем переменной news, чтобы использоавать ее в редиректе
            news = form.save()   # for model-forms
            # метод save() - есть у модельных форм, не у обчных
            # и в модельные формы не нужно пихать form.cleaned_data, они работают напрямую с моделями
            return redirect(reverse('news:view_news', kwargs={'news_id': news.id}))
    else:
        # form = forms.NewsForm()
        form = forms.NewsModelForm()
    context = {'form': form,}

    return render(request, template_name='news/add_news.html', context=context)



def test_pagination(request):
    objects = ['john1', 'paul2', 'george3', 'ringo4', 'john5', 'paul6', 'george7',]
    paginator = Paginator(objects, 2)

    num_page = request.GET.get('page', 1) # request.GET - у нас словарь
# этот словарь QueryDict. Посмотри в косоли как он выглядит. Так мы получим номер в виде int нашей страницы
#    ?page в url считается get аргументом

    print(f'\n\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\n'
          f'request.GET - {request.GET}\n'
          f'paginator - {paginator}\n'
          f'paginator.get_page(num_page) - {paginator.get_page(num_page)}'
          f'\nQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ\n\n')

    page_objects = paginator.get_page(num_page) # есть метод page(), а есть get_page().
    #                                           туда передается int, номер страницы
    #                                           get_page() не вызывает ошибку если страницы нет
    #                                           page() - вызывает

    return render(request, 'news/test_pagination.html', {'page_obj': page_objects})
#      желательно всегда использовать в названии page_obj для контекста
#      именно такое название передается по умолчанию при наследовании ListView
# Хоть мы это и не выводим, но в шабло










def console(request):
    piece_of_news = News.objects.first()
    category = Category.objects.get(pk=1)
    print('\n\n((((((((((((((((((((((((((\n'
          'dir(News.objects.first())',
          *dir(News.objects.first()),
          '\n',
          'dir(News.objects.all())',
          *dir(News.objects.all()),
          ')))))))))))))))))))))))))))))))\n\n',sep='\n')

    print(f'\n\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
          f'template - {template}\n'
          f'teplate.Library() - {template.Library()}'
          f'\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n\n')

    print(f'\n\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n'
          f'dir(ListView) - {dir(ListView)}\n'
          f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n'
          f'ListView.__dict__ - {ListView.__dict__}\n'
          f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n'
          f'ListView.mro() - {ListView.mro()}\n'
          f'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n\n')

    print(f'\n\nZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n'
          f'dir(View) - {dir(View)}\n'
          f'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n'
          f'View.__dict__ - {View.__dict__}\n'
          f'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n'
          f'View.mro() - {View.mro()}\n'
          f'ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ\n\n')


    print(f'\n\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n'
          f'category.title - '
          f'{type(category)}'
          f'\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@\n\n')

    return HttpResponse('<h1>Look in console</h1>')


# MVC = MTV (архитектурный паттерн django)
# MVC - models     views          controller
# MTV - models     templates      views


# views (controller) - это часть приложения,
# которая вызывается в ответ на клиентские запросы

# контроллер - некое связующее звено между
# моделями(таблицами в бд) и представлениями templates (шаблоны интерфейса в основном html)

# Ну а формы (forms) - связующее звено между models-templates-views,
# причем связывает каждое с каждым

# в request хранятся все возможные данные
# о полученном запросе, о клиенте, о его браузере, куки, данные сессии
# и это далеко не все что там хранится
# выведи в консоль dir(request)

# request - экземпляр класса HttpRequest

# alt-enter очень полезная комбинация для джанго на пайчарме. Наведи на незаимствованный метод и проверь)

# рендеринг - это когда мы берем некий файл, шаблон, и наполняем его данными из модели
# функция render

# objects - это менеджер объектов из бд

# в шаблонах мы используем три составляющие из джанго - дерективы(переменные из контекста), теги, фильтры
# с помощью них мы и размещаем ин-фу на страницах html


# Фильтры (не знал куда записывать)
# slug - используется для url адресов, теперь это уже окончательно понятно
# так вот, есть фильтр в django, использующийся в шаблоне, который преобразует строку в slug {{value|slugify}}
# чекни фильтр timesinse (применяется в купе с dateField) {{some_date|timesince}}
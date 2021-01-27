"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from news import urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('captcha/', include('captcha.urls')),
    path('test/', include('testapp.urls', namespace='testapp')),
    path('index/', include('news.urls', namespace='news')),

]
# функция url для старой версии Django. для нее нужно добавлять ^ в начало url-маршрута и r перед url маршрутом
# path() заменяет url()
# при добавлении url адресов стоит следовать правилу - более конкретные маршруты должны идти выше,
# чем более общие



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar

    urlpatterns += [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ]





# lesson 20, (part 2) start

# 31 урок django про серверы

































































# 7 lesson start
# path wfms-djangocourseneu
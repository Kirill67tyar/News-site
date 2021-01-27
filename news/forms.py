from django import forms
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from . import models
from .models import Category
import re
from captcha.fields import CaptchaField




class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control', }))
    content = forms.CharField(
        label='Текст',
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=False)
    capctha = CaptchaField()




class NewsForm(forms.Form):
    title = forms.CharField(max_length=50,
                            label='Название',
                            widget=forms.TextInput(attrs={'class': 'form-control'}))

    content = forms.CharField(widget=forms.Textarea(attrs={
                                            'class': 'form-control', 'rows': 5
                                                           }), label='Текст статьи', required=False)
    # photo = forms.ImageField()
# аргумент initial в forms.BooleanField - отвечает за значение по умолчанию (странно что не default)
    is_published = forms.BooleanField(label='Опубликовать?',
                                      initial=True,
                                      widget=forms.CheckboxInput(attrs={'class': 'form-control'}))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                    label='Категория',
                                    empty_label='Веберите категорию',
                                    widget=forms.Select(attrs={'class': 'form-control'}))


# forms.ModelMultipleChoiceField(NameModel) - поле формы для связи many-to-many



class NewsModelForm(forms.ModelForm):
    class Meta:
        model = models.News
        fields = 'title', 'content', 'is_published', 'category', 'photo'
        # fields = '__all__' # будут представлены все поля из используемой модели
#       А как в бекэнде установить стили для форм? А вот так:
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content' : forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # 'content' : CKEditorUploadingWidget(),
            'is_published' : forms.CheckboxInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }
    # почитать в doc, как добавить CKEditorUploadingWidget() пользователям.
    # чтобы при добалении новости у них была такая продвинутая панель


    # когда мы описываем валидатор с названием clean_<name field> (как этот валидатор)
    # то его не обязательно передавать в аргументы validators, как мы это делали с itvdn
    # но проверять этот валидатор будет уже после основной проверки валидации в контроллере
    # обрати внимание, что мы используем cleaned_data
    # обрати внимание, что возвращает этот валидатор
    # в словарь cleaned_data попадет ключ и значение, где ключ name в названии функции (clean_<name>)
    # а значение - то что возвращает эта функция.
    # и все таки это кастомный валидатор
    def clean_title(self):  # валидатор проверяет, что название начинается с цифры
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title



class UserLoginForm(AuthenticationForm) :
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control',}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))




class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(
        attrs={'class': 'form-control', 'autocomplete': 'off'}))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='E-mail', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    # не забывай, что в аргументы полей форм можно также передавать help_text

    class Meta:
        model = User
        fields = 'username', 'email', 'password1', 'password2',
# Важная ремарка - аттрибут fields, как мне кажется не привязан строго к модели к классе Meta
# т.е. он может брать поля из этой модели, но и может брать поля определенные раньше, до класса Meta
# включая поля класса, от которого мы наследуемся (UserCreationForm)
# а в widgets эти поля могут дополняться
# Вопрос в том, куда эти поля будут дальше сохраняться

# дилемма метода set_password()
# скорее всего в UserCreationForm уже используется метод set_password()
# который шифрует пароль и сохраняет его в бд, т.к. нигде в конторллере мы его не использвали
# а должны были бы. Но ключевое здесь - 'скорее всего' (в самом UserCreationForm set_password не определен)
# Попрака, set_password определен в классе AbstractBaseUser от которого наследуется AbstractUser,
# от которого в свою очередь наследуется уже User. А теперь вспомни,
# что UserCreationForm - по сути модельная форма User





# поля форм нужно переопределять, чтобы они не имели оформление django
# ниже моя форма, и она не совсем правильная
# class MyyyyyyyyyyyyyyyyyyyyyyyyyyyyyUserRegisterForm(forms.ModelForm):
#
#     password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#     password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
#
#     class Meta:
#         model = User
#         fields = 'username', 'email',
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control'}),
#
#         }


# по работе с формами - отличный урок 24 подробных курсов по джанго. Пересмотри его


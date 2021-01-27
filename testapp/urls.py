from django.urls import path
from . import views

app_name = 'testapp'

urlpatterns = [
    path('', views.test, name='test'),
    path('all-rubric/', views.show_rubrics, name='all_rubrics'),
    path('rubric/<int:pk>', views.get_rubric, name='rubric')
]

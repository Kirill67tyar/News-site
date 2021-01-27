from django.shortcuts import render, HttpResponse
from string import printable
from random import choice, randrange, SystemRandom
from .models import Rubric




def test(request):
    krakoziabra = ''.join([choice(printable[10:62]) for i in range(randrange(10,50))])
    context = {'shalom':'Шалом ворлд', 'salt': krakoziabra, }
    return render(request=request, template_name='testapp/test.html', context=context)




def show_rubrics(request):
    return render(request, "testapp/rubric.html", {'rubrics': Rubric.objects.all()})


def get_rubric(request, pk):
    rubric = Rubric.objects.get(pk=pk)
    return render(request, 'testapp/rubric.html', context={'rubruc': rubric})










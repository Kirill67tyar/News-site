from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import reverse



class Rubric(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('testapp:rubric', kwargs={'pk': self.pk})

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Рубрика(у)'
        verbose_name_plural = 'Рубрики'



class Article(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    category = TreeForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Статья(ю)'
        verbose_name_plural = 'Статьи'




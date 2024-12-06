from django.db import models


class Categories(models.Model):
    title = models.CharField(max_length=125, verbose_name='title')

    def __str__(self):
        return self.title


class Tags(models.Model):
    title = models.CharField(max_length=125, verbose_name='title')

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=125, verbose_name='title')
    content = models.TextField(verbose_name='content')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE,
                                 verbose_name='category',
                                 blank=True, null=True)
    tags = models.ManyToManyField(to=Tags, verbose_name='tags',
                                  blank=True)
    createdAt = models.DateField(verbose_name='date of publishing')
    updatedAt = models.DateField(verbose_name='date of updating')

    def __str__(self):
        return self.title
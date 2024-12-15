from django.db import models


class Categories(models.Model):
    category = models.CharField(max_length=125, verbose_name='category')

    def __str__(self):
        return self.category


class Tags(models.Model):
    tag = models.CharField(max_length=125, verbose_name='tag')

    def __str__(self):
        return self.tag


class Article(models.Model):
    title = models.CharField(max_length=125, verbose_name='title')
    content = models.TextField(verbose_name='content')
    category_id = models.ForeignKey(to=Categories, on_delete=models.CASCADE,
                                    verbose_name='category_id',
                                    blank=True, null=True)
    tags_id = models.ManyToManyField(to=Tags, verbose_name='tags_id',
                                     blank=True)
    createdAt = models.DateField(verbose_name='date of publishing')
    updatedAt = models.DateField(verbose_name='date of updating',
                                 blank=True, null=True)

    def __str__(self):
        return self.title
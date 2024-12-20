# Generated by Django 4.2.16 on 2024-12-06 16:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125, verbose_name='title')),
            ],
        ),
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=125, verbose_name='title')),
            ],
        ),
        migrations.RenameField(
            model_name='article',
            old_name='date',
            new_name='createdAt',
        ),
        migrations.RemoveField(
            model_name='article',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='article',
            name='text',
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(default='Text', verbose_name='content'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='updatedAt',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='date of updating'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.categories', verbose_name='category'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='catalog.tags', verbose_name='tags'),
        ),
    ]

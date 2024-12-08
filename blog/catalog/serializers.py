from rest_framework import serializers
from .models import Article, Categories, Tags


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category']


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tag']


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category_id',
                  'tags_id', 'createdAt', 'updatedAt']

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
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
    category = serializers.SerializerMethodField()
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = ['title', 'content', 'category',
                  'tags', 'createdAt', 'updatedAt', 
                  'category_id', 'tags_id']
        
    def get_category(self, obj):
        if obj.category_id:
            return obj.category_id.category
        return None
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_tags(self, obj):
        return [tag.tag for tag in obj.tags_id.all()]
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime as dt

from .models import Article, Categories, Tags
from .serializers import (ArticleSerializer, 
                          CategorySerializer, 
                          TagsSerializer)


class SingleArticleView(APIView):
    def get_article(self, article_id):
        try:
            return Article.objects.get(id=article_id)
        except Article.DoesNotExist:
            return None

    def get_category(self, category_name):
        try:
            return Categories.objects.get(category=category_name)
        except Categories.DoesNotExist:
            return None

    def get_tag(self, tag_name):
        try:
            return Tags.objects.get(tag=tag_name)
        except Tags.DoesNotExist:
            return None
        
    def check_category(self, category_name):
        category = self.get_category(category_name)
        if category is None:
            category_serializer = CategorySerializer(data={'category': category_name})
            if category_serializer.is_valid():
                category = category_serializer.save()
            else:
                return Response(category_serializer.errors, 
                                status=status.HTTP_400_BAD_REQUEST)
        return category
    
    def check_tags(self, tag_list):
        tags = []
        for tag_name in tag_list:
            tag = self.get_tag(tag_name)
            if tag is None:
                tag_serializer = TagsSerializer(data={'tag', tag_name})
                if tag_serializer.is_valid():
                    tag = tag_serializer.save()
                else:
                    return Response(tag_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            tags.append(tag.id)
        return tags

    def post(self, request):
        category_name = request.data.get('category')
        category = self.check_category(category_name)

        tag_list = request.data.get('tags', [])
        tags = self.check_tags(tag_list)
        
        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'category': category.id,
            'tags': tags,
            'createdAt': dt.datetime.now().strftime('%d.%m.%Y'),
            'updatedAt': None
        }
        article_serializer = ArticleSerializer(data=data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data,
                             status=status.HTTP_201_CREATED)
        
        return Response(article_serializer.data,
                         status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, article_id):
        article_instance = self.get_article(article_id)
        if not article_instance:
            Response(status=status.HTTP_404_NOT_FOUND)
        
        data = {}
        if request.data.get('title'):
            data['title'] = request.data.get('title')
        if request.data.get('content'):
            data['content'] = request.data.get('content')
        if request.data.get('category'):
            category_name = request.data.get('category')
            category = self.check_category(category_name)
            data['category'] = category
        if request.data.get('tags'):
            tag_list = request.data.get('tags')
            tags = self.check_tags(tag_list)
            data['tags'] = tags
        if len(data) > 0:
            data['updatedAt']: dt.datetime.now().strftime('%d.%m.%Y')
        
        article_serializer = ArticleSerializer(isinstance=article_instance,
                                               data=data,
                                               partial=True,
                                               context={'request':request})
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data, 
                            status=status.HTTP_200_OK)
        return Response(article_serializer.errors, 
                        status=status.HTTP_400_BAD_REQUEST)
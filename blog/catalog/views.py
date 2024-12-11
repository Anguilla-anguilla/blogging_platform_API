from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema


import datetime as dt

from .models import Article, Categories, Tags
from .serializers import (ArticleSerializer, 
                          CategorySerializer, 
                          TagsSerializer)


class PostArticleView(GenericAPIView):
    serializer_class = ArticleSerializer

    @extend_schema(request=ArticleSerializer)
    def post(self, request):
        single_article_view = SingleArticleView()

        category_name = request.data.get('category')
        category = single_article_view.check_category(category_name)
        if not category:
            return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

        tag_list = request.data.get('tags', [])
        tags = single_article_view.check_tags(tag_list)
        if isinstance(tags, Response):
            return tags

        data = {
            'title': request.data.get('title'),
            'content': request.data.get('content'),
            'category_id': category.id,
            'tags_id': [tag.id for tag in tags],
            'createdAt': dt.datetime.now().strftime('%Y-%m-%d'),
            'updatedAt': None
        }
        print(data)
        article_serializer = ArticleSerializer(data=data)
        if article_serializer.is_valid():
            article_serializer.save()
            return Response(article_serializer.data,
                                status=status.HTTP_201_CREATED)
        print(article_serializer.errors)
        
        return Response(article_serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)


class SingleArticleView(GenericAPIView):
    serializer_class = ArticleSerializer

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
                return None
        return category
    
    def check_tags(self, tag_list):
        tags = []
        for tag_name in tag_list:
            tag = self.get_tag(tag_name)
            if tag is None:
                tag_serializer = TagsSerializer(data={'tag': tag_name})
                if tag_serializer.is_valid():
                    tag = tag_serializer.save()
                else:
                    return Response(tag_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            tags.append(tag)
        return tags

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
            data['updatedAt'] = dt.datetime.now().strftime('%Y-%m-%d')

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
    
    def delete(self, article_id):
        article_instance = self.get_article(article_id)
        if not article_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article_instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, article_id):
        article_instance = self.get_article(article_id)
        if not article_instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        article_serializer = ArticleSerializer(isinstance=article_instance)
        return Response(article_serializer.data, 
                        status=status.HTTP_200_OK)


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content', 'category_id__category', 'tags_id__tag']

    def get_queryset(self):
        queryset = super().get_queryset()
        search_term = self.request.query_params.get('search', None)
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term) |
                Q(content__icontains=search_term) |
                Q(category_id__category__icontains=search_term) |
                Q(tags_id__tag__icontains=search_term)
            ).distinct()
        return queryset
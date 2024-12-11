from django.urls import path

from . import views

app_name = 'catalog'


urlpatterns = [
    path('api/', views.ArticleViewSet.as_view({'get': 'list'}), name='view-set'),
    path('api/<int:article_id>', views.SingleArticleView.as_view(), name='api-id'),
    path('api/new/', views.PostArticleView.as_view(), name='new-article')
]

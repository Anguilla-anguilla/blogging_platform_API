from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime as dt

from .models import Article
from .serializers import ArticleSerializer


class SingleArticleView(APIView):
    def post(self, request):
        # data = {
        #     'title': request.data.get('title'),
        #     'summary': request.data.get('summary'),
        #     'date': dt.datetime.now().strftime('%d.%m.%Y'),
        #     'text': request.data.get('text')
        # }
        serializer = ArticleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
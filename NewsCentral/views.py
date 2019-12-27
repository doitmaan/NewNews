from django.shortcuts import render

# Create your views here.
from django.db import transaction

# NewsCentral/views.py
from rest_framework import generics
import json
from .models import STOCK, LINK
from .serializers import NewsCentralSerializer, LinkTableSearlizer

from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from datetime import datetime
from newsapi import NewsApiClient
from rest_framework.permissions import IsAuthenticated #for authenication
from rest_framework.views import APIView


from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response


import logging


def index(request):
    try:
        raise Exception("Custom error thrown by newbie developer :D")
    except Exception as e:
        logging.getLogger("error_logger").error(repr(e))

        pass


class ListStocks(generics.ListCreateAPIView):
    queryset = STOCK.objects.all()
    serializer_class = NewsCentralSerializer


class ListLINKS(generics.ListCreateAPIView):
    queryset = LINK.objects.all()
    serializer_class = LinkTableSearlizer


class DetailStocks(generics.RetrieveUpdateDestroyAPIView):
    queryset = STOCK.objects.all()
    serializer_class = NewsCentralSerializer


class TabelsUtils():
    def createSTOCK(validated_data):
        STOCKObj, created = STOCK.objects.get_or_create(
            stockId=validated_data['stockId'],

        )

        return (STOCKObj, created)

    def createLINKTable(StcokId, LinkUrl, Publish_date, ImageLinkUrl, Title):
        LinkObj, created = LINK.objects.update_or_create(
            stcokId=StcokId,
            linkUrl=LinkUrl,
            publish_date=Publish_date,
            imageLinkUrl=ImageLinkUrl,
            title=Title)
        return (LinkObj, created)

    def PopulateLinkTable(Query):
        newsapi = NewsApiClient(api_key='715dbdda916144d68f79afee86185795')
        # /v2/everything

        all_articles = newsapi.get_everything(q=Query,
                                              language='en',
                                              sort_by='relevancy',
                                              page=2)

        articles = json.dumps(all_articles)  # dict to string
        articles = json.loads(articles)  # string to json
        print(articles['articles'])
        print("-----------------------------------------------")
        ac = 0
        creationLinkObjDict = {}
        for x in articles['articles']:
            print(x['url'])

            LinkObj, created = TabelsUtils.createLINKTable(Query, x['url'], x['publishedAt'], x['urlToImage'],
                                                           x['title'])
            creationLinkObjDict[LinkObj].append(created)

            ac = ac + 1

        print("the value of urls " + str(x))

        return creationLinkObjDict


@csrf_exempt
class PostValidatedStock():
    @api_view(["POST"])
    @csrf_exempt
    def PostStock(request):


        if request.method == 'POST':
            data = JSONParser().parse(request)

            # restrictions on input
            data = dict((k, v.upper()) for k, v in data.items())  # Upper casing all stocks

            #     if additional validation just in case
            #
            #
            #
            validated_data = data

            STOCKobj, created = TabelsUtils.createSTOCK(validated_data)

            if created:

                serializer = NewsCentralSerializer(STOCKobj)

                print("created")

                return JsonResponse(serializer.data['stockId'], safe=False, status=200)
            else:
                print("already is there")

                serializer = NewsCentralSerializer(STOCKobj)
                return JsonResponse(serializer.data['stockId'], safe=False, status=200)


@csrf_exempt
class PostMethodLink():
    @csrf_exempt
    @api_view(["POST"])
    def post_LINK(request):
        if request.method == 'POST':
            data = JSONParser().parse(request)
            print(data)
            qdat = str(data)
            # restrictions on input
            data = dict((k, v.upper()) for k, v in data.items())  # Upper casing all stocks
            print("the query is ")

            print(data['stockId'])

            null = None

            newsapi = NewsApiClient(api_key='715dbdda916144d68f79afee86185795')
            # /v2/everything

            all_articles = newsapi.get_everything(q=data['stockId'],
                                                  language='en', page=3
                                                  )
            print("iam here")
            articles = json.dumps(all_articles)  # dict to string
            articles = json.loads(articles)  # string to json

            # print(all_articles)

            failedarticelscounter = 0

            if (articles['articles'] is not null):

             for i in articles['articles']:
                print("---------")
                print(i['title'])
                print("---------")
                validated_data = {"stcok": str(data['stockId']), "linkUrl": str(i['url']),
                                  "publish_date": str(i['publishedAt']), "imageLinkUrl": str(i['urlToImage']),
                                  "title": str(i['title'])}
                serializer = LinkTableSearlizer(data=validated_data)
                print(serializer.is_valid())

                print("---------")

                if serializer.is_valid():
                    print("the sealizwer is valid")

                    serializer.save()
                else:
                    failedarticelscounter = failedarticelscounter + 1
                    print(serializer.errors)
            print("failed" + str(failedarticelscounter))

            return JsonResponse(serializer.data, safe=False, status=201)




@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)



# @csrf_exempt
# @api_view(["GET"])
# def sample_api(request):
#     data = {'sample_data': 123}
#     return Response(data, status=HTTP_200_OK)

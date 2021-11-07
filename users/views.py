from django.shortcuts import render
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class TestAPIView(APIView):

    def get(self, request):
        reply = {'data': {'message': 'Hello, world'}}
        print(request.user)
        return Response(reply, status=200, content_type='application/json')
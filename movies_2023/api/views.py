from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

@api_view(['GET'])
def getData(request):
  person={'name':'John','age':30}
  return Response(person)


from functools import partial
import json
from django.shortcuts import render
import io
from rest_framework.parsers import JSONParser
from .models import Student
from .serializers import StudentSerializer
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

# we are using function base view
@csrf_exempt
def student_api(request):
    if request.method == 'GET':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream) # python dictionary return
        id = pythondata.get('id', None) # if value in id is showing other wise none
        if id is not None:
            stu = Student.objects.get(id=id)
            serializers = StudentSerializer(stu)
            json_data = JSONRenderer().render(serializers.data)
            return HttpResponse(json_data, content_type='application/json')
        
        stu = Student.objects.all() # query set
        serializers = StudentSerializer(stu, many=True)
        json_data = JSONRenderer().render(serializers.data)
        return HttpResponse(json_data, content_type='application/json')
    
    if request.method == 'POST':
       json_data = request.body
       stream = io.BytesIO(json_data)
       pythondata = JSONParser().parse(stream)
       serializer = StudentSerializer(data=pythondata)
       if serializer.is_valid():
           serializer.save()
           res = {'msg':'Data is Created'}
           json_data = JSONRenderer().render(res)
           return HttpResponse(json_data, content_type='application/json')

       json_data = JSONRenderer().render(serializer.errors)
       return HttpResponse(json_data, content_type='application/json')

    if request.method == 'PUT':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')
        if not Student.objects.filter(id=id).exists():
            res = {'msg':'Sorry There is no record for updation !!!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        else:
            stu = Student.objects.get(id=id) # this is the model object
            serializer = StudentSerializer(stu, data=pythondata, partial=True)

        if serializer.is_valid(): # we checking here data is valid or not otherwise error showing
            serializer.save()
            res = {'msg':'Record is Successfull Updated !!!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        json_data = JSONParser().render(serializers.errors)
        return HttpResponse(json_data, content_type='application/json')

    if request.method == 'DELETE':
        json_data = request.body
        stream = io.BytesIO(json_data)
        pythondata = JSONParser().parse(stream)
        id = pythondata.get('id')

        if not Student.objects.filter(id=id).exists():
            res = {'msg':'Sorry for inconvenience There is no Record !!!'}
            json_data = JSONRenderer().render(res)
            return HttpResponse(json_data, content_type='application/json')
        else:
            stu = Student.objects.get(id=id)
            stu.delete()
 
        res = {'msg':'Data is Deleted'}
        # json_data = JSONRenderer().render(res)
        # return HttpResponse(json_data, content_type='application/json')
        return JsonResponse(res, safe=False)


       

        





import django
from django.shortcuts import render

from django.views.generic import ListView
from rest_framework import generics
from rest_framework import views

from .serializers import manGANSerializer
from backend.my_exception_handler import ImageHandlingError
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
# from rest_framework.views import exception_handler
import PIL
from PIL import Image
from io import BytesIO
import numpy as np

from django.http import JsonResponse, HttpResponse
from .generate_image import generateCartoonImage

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)

class manGANAPIView(views.APIView):
    serializer_class = manGANSerializer
    http_method_names = ['get', "post",'head', "options"]

    
    def get(self, request, format=None):
        return send_image(request)

    def post(self, request, format=None):
        return send_image(request)


def send_image(request_):
    # curl -X GET -H "Content-Type: multipart/form-data" -F "style=hayao" -F "file=@./sample_data/memory.jpg" 127.0.0.1:8000/api/
    # 上記コマンドでraspberry piから送信
    # https://stackoverflow.com/questions/47515243/reading-image-file-file-storage-object-using-cv2
    # read methodが必要
    logger.info("API is requested")
    try:
         # image file
        
        import json
        import base64
        
        # form-data type
        dict_res = request_.data
        # json.loads(request_.body)
        
        expected_datatype = (django.core.files.uploadedfile.InMemoryUploadedFile, django.core.files.uploadedfile.TemporaryUploadedFile)
        assert isinstance(dict_res.get("file"), expected_datatype) & isinstance(dict_res.get("style"), str)
        # 1. make an image asarray.``
        # BytesIO(base64.b64decode(dict_res["file"]))
        # Image.open(BytesIO(base64.b64decode(dict_res["file"])))
        binaryImage = dict_res["file"]
        # binaryImage = base64.b64decode(dict_res["file"].split(",")[1])
        # binaryImage = base64.b64decode(dict_res["file"])
        # binaryImage = base64.urlsafe_b64decode(dict_res["file"])
        # binaryImage = BytesIO(dict_res["file"].read())
        style = dict_res["style"]

        # from urllib import request
        # with request.urlopen(data_uri) as response:
        #     binaryImage = response.read()
        # 2. prediction
        generated_img = generateCartoonImage(binaryImage, style)
        # generated_img = generated_img.transpose((1, 2, 0))
        # generated_img = generated_img.astype("int")

        # 3. convert the generated_img to binary format
        # https://chiyoh.hatenablog.com/entry/2019/05/04/145639
        # sendtoimageasbinary file

        output = BytesIO()
        bin_generated_img = Image.fromarray(generated_img, 'RGB')
        bin_generated_img.save(output, format='JPEG')
        
    except Exception as exc:
        logger.error(f'Something went wrong! {exc}')
        raise ImageHandlingError(exc)
    # 4. create HTTPREsponse
    # TODO:bin_imgをcloud storageに格納してurlを送付 or binary dataを直接送る
    response = HttpResponse(
        # base64.b64encode()
        encode_b64(output.getvalue()),
        content_type="image/png"
        )
    response['Access-Control-Allow-Origin'] = '*'
    return response

# import mimetypes
from base64 import b64decode, b64encode

def encode_b64(value):
    # value.file.seek(0)
    # mime_type, encoding = mimetypes.guess_type(value.name)
    # if not mime_type:
    mime_type = 'image/png'
    data = value
    image_data = bytes(
        'data:' + mime_type + ';base64,', encoding='UTF-8'
        ) + b64encode(data)
    return image_data  # or str(image_data, 'utf-8')

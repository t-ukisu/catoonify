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

from PIL import Image
from io import BytesIO
import numpy as np

from django.http import JsonResponse, HttpResponse

class manGANAPIView(views.APIView):
    serializer_class = manGANSerializer
    http_method_names = ['get', 'head']

    
    def get(self, request, format=None):
        return send_image(request)



def send_image(request):
    # curl -X GET -H "Content-Type: multipart/form-data" -F "style=hayao" -F "file=@./sample_data/memory.jpg" 127.0.0.1:8000/api/
    # 上記コマンドでraspberry piから送信
    # https://stackoverflow.com/questions/47515243/reading-image-file-file-storage-object-using-cv2
    # read methodが必要
    # import pdb; pdb.set_trace()
    try:
         # image file
        expected_datatype = (django.core.files.uploadedfile.InMemoryUploadedFile, django.core.files.uploadedfile.TemporaryUploadedFile)
        assert isinstance(request.data.get("file"), expected_datatype) & isinstance(request.data.get("style"), str)
        # 1. make an image asarray.
        img = Image.open(BytesIO(request.data["file"].read()))
        img = np.asarray(img)

        style = request.data["style"]

        # 2. prediction
        # generated_img = manGAN.predict(img_array)
        # img = img - 0.5

        # 3. convert the generated_img to binary format
        # https://chiyoh.hatenablog.com/entry/2019/05/04/145639
        # sendtoimageasbinary file

        output = BytesIO()
        bin_img = Image.fromarray(img, 'RGB')
        bin_img.save(output, format='JPEG')
        
        

        # 4. create JSONREsponse
        # bin_imgをcloud storageに格納してurlを送付
        # or binary dataを直接送る
        from django.template.loader import render_to_string
        # context = {"data":bin_img}
        # content_data_string = render_to_string(None, context ,request)
        # json_data = { "content" : content_data_string }
        # generated_img 
        # JSONResponse()
    except Exception as exc:
        raise ImageHandlingError(exc)
    return HttpResponse(output.getvalue(), content_type="image/png")


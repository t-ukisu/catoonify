from django.shortcuts import render

from django.views.generic import ListView
from rest_framework import generics

from serializers import manGANSerializer
# Create your views here.


class manGANAPIView(generics.ListAPIView):
    serializer_class = manGANSerializer

 def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)
            send_image(request)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(self, request.method.lower(),
                                  self.http_method_not_allowed)
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)
        

        self.response = self.finalize_response(request, response, *args, **kwargs)
        return self.response




def send_image(request):
    # curl -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/pi/Desktop/image.jpg" 100.64.1.11:5000/send_image
    # 上記コマンドでraspberry piから送信
    # https://stackoverflow.com/questions/47515243/reading-image-file-file-storage-object-using-cv2
    # read methodが必要
    import pdb; pdb.set_trace()
    image = request.files["file"].read()
    # https://teratail.com/questions/222843
    img = Image.open(BytesIO(image))
    # flipped_img = ImageOps.flip(img)
    # flipped_img.save("image.jpg")

    # 1. make an image asarray.

    # 2. prediction
    # generated_img = manGAN.predict(img_array)

    # 3. convert the generated_img to binary format
    # sendtoimageasbinary file

    # 4. create JSONREsponse
    # generated_img 
    # JSONResponse()
    return JSONResponse()


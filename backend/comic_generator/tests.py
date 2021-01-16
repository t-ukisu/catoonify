from django.test import TestCase


from .views import send_image
# Create your tests here.


class GANAPITests(TestCase):
    def test_api(self):
        """
        requestをhttp://localhost:8000/api/ に送り、test_sampleに格納される写真が帰ってくるか確かめる。
        """
        imagebinary_data = ""
        request = {"file": imagebinary_data}
        actual_img = send_image(request)
        self.assertEqual(actual_img, expected_img)
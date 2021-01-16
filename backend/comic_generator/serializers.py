from rest_framework import serializers


class manGANSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("generated_image",)
# """Picture serializers."""

# # Django REST Framework
# from rest_framework import serializers

# # Models
# from apps.publications.models import Picture

# # Utils
# from apps.utils.serializers import DynamicFieldsModelSerializer

# class PictureModelSerializer(DynamicFieldsModelSerializer):
#     """Picture model serializer."""

#     class Meta:
#         model = Picture
#         fields = ('id', 'picture', 'publication',)
#         read_only_fields = ('publication',)

#     def create(self, data):
#         """Handle picture creation."""
#         return Picture.objects.create(**data, publication=self.context['publication'])

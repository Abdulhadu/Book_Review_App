import jwt
from django.conf import settings
from rest_framework import serializers, authentication, exceptions
from rest_framework.fields import get_attribute
from rest_framework.relations import MANY_RELATION_KWARGS
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet


from Auth.models import Auth


class EricViewSet(ModelViewSet):
    pass

class FilterableRelatedFieldMixin:
    @classmethod
    def many_init(cls, *args, **kwargs):
        """
        Taken directly from DRF.
        """
        get_relationship = kwargs.pop("get_relationship", None)
        list_kwargs = {"child_relation": cls(*args, **kwargs)}
        for key in kwargs:
            if key in MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return ManyRelatedField(**list_kwargs, get_relationship=get_relationship)
    
class ManyRelatedField(serializers.ManyRelatedField):
    def __init__(self, child_relation=None, get_relationship=None, *args, **kwargs):
        self.get_relationship = get_relationship
        super().__init__(child_relation=child_relation, *args, **kwargs)
    def get_attribute(self, instance):
        if hasattr(instance, "pk") and instance.pk is None:
            return []
        relationship = get_attribute(instance, self.source_attrs)
        if getattr(self, "get_relationship") is not None:
            return self.get_relationship(relationship)
        return relationship.all() if hasattr(relationship, "all") else relationship

class PrimaryKeyRelatedField(FilterableRelatedFieldMixin, serializers.PrimaryKeyRelatedField):
    pass

class EricModelSerializer(ModelSerializer):
    serializer_field_mapping = {
        **ModelSerializer.serializer_field_mapping,
    }
    serializer_related_field = PrimaryKeyRelatedField
    
    

    
def generate_jwt_token(useremail):
    payload = {
        'Email': useremail
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token

class testclass():
    pass
    


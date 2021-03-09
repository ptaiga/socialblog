import json
import base64

from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from django import forms
from django.core import serializers
from django.forms.models import model_to_dict

from django.contrib.auth import authenticate

from jsonschema import validate
from jsonschema.exceptions import ValidationError

from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow import ValidationError as MarshValidationError

from .models import Item, Review


### jsonschema ###

# ADD_ITEM_SCHEMA = {
#     '$schema': 'http://json-schema.org/schema#',
#     'type': 'object',
#     'properties': {
#         'title': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 64,
#         },
#         'description': {
#             'type': 'string',
#             'minLength': 1,
#             'maxLength': 1024,
#         },
#         'price': {
#             'type': 'integer',
#             'minimum': 1,
#             'maximum': 1000000,
#         },
#     },
#     'required': ['title', 'description', 'price'],
# }


# @method_decorator(csrf_exempt, name='dispatch')
# class AddItemView(View):
#     """ View for adding product """

#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             data['price'] = int(data.get('price'))
#             validate(data, ADD_ITEM_SCHEMA)
#             item = Item.objects.create(**data)
#             return JsonResponse({"id": item.pk}, status=201)
#         except ValueError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except TypeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON'}, status=400)
#         except ValidationError as err:
#             return JsonResponse({'error': err.message}, status=400)


### Django Forms ###

class StrictChar(forms.CharField):

    def to_python(self, value):
        if not isinstance(value, str):
            raise forms.ValidationError('Title must be a string!')
        return value


class AddItemForm(forms.Form):
    title = StrictChar(max_length=64)
    description = StrictChar(max_length=1024)
    price = forms.DecimalField(min_value=0, max_value=1000000, decimal_places=0)

    # title = forms.CharField(max_length=64)
    # description = forms.CharField(max_length=1024)
    # price = forms.DecimalField(max_value=1000000, decimal_places=0)
    # def clean(self):
    #     data = self.cleaned_data
    #     print(self.data)
    #     if not isinstance(self.data['title'], str) or \
    #        not isinstance(self.data['description'], str):
    #         raise forms.ValidationError('Title must be a string!')
    #     return data


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """ View for adding product """

    def post(self, request):

        try:
            authorization = request.META['HTTP_AUTHORIZATION']
            basic, credential = authorization.split()
            if basic.lower() != 'basic':
                return JsonResponse({}, status=401)
            username, password = base64.b64decode(credential) \
                                    .decode('utf-8').split(':')
            user = authenticate(request, username=username, password=password)
        except (ValueError, KeyError):
            return JsonResponse({}, status=401)
        if user is None:
            return JsonResponse({}, status=401)
        if not user.is_staff:
            return JsonResponse({}, status=403)
        if request.content_type != 'application/json':
            return JsonResponse({'error': 'Invalid content type'}, status=400)

        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        form = AddItemForm(data)
        if form.is_valid():
            item = Item.objects.create(**form.cleaned_data)
            return JsonResponse({"id": item.pk}, status=201)
        else:
            return JsonResponse({'errors': form.errors}, status=400)


class PostReviewSchema(Schema):
    text = fields.Str(validate=Length(1, 1024))
    grade = fields.Int(validate=Range(1, 10))


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """ View for adding product review """

    def post(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        try:
            schema = PostReviewSchema(strict=True)
            data = schema.loads(request.body)
            review = Review.objects.create(item=item, **data.data)
            return JsonResponse({"id": review.pk}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except MarshValidationError as err:
            return JsonResponse({"errors": err.messages}, status=400)


class GetItemView(View):
    """ View for getting product information (and 5 last reviews) """

    def get(self, request, item_id):
        item = get_object_or_404(Item, pk=item_id)
        data = model_to_dict(item)
        reviews = item.review_set.all().order_by("-pk")[:5]
        # reviews_dict = serializers.serialize('json', reviews)
        reviews_list=[]
        for rev in reviews:
            reviews_list.append(model_to_dict(rev, 
                fields=('id', 'text', 'grade')))
        data['reviews'] = reviews_list
        return JsonResponse(data, status=200)

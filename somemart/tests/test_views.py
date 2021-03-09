import json
import base64

from somemart.models import Item, Review
# from .factories import ItemFactory, ReviewFactory
from django.contrib.auth.models import User


class TestViews(object):

    def setup(self):
        u = User.objects.create_user('user1', 'u@gmail.com', 'user1')
        u.is_staff = True
        u.save()
        self.auth_header_admin = {
            'HTTP_AUTHORIZATION': 'basic ' + \
            base64.b64encode('user1:user1'.encode('ascii')).decode('utf-8')
            # dXNlcjE6dXNlcjE=
        }

        User.objects.create_user('user', 'u@gmail.com', 'user').save()
        self.auth_header_user = {
            'HTTP_AUTHORIZATION': 'basic ' + \
            base64.b64encode('user:user'.encode('ascii')).decode('utf-8')
            # dXNlcjp1c2Vy
        }

        self.url = '/api/v1/goods/'
        self.data = {
            'title': 'Cheese',
            'description': 'Very tasty cheese',
            'price': 100
        }

    def test_post_item_1(self, client, db):
        """ /api/v1/goods/ (POST) save product to DB """
        response = client.post(self.url, data=json.dumps(self.data),
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 201
        document = response.json()
        # Product is saved
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Cheese'
        assert item.description == 'Very tasty cheese'
        assert item.price == 100

    def test_post_item_2(self, client, db):
        """ Check content type """
        response = client.post(self.url, data=json.dumps(self.data),
            content_type='text/html', **self.auth_header_admin)
        assert response.status_code == 400

    def test_post_item_3(self, client, db):
        """ Check data restrictions """
        data = json.dumps({
            'title': 'Cheese',
            'price': 100
        })
        response = client.post(self.url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 400

    def test_post_item_4(self, client, db):
        """ Check data restrictions """
        data = json.dumps({
            'title': 'Cheese',
            'description': 'Very tasty cheese',
            'price': -100
        })
        response = client.post(self.url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 400

    def test_post_item_5(self, client, db):
        """ Check data restrictions """
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Cheese',
            'description': 'Rather good tasty',
            'price': 'xyz'
        })
        response = client.post(self.url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 400

    def test_post_item_6(self, client, db):
        """ Check data restrictions """
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 10,
            'description': 'Rather good tasty',
            'price': 100
        })
        response = client.post(self.url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 400

    def test_post_item_7(self, client, db):
        """ Check admin's rights """
        response = client.post(self.url, data=json.dumps(self.data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'basic dXNlcjp1c2Vy'})
        assert response.status_code == 403

    def test_post_item_8(self, client, db):
        """ Check authentication """
        response = client.post(self.url, data=json.dumps(self.data),
            content_type='application/json',
            **{'HTTP_AUTHORIZATION': 'basic dXNlcjp1c2VyNQ=='})
        assert response.status_code == 401

    def test_get_item(self, client, db):
        """(GET) /api/v1/goods/:id/ - get product info"""
        url = '/api/v1/goods/1/'
        response = client.get(url, content_type='application/json')
        assert response.status_code == 404

    def test_post_review_1(self, client, db):
        """(POST) /api/v1/goods/:id/reviews/ - add review to product"""
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Cheese',
            'description': 'Rather good tasty',
            'price': '200'
        })
        response = client.post(url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 201
        document = response.json()
        # Product is saved
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Cheese'
        assert item.description == 'Rather good tasty'
        assert item.price == 200

        url = '/api/v1/goods/' + str(document['id']) + '/reviews/'
        data = json.dumps({
            'text': 'Not bad.',
            'grade': 6
        })
        response = client.post(url, data=data,
            content_type='application/json')
        assert response.status_code == 201
        document = response.json()
        # Review is saved
        review = Review.objects.get(pk=document['id'])
        assert review.item == item
        assert review.text == 'Not bad.'
        assert review.grade == 6

    def test_post_review_2(self, client, db):
        """(POST) /api/v1/goods/:id/reviews/ - add review to product """
        url = '/api/v1/goods/'
        data = json.dumps({
            'title': 'Cheese',
            'description': 'Rather good tasty',
            'price': '200'
        })
        response = client.post(url, data=data,
            content_type='application/json', **self.auth_header_admin)
        assert response.status_code == 201
        document = response.json()
        # Product is saved
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Cheese'
        assert item.description == 'Rather good tasty'
        assert item.price == 200

        url = '/api/v1/goods/' + str(document['id']) + '/reviews/'
        data = json.dumps({
            'text': 'Not bad.',
            'grade': None
        })
        response = client.post(url, data=data, 
            content_type='application/json')
        assert response.status_code == 400

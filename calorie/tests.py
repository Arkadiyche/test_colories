from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from calorie.models import Activity, Dish, Person, PersonActivity, PersonDish
from calorie.serializer import ActivitySerializer, PersonSerializer, DishSerializer
from rest_framework import status

# Create your tests here.

class ActivityTestCase(APITestCase):
    data = {"id": 1, "name": "Beg", "calorie_content": 200, "unit":'Км'}
    def setUp(self):
        self.activity = Activity.objects.create(**self.data)
        self.activity.save()
        self.client = APIClient()

    def test_create_activity(self):
        """Test that activity created
        """
        response = self.client.post('/api/activity/', format='json', data=self.data)
        status_code = response.status_code 
        data = response.json()
        self.data['id'] = data['id']
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)

    def test_put_activity(self):
        """Test put activity
        """
        response = self.client.put('/api/activity/', format='json', data=self.data)
        status_code = response.status_code 
        data = response.json()
        self.data['id'] = data['id']
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)

    def test_delte_activity(self):
        """Test delete activity
        """
        response = self.client.delete('/api/activity/', format='json', data=self.data)
        status_code = response.status_code 
        self.assertEqual(status_code, status.HTTP_200_OK)


class DishTestCase(APITestCase):
    data = {"id": 1, "name": "яйцо", "calorie_content": 200, "serving_weight": 100}
    def setUp(self):
        self.dish = Dish.objects.create(**self.data)
        self.dish.save()
        self.client = APIClient()

    def test_create_dishes(self):
        """Test that activity created
        """
        response = self.client.post('/api/dish/', format='json', data=self.data)
        status_code = response.status_code 
        data = response.json()
        self.data['id'] = data['id']
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)

    def test_put_dishes(self):
        """Test put activity
        """
        response = self.client.put('/api/dish/', format='json', data=self.data)
        status_code = response.status_code 
        data = response.json()
        self.data['id'] = data['id']
        self.assertEqual(status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), self.data)

    def test_delte_activity(self):
        """Test delete activity
        """
        response = self.client.delete('/api/dish/', format='json', data=self.data)
        status_code = response.status_code 
        self.assertEqual(status_code, status.HTTP_200_OK)

class ActionActivityTestCase(APITestCase):
    data = {"id": 1, "name": "Beg", "calorie_content": 200, "unit":'Км'}
    def setUp(self):
        self.activity = Activity.objects.create(**self.data)
        #self.activity=1
        self.activity.save()
        self.person = Person.objects.create(surname="A", first_name="b", patronymic="C", height=200, weight=100, age=20)
        #self.person=1
        self.person.save()
        self.client = APIClient()

    def ttest_create_ActionActivity(self):#TO DO переделать
        """Test that activity created
        """
        response = self.client.post('/api/activity/', format='json', data={
                                                        "person":  PersonSerializer(self.person).data,
                                                        "activity": ActivitySerializer(self.activity).data,
                                                        "date": "2021-01-10T21:34",
                                                        "duration": 2
                                                })
        status_code = response.status_code 
        print(response.json())
        self.assertEqual(status_code, status.HTTP_200_OK)


class ActionTestCase(APITestCase):
    data_activity = {"id": 1, "name": "Beg", "calorie_content": 200, "unit":'Км'}
    data_dish = {"id": 1, "name": "яйцо", "calorie_content": 200, "serving_weight": 100}
    def setUp(self):
        self.activity = Activity.objects.create(**self.data_activity)
        #self.activity=1
        self.activity.save()
        self.dish = Dish.objects.create(**self.data_dish)
        self.dish.save()
        self.person = Person.objects.create(surname="A", first_name="b", patronymic="C", height=200, weight=100, age=20)
        self.person.save()
        self.action_activity = PersonActivity.objects.create(person=self.person, activity=self.activity, date="2021-01-10T21:34", duration=2)
        self.action_activity.save()

    def test_get_stats(self):
        """get stats by person"""
        response = self.client.post('/api/stat/', format='json', data={
                                                            "person_id": 1,
                                                            "period": {
                                                                "start": "2021-01-07T21:34",
                                                                "end": "2021-01-12T21:34"
                                                            }})
        status_code = response.status_code 
        print(response.json())
        self.assertEqual(status_code, status.HTTP_200_OK)
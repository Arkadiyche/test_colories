from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from calorie.models import Activity, Dish, Person, PersonActivity, PersonDish
from calorie.serializer import ActivitySerializer, DishSerializer, PersonActivitySerializer, PersonDishSerializer, ActivitiesListSerializer, DishesListSerializer, RequestStatsSerializer, PersonSerializer
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import dateutil.parser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
@api_view(['GET'])
def index(request):
    """Returns an index message"""
    return JsonResponse({'message': 'You\'re at competitions index!'})


class ActivityView(APIView):
    @classmethod
    def get_activity_by_id(self, id):
        """
        Returns the competition by its id or raises 404
        """
        try:
            return Activity.objects.get(id=id)
        except ObjectDoesNotExist:
            raise ValidationError('Could not retrieve activity with specified id')

    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='name', in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='поиск по части имени'
        ),]
        , responses={
        status.HTTP_200_OK: ActivitiesListSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='get activity by name')
    def get(self, request):
        """Get information about activity by name
        :name (str, query)
        """
        try:
            name = request.GET.get('name')
        except ValueError:
            raise ValidationError('expected query param "name"')
        query_set = Activity.objects.filter(name__icontains=name)
        activities = list([c for c in query_set.values()])

        return JsonResponse({
            "total": query_set.count(),
            "activities": activities,
        })

    @swagger_auto_schema(request_body=ActivitySerializer, responses={
        status.HTTP_200_OK: ActivitySerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='post activity')
    def post(self, request):
        """post activity
        :name (str)
        :calorie_content (int)
        :unit (str)
        """
        activity = ActivitySerializer(data=request.data)

        if activity.is_valid(raise_exception=True):
            activity.save()
            return JsonResponse(activity.data, safe=False)
    
    @swagger_auto_schema(request_body=ActivitySerializer, responses={
        status.HTTP_200_OK: ActivitySerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='edit activity')
    def put(self, request):
        """update activity by id
        :id (int)
        :name (str)
        :calorie_content (int)
        :unit (str)
        """
        try:
            id = request.data.get('id')
        except ValueError:
            raise ValidationError('expected "id"')
        activity=self.get_activity_by_id(id)
        serializer=ActivitySerializer(activity, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)


    @swagger_auto_schema(request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=1)
                        }
                        ), responses={
        status.HTTP_200_OK: 'OK',
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='delete activity')
    def delete(self, request):
        """delete activity by id
        :id (int)
        """
        try:
            id = request.data.get('id')
        except ValueError:
            raise ValidationError('expected "id"')
        activity=self.get_activity_by_id(id)
        activity.delete()
        return HttpResponse(status=status.HTTP_200_OK)
        

class DishView(APIView):
    @classmethod
    def get_dish_by_id(self, id):
        """
        Returns the competition by its id or raises 404
        """
        try:
            return Dish.objects.get(id=id)
        except ObjectDoesNotExist:
            raise ValidationError('Could not retrieve dish with specified id')


    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter(
            name='name', in_=openapi.IN_QUERY,
            type=openapi.TYPE_STRING,
            description='поиск по части имени'
        ),]
        , responses={
        status.HTTP_200_OK: DishesListSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='get dish by name')
    def get(self, request):
        """Get information about dish by name
        :name (str, query)
        """
        try:
            name = request.GET.get('name')
        except ValueError:
            raise ValidationError('expected query param "name"')
        query_set = Dish.objects.filter(name__icontains=name)
        dishes = list([c for c in query_set.values()])
        return JsonResponse({
            "total": query_set.count(),
            "dishes": dishes,
        })
    

    @swagger_auto_schema(request_body=DishSerializer, responses={
        status.HTTP_200_OK: DishSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='Post dish')
    def post(self, request):
        """post dish
        :name (str)
        :calorie_content (int)
        :serving_weight (str)
        """
        dish = DishSerializer(data=request.data)

        if dish.is_valid(raise_exception=True):
            dish.save()
            return JsonResponse(dish.data, safe=False)

    @swagger_auto_schema(request_body=DishSerializer, responses={
        status.HTTP_200_OK: DishSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='edit dish')
    def put(self, request):
        """update dish by id
        :id (int)
        :name (str)
        :calorie_content (int)
        :serving_weight (str)
        """
        try:
            id = request.data.get('id')
        except ValueError:
            raise ValidationError('expected "id"')
        dish=self.get_dish_by_id(id)
        serializer=DishSerializer(dish, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)

    @swagger_auto_schema(request_body=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                        'id': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=1)
                        }
                        ), responses={
        status.HTTP_200_OK: 'OK',
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='delete dish')
    def delete(self, request):
        """delete dish by id
        :id (int)
        """
        try:
            id = request.data.get('id')
        except ValueError:
            raise ValidationError('expected "id"')
        dish=self.get_dish_by_id(id)
        dish.delete()
        return HttpResponse(status=status.HTTP_200_OK)


class ActivityActionView(APIView):
    @swagger_auto_schema(request_body=PersonActivitySerializer, responses={
        status.HTTP_200_OK: PersonActivitySerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='Post Action activity')
    def post(self, request):
        """post information about activity action
        :person (int, id)
        :activity (int, id)
        :date (str isoformat YYYY-MM-DDThh:mm)
        :duration (int)
        """
        serializer = PersonActivitySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return JsonResponse(serializer.data, safe=False)


class DishActionView(APIView):
    @swagger_auto_schema(request_body=PersonDishSerializer, responses={
        status.HTTP_200_OK: PersonDishSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='Post Action activity')
    def post(self, request):
        """post information about dish action
        :person (int, id)
        :dish (int, id)
        :date (str isoformat YYYY-MM-DDThh:mm)
        :amount (int)
        """
        serializer = PersonDishSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        return JsonResponse(serializer.data, safe=False)


@swagger_auto_schema(method='post',request_body=RequestStatsSerializer, responses={
        status.HTTP_200_OK: openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                        'total_activities': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=3
                        ),
                        'total_dishes': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=2
                        ),
                        'actions': openapi.Schema(
                            type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_STRING, description='Набор actions и dishes')
                        ),
                        }
                    )
                ,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='stats by person')
@api_view(['POST'])
def get_stats(request):
    """Returns stats by person_id
    :person_id
    :period (object, start and end datetime(isoformat))"""
    filter = {}
    all = []
    try:
        filter['person_id'] = request.data.get('person_id')
        period = request.data.get('period')
    except ValueError:
        raise ValidationError('expected params "person_id" and "period"')
    try:
        filter['date__gte'] = dateutil.parser.parse(period.get('start'))
        filter['date__lte'] = dateutil.parser.parse(period.get('end'))
    except Exception:
        raise ValidationError('expected params "start" and "start" in period')
    query_set_activities = PersonActivity.objects.filter(**filter)
    activities = []
    for c in query_set_activities.values():
        c['activity'] = Activity.objects.filter(id=c.pop('activity_id')).values()[0]
        c['total_colories'] = c['activity']['calorie_content']*c['duration']
        activities.append(c)
    query_set_dishes = PersonDish.objects.filter(**filter)
    dishes = []
    for c in query_set_dishes.values():
        c['dish'] = Dish.objects.filter(id=c.pop('dish_id')).values()[0]
        c['total_colories'] = c['dish']['calorie_content']*c['amount']
        c['total_weight'] = c['dish']['serving_weight']*c['amount']
        dishes.append(c)
    all = activities + dishes
    return JsonResponse({
            "total_activities": query_set_dishes.count(),
            "total_dishes": query_set_dishes.count(),
            "actions": all,
        })


@swagger_auto_schema(method='post',request_body=RequestStatsSerializer, responses={
        status.HTTP_200_OK: openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                        'received': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=1000
                        ),
                        'spent': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=500
                        ),
                        'diff': openapi.Schema(
                            type=openapi.TYPE_INTEGER, example=500
                        )
                        }
                    )
                ,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='calories by person')
@api_view(['POST'])
def get_person_calories(request):
    """Returns received, spent, diff calories
    :person_id
    :period (object, start and end datetime(isoformat))"""
    filter = {}
    total_calories_received = 0
    total_calories_spent = 0
    try:
        filter['person_id'] = request.data.get('person_id')
        period = request.data.get('period')
    except ValueError:
        raise ValidationError('expected params "person_id" and "period"')
    try:
        filter['date__gte'] = dateutil.parser.parse(period.get('start'))
        filter['date__lte'] = dateutil.parser.parse(period.get('end'))
    except Exception:
        raise ValidationError('expected params "start" and "start" in period')
    query_set_activities = PersonActivity.objects.filter(**filter)
    for c in query_set_activities.values():
        activity = Activity.objects.filter(id=c.pop('activity_id')).values()[0]
        total_calories_spent = total_calories_spent + activity['calorie_content']*c['duration']
    query_set_dishes = PersonDish.objects.filter(**filter)
    for c in query_set_dishes.values():
        dish = Dish.objects.filter(id=c.pop('dish_id')).values()[0]
        total_calories_received = total_calories_received + dish['calorie_content']*c['amount']
    return JsonResponse({
            "received": total_calories_received,
            "spent": total_calories_spent,
            "diff": total_calories_received-total_calories_spent,
        })


@swagger_auto_schema(method='post', request_body=PersonSerializer, responses={
        status.HTTP_200_OK: PersonSerializer,
        status.HTTP_400_BAD_REQUEST: 'Bad Request'}, operation_description='create person')
@api_view(['POST'])
def create_person(request):

    person = PersonSerializer(data=request.data)

    if person.is_valid(raise_exception=True):
        person.save()
        return JsonResponse(person.data, safe=False)

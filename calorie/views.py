from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.views import APIView
from calorie.models import Activity, Dish, Person, PersonActivity, PersonDish
from calorie.serializer import ActivitySerializer, DishSerializer, PersonActivitySerializer, PersonDishSerializer
from rest_framework.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
import dateutil.parser

# Create your views here.
@api_view(['GET'])
def index(request):
    """Returns an index message"""
    return JsonResponse({'message': 'You\'re at competitions index!'})


class ActivityView(APIView):
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


class DishView(APIView):
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
            "activities": dishes,
        })
    
    def post(self, request):
        """post activity
        :name (str)
        :calorie_content (int)
        :unit (str)
        """
        dish = DishSerializer(data=request.data)

        if dish.is_valid(raise_exception=True):
            dish.save()
            return JsonResponse(dish.data, safe=False)


class ActivityActionView(APIView):
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

@api_view(['POST'])
def get_stats(request):
    """Returns an index message
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



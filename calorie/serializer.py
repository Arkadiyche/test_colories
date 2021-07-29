from rest_framework import serializers
from calorie.models import Person, Activity, Dish, PersonActivity, PersonDish

class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Person
        fields='__all__'

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=Activity
        fields='__all__'

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model=Dish
        fields='__all__'

class PersonActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model=PersonActivity
        fields='__all__'

class PersonDishSerializer(serializers.ModelSerializer):
    class Meta:
        model=PersonDish
        fields='__all__'
from django.contrib import admin
from calorie.models import Person, Activity, Dish, PersonActivity, PersonDish

# Register your models here.
admin.site.register(Person)
admin.site.register(Activity)
admin.site.register(Dish)
admin.site.register(PersonActivity)
admin.site.register(PersonDish)
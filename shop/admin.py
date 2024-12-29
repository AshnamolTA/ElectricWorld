from django.contrib import admin

from shop.models import Brand,LightBodyColour,Shape,LightColour,Material,Category,Wates,Light

# Register your models here.

admin.site.register(Category)
admin.site.register(LightBodyColour)
admin.site.register(LightColour)
admin.site.register(Shape)
admin.site.register(Brand)
admin.site.register(Material)
admin.site.register(Wates)
admin.site.register(Light)

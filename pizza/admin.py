from django.contrib import admin
from .models import Pizza, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  
    search_fields = ('name',)  


@admin.register(Pizza)
class PizzaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category')  
    list_filter = ('category',)  
    search_fields = ('name', 'description')  
    list_editable = ('price',)  
    readonly_fields = ('image_preview',)  

    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'price', 'category')
        }),
        ('Изображение', {
            'fields': ('image', 'image_preview'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="150" height="150" style="object-fit: contain;" />'
        return 'Нет изображения'
    image_preview.allow_tags = True
    image_preview.short_description = 'Превью изображения'

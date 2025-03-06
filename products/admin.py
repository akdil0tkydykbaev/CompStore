from django.contrib import admin
from .models import Category, Product, Review
from rangefilter.filters import NumericRangeFilter  # Убедитесь, что пакет установлен!

class PriceRangeFilter(admin.SimpleListFilter):
    title = "Диапазон цен"
    parameter_name = 'price_range'

    def lookups(self, request, model_admin):
        return (
            ('0-500', 'До 500'),
            ('500-1000', '500–1000'),
            ('1000-5000', '1000–5000'),
        )

    def queryset(self, request, queryset):
        value = self.value()
        if value == '0-500':
            return queryset.filter(price__range=(0, 500))
        elif value == '500-1000':
            return queryset.filter(price__range=(500, 1000))
        elif value == '1000-5000':
            return queryset.filter(price__range=(1000, 5000))
        return queryset  # Важно: возвращаем исходный queryset, если фильтр не выбран

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at')
    list_filter = (
        ('price', NumericRangeFilter),  # Фильтр "от-до"
        PriceRangeFilter,                # Фильтр с фиксированными диапазонами
        'categories'
    )
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)
    autocomplete_fields = ['categories']  # Работает только если в CategoryAdmin есть search_fields

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)  # Необходимо для autocomplete_fields в ProductAdmin

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating',)
    raw_id_fields = ('product', 'user')
import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    price_range = django_filters.NumericRangeFilter(
        field_name='price',
        lookup_expr='range',
        label="Диапазон цен (например: 100-500)"
    )

    class Meta:
        model = Product
        fields = {
            'categories': ['exact'],
        }
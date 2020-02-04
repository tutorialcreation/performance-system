from pams_system.models.levels import KPIWeightings, KPIWeight, InputData
import django_filters


class WeightFilter(django_filters.FilterSet):
    weight__gt = django_filters.NumberFilter(field_name='weight', lookup_expr='gt')
    weight__lt = django_filters.NumberFilter(field_name='weight', lookup_expr='lt')

    class Meta:
        model = KPIWeightings
        fields = {
            'effective_date': ['year'],
        }

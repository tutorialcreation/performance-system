from pams_system.models.levels import KPIWeightings, KPIWeight, InputData
from pams_system.models.kpis import KpiValue,KpiValueset
import django_filters


class WeightFilter(django_filters.FilterSet):
    # weight__gt = django_filters.NumberFilter(field_name='weight', lookup_expr='gt')
    # weight__lt = django_filters.NumberFilter(field_name='weight', lookup_expr='lt')

    class Meta:
        model = KPIWeightings
        fields = {
            'effective_date': ['lte'],
        }

class ValueFilter(django_filters.FilterSet):
    class Meta:
        model = InputData
        fields = ['name' ]

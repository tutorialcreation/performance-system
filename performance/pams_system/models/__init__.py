from .levels import (
    InputData,
    Level,
    MainLevel,
)
from .maps import (
    Map,
    MapList,
    MapType,
)

from .kpis import (
    KpiTypes,
    KpiIndividual,
    KpiDates,
    KpiValue,
    KpiWeights
)

__all__ = [
    # models for levels
    'InputData',
    'Level',
    'MainLevel',
    # models for maps
    'Map',
    'MapType',
    'MapList',
    # models for kpis
    'KpiTypes',
    'KpiUser',
    'KpiDates',
    'KpiValue',
    'KpiWeights',
]

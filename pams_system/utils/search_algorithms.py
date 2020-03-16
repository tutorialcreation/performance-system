import os, sys
import itertools

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django

django.setup()

from pams_system.models.levels import InputData, KPIWeightings
from django.db.models import Q,F
from datetime import date, datetime
from django.db import connection
import pandas as pd

# query = str(InputData.objects.all().query)
# df = pd.read_sql_query(query, connection)
# # data cleaning
# df[['value_date']] = df[['value_date']].astype(object).where(df[['value_date']].notnull(), None)


def get_kpis(matching_string):
    data = InputData.objects.filter(name=matching_string)
    pk = []
    number_of_levels = []
    levelset = []
    for i in range(0, len(data)):
        pk.append(data[i].pk)
        number_of_levels.append(data[i].number_of_levels)
        levelset.append(data[i].levelset_id)
    upscale = 1
    tree_id = [x + upscale for x in number_of_levels]
    if matching_string == None:
        tree_id = [0]
        levelset = [0]
        pk = [0]
    else:
        tree_id = tree_id
        levelset = levelset
        pk = pk
    kpi_query = InputData.objects.filter(Q(number_of_levels=tree_id[0]) & Q(parent_id=pk[0]) & Q(levelset_id=levelset[0]))
    return kpi_query


def get_value_dates(matching_string):
    data = InputData.objects.filter(name__iexact=matching_string)
    value_dates = []
    for i in range(0, len(data)):
        value_dates.append(data[i].value_date)    # li = list(itertools.chain.from_iterable(value_dates))
    # import  pdb; pdb.set_trace()
    return list(itertools.chain.from_iterable(value_dates))


def check(list1, val):
    return(all(x > val for x in list1))

def get_weights(matching_string):
    dataset = KPIWeightings.objects.filter(content_id__name__exact=matching_string)
    dates = [v.effective_date for v in dataset]
    value_dataset = InputData.objects.filter(name__exact=matching_string)
    match_dates = [v.value_date for v in value_dataset]

    nearest_val = []
    for date_ in dates:
        match_date_list = [match for match in match_dates if [date_] <= match]
        if match_date_list:
            nearest_val.append(date_)
    cleaned_weights = ''
    if nearest_val:
        latest_date = sorted(nearest_val)[-1]
        query_2 = KPIWeightings.objects.filter(effective_date=latest_date).values("final_weight").annotate(weight_kpi=F("content_id__name"),created=F("created_at"))
        df_2 = pd.DataFrame(query_2)
        cleaned_weights = df_2.dropna()
        exact_weight = cleaned_weights[(cleaned_weights['weight_kpi'])==matching_string]
        sorted_weights = exact_weight.sort_values(by="created")
        latest_weight = pd.DataFrame(sorted_weights.iloc[-1]).transpose()
        return latest_weight

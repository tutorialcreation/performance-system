import os, sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
import django

django.setup()

from pams_system.models import InputData
from django.db import connection
import pandas as pd

query = str(InputData.objects.all().query)
df = pd.read_sql_query(query, connection)
# data cleaning
df[['value_date']] = df[['value_date']].astype(object).where(df[['value_date']].notnull(), None)


def get_value_dates(matching_string):
    required_data = df[df['name'].str.contains(matching_string)]
    preprocessed_value_dates = required_data['value_date']
    cleaned_value_dates = preprocessed_value_dates.reset_index()
    cleaned_value_dates.columns = ['indices', 'value_dates']
    return cleaned_value_dates


def return_full_row(matching_string):
    required_data = df[df['name'].str.contains(matching_string)]
    preprocessed_data = required_data[['value_date', 'name']]
    cleaned_data = preprocessed_data.reset_index()
    cleaned_data.columns = ['indices', 'value_date', 'name']
    return cleaned_data

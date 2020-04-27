# from django.http import JsonResponse
# from random import randint
# from django.shortcuts import render
# from django.views.generic import TemplateView, View
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
# from pams_system.models.levels import InputData
# from .models import MonthlyWeatherByCity
# from pams_system.models.kpis import KpiValue

# User = get_user_model()


# class HomeView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'reports/index.html', {"weights": 10})


# def get_data(request, *args, **kwargs):
#     data = {
#         "kpi": 100,
#         "weights": 10,
#     }
#     return JsonResponse(data)  # http response


# class ChartData(APIView):
#     authentication_classes = []
#     permission_classes = []

#     def get(self, request, format=None):
#         """
#         Return data for calculating apis.
#         """
#         qs_count = User.objects.all().count()
#         kpi_value = [str(kpi.value*100) for kpi in KpiValue.objects.all()[1:2]],
#         labels = ['Users', 'KpiValue','KpiWeight','Quality']
#         default_items = [qs_count,2,1.5,3.9]
#         data = {
#             "labels": labels,
#             "default": default_items,
#         }

#         return Response(data)

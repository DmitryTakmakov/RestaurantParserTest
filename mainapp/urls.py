from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.IndexPageView.as_view(), name='index'),
    path('parse_bk/', mainapp.parse_bk_data, name='bk_parser'),
    path('parse_mcd/', mainapp.parse_mcd_data, name='mcd_parser'),
    path('parse_kfc/', mainapp.parse_kfc_data, name='kfc_parser'),
    path('process_pandas/', mainapp.process_to_pandas, name='pandas'),
    path('moscow_report/', mainapp.moscow_report, name='moscow_report'),
]

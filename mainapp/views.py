import requests
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import TemplateView
from pandas import DataFrame, Series

from mainapp.models import Restaurant


class IndexPageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bk_len = len(Restaurant.objects.filter(restaurant_chain="Burger King"))
        mcd_len = len(Restaurant.objects.filter(restaurant_chain="McDonalds"))
        kfc_len = len(Restaurant.objects.filter(restaurant_chain="KFC"))
        context['bk_length'] = bk_len
        context['mcd_length'] = mcd_len
        context['kfc_length'] = kfc_len
        return context


def parse_bk_data(request):
    restaurant_list = requests.get('https://burgerking.ru/restaurant-locations-json-reply-new').json()
    for rest in restaurant_list:
        Restaurant.objects.create(
            restaurant_chain='Burger King',
            restaurant_id=f"BK_{rest['storeId']}",
            restaurant_location_longitude=rest['longitude'],
            restaurant_location_latitude=rest['latitude']
        )
    return HttpResponseRedirect(reverse('main:index'))


def parse_mcd_data(request):
    restaurant_dict = requests.get('https://mcdonalds.ru/api/restaurants').json()
    for rest in restaurant_dict['restaurants']:
        Restaurant.objects.create(
            restaurant_chain='McDonalds',
            restaurant_id=f"McD_{rest['id']}",
            restaurant_location_longitude=rest['longitude'],
            restaurant_location_latitude=rest['latitude']
        )
    return HttpResponseRedirect(reverse('main:index'))


def parse_kfc_data(request):
    payload = {'coordinates': [55.77500599999999, 37.583211000000006], 'radiusMeters': 10000000, 'channel': 'website'}
    restaurant_dict = requests.post('https://api.kfc.com/api/store/v2/store.geo_search', json=payload).json()
    for rest in restaurant_dict['searchResults']:
        Restaurant.objects.create(
            restaurant_chain='KFC',
            restaurant_id=f"KFC_{rest['store']['storeId']}",
            restaurant_location_longitude=rest['store']['contacts']['coordinates']['geometry']['coordinates'][1],
            restaurant_location_latitude=rest['store']['contacts']['coordinates']['geometry']['coordinates'][0]
        )
    return HttpResponseRedirect(reverse('main:index'))


def process_to_pandas(request):
    bk_rests_coords = get_coords('Burger King')
    mcd_rests_coords = get_coords('McDonalds')
    kfc_rests_coords = get_coords('KFC')
    result = DataFrame({
        'Burger King': Series(bk_rests_coords),
        'McDonalds': Series(mcd_rests_coords),
        'KFC': Series(kfc_rests_coords)
    })
    result.to_csv('table.csv')
    content = {
        'result': 'Pandas table saved to table.csv file in project directory.',
        'bk_length': len(Restaurant.objects.filter(restaurant_chain="Burger King")),
        'mcd_length': len(Restaurant.objects.filter(restaurant_chain="McDonalds")),
        'kfc_length': len(Restaurant.objects.filter(restaurant_chain="KFC"))
    }
    return render(request, 'index.html', content)


def moscow_report(request):
    bk_rests = get_rests_in_moscow('Burger King')
    mcd_rests = get_rests_in_moscow('McDonalds')
    kfc_rests = get_rests_in_moscow('KFC')
    content = {
        'bk_length': len(Restaurant.objects.filter(restaurant_chain="Burger King")),
        'mcd_length': len(Restaurant.objects.filter(restaurant_chain="McDonalds")),
        'kfc_length': len(Restaurant.objects.filter(restaurant_chain="KFC")),
        'report': f'Всего в Москве существует {len(bk_rests)} ресторанов Burger King, '
                  f'{len(mcd_rests)} ресторана McDonalds и {len(kfc_rests)} ресторанов KFC.'
                  f'Не трудно заметить, что явное преимущество у KFC. За счет бОльшего количества ресторанов вообще'
                  f'KFC получают также бОльшую плотность этих ресторанов в центре Москвы, пожалуй, самый проходимый'
                  f' район города. Также интересно отметить, что McDonalds практически "сдал" центр города, '
                  f'сконцентрировавшись на других районах и окраинах. Burger King же старается равномерно покрыть'
                  f' все районы города.'
    }
    return render(request, 'index.html', content)


def get_rests_in_moscow(restaurant_name: str):
    mos_lat_1 = 55.579644
    mos_lat_2 = 55.901642
    mos_long_1 = 37.334859
    mos_long_2 = 37.830056
    all_rests = Restaurant.objects.filter(restaurant_chain=restaurant_name)
    moscow_rests_list = []
    for rest in all_rests:
        if mos_long_1 <= rest.restaurant_location_longitude <= mos_long_2 \
                and mos_lat_1 <= rest.restaurant_location_latitude <= mos_lat_2:
            moscow_rests_list.append({
                rest.restaurant_id: [float(rest.restaurant_location_longitude),
                                     float(rest.restaurant_location_latitude)]
            })
    return moscow_rests_list


def get_coords(restaurant_name: str):
    coords = list(Restaurant.objects.filter(restaurant_chain=restaurant_name).
                  values('restaurant_id', 'restaurant_location_longitude', 'restaurant_location_latitude'))
    coords_list = []
    for _ in coords:
        instance = f"{_['restaurant_id']}, {float(_['restaurant_location_longitude'])}," \
                   f" {float(_['restaurant_location_latitude'])}"
        coords_list.append(instance)
    return coords_list

from django.shortcuts import render
import requests
from django.http import Http404
from django.http import JsonResponse

# Create your views here.
class ZomatoOrderDetailsView:
    def get_orders(request):
        total_pages = 1
        current_page = 1
        total_amount = 0
        
        url = "https://www.zomato.com/webroutes/user/orders?page={current_page}"

        headers = {}

        while current_page <= total_pages:
            try:
                response = requests.get(url, headers=headers)
            except:
                raise Http404

            if response.status_code == 200:
                response = response.json()
                data = response.get('sections', {}).get('SECTION_USER_ORDER_HISTORY', {})
                total_pages = data.get('totalPages', total_pages)

                orders = response.get('entities', {}).get('ORDER', {})
                for each in orders:
                    order = orders[each]
                    total_cost = order.get('totalCost', '0')
                    if total_cost[0] != '0':
                        total_cost = float(total_cost[1:])
                    total_amount += total_cost

                current_page += 1

        return JsonResponse({
            'total_amount': total_amount
        }, status=200)
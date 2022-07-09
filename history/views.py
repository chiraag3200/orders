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

        headers = {}

        while current_page <= total_pages:
            try:
                url = f"https://www.zomato.com/webroutes/user/orders?page={current_page}"
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

    def get_invoices(request):
        total_pages = 1
        current_page = 1

        headers = {}

        while current_page <= total_pages:
            try:
                url = f"https://www.zomato.com/webroutes/user/orders?page={current_page}"
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
                    order_hash_id = order.get('hashId', None)
                    
                    if order_hash_id:
                        invoice_url = f"https://www.zomato.com/webroutes/order/receipt?hashId={order_hash_id}"
                        invoice_response = requests.get(invoice_url, headers=headers)

                        if invoice_response.status_code == 200:
                            invoice_response = invoice_response.json()
                            invoice_file_link = invoice_response.get('file', None)

                            if invoice_file_link:
                                invoice_file = requests.get(invoice_file_link)
                                if invoice_file.status_code == 200:
                                    with open(f"./invoices/{order_hash_id}.pdf", "wb") as file:
                                        file.write(invoice_file.content)  

                current_page += 1

        return JsonResponse({
            'message': "Invoices saved successfully"
        }, status=200)
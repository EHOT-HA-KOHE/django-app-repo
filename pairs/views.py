from typing import Any

from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View
from django.views.generic import DetailView, TemplateView, ListView

from pairs.forms import SearchForm
from pairs.models import Pools, PoolTokenPrice
from pairs.utils import q_search


class PairView(TemplateView):
    template_name = 'pairs/pair.html'
    # pair_address = 'pair_address'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = 'Pair Info'

        pool = Pools.objects.get(address=self.kwargs.get('pair_address'))
        context["pool"] = pool

        prices = PoolTokenPrice.objects.filter(pool=pool).order_by('timestamp')
        price_data = {
            'timestamps': [price.timestamp.isoformat() for price in prices],
            'prices': [float(price.usd_price) for price in prices],
        }
        context['price_data'] = price_data

        print(price_data)

        return context
    

class SearchView(View):
    def get(self, request):
        form = SearchForm(request.GET)

        if form.is_valid():
            query = form.cleaned_data.get('q')

            query_results = q_search(query)

            q_results = render_to_string(
                "pairs/search_result.html", {"query_results": query_results}
            )

            # Формируем данные для ответа
            response_data = {
                "q_results": q_results,
                "message": "Вот результаты поиска",
            }

            return JsonResponse(response_data)
        
        else:
            response_data = {
                "q_results": "",
                "message": "Неверный запрос поиска.",
                "errors": form.errors,  # Передаем ошибки валидации
            }

            return JsonResponse(response_data, status=400)

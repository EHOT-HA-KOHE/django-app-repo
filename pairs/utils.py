from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline

from pairs.models import Pools


def q_search(query):
    if query.isdigit() and len(query) <= 5:
        return Pools.objects.filter(
            id=int(query)
        )  # Используем filter а не get тк нужно получить QuerySet

    # vector = SearchVector("address", "token_1__name")
    # query = SearchQuery(query)

    # result = (
    #     Pools.objects.annotate(rank=SearchRank(vector, query))
    #     .order_by("-rank")
    #     .filter(rank__gt=0)
    # )

    # result = result.annotate(
    #     headline=SearchHeadline(
    #         'address', 
    #         query, 
    #         start_sel='<span style="background-color: yellow;">',
    #         stop_sel='</span>',
    #     )
    # )

    # result = result.annotate(
    #     bodyline=SearchHeadline(
    #         'token_1__name', 
    #         query, 
    #         start_sel='<span style="background-color: yellow;">',
    #         stop_sel='</span>',
    #     )
    # )

    # Используем LIKE для поиска по тексту
    result = (
        Pools.objects.filter(
            address__icontains=query
        ) | Pools.objects.filter(
            token__name__icontains=query
        )
    ).distinct()

    return result

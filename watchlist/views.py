from email import message
from typing import Any
from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views import View

from pairs.models import Pools
from users.models import User
from watchlist.models import UserCollections


class CollectionsView(TemplateView):
    template_name = "watchlist/watchlist_categories.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["title"] = "User`s Lists"
        return context


class CollectionPairsView(TemplateView):
    template_name = "watchlist/category_pairs.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        category_name = kwargs.get("category_name")
        query_kwargs = {'user': self.request.user} if self.request.user.is_authenticated \
                                        else {'session_key': self.request.session.session_key}

        collection = UserCollections.objects.filter(name=category_name, **query_kwargs).first()
        if not collection:
            raise Http404(f"Коллекция с именем '{category_name}' не найдена.")
        
        context["pools"] = collection.pools.all()
        context["title"] = f"User Collection - {category_name}"
        context["category_name"] = category_name
        context["is_saving_view"] = True
        return context


class CreateNewCollectionView(View):
    def post(self, request, *args, **kwargs):
        category_name = request.POST.get("category_name")

        if category_name == "":
            collections = render_to_string(
                "watchlist/_categories_list.html", {"request": request}
            )
            return JsonResponse(
                {
                    "message": "Категория не может быть пустой.",
                    "collections": collections,
                }
            )

        query_kwargs = {'user': request.user} if request.user.is_authenticated \
                                else {'session_key': request.session.session_key}
        # Логика создания новой категории, если требуется
        collection, created = UserCollections.objects.get_or_create(
            name=category_name, 
            **query_kwargs
        )

        if not created:
            return JsonResponse(
                {"message": f"Категория с именем {collection} уже существует."}
            )

        collections = render_to_string(
            "watchlist/_categories_list.html", {"request": request}
        )

        # Формируем данные для ответа
        response_data = {
            "message": f"Категория {collection} создана.",
            "collections": collections,
        }

        return JsonResponse(response_data)


class DelCollectionView(View):
    def post(self, request):
        category_name = request.POST.get("category_name")
        user = request.user

        query_kwargs = {'user': request.user} if request.user.is_authenticated \
                                else {'session_key': request.session.session_key}

        collection = UserCollections.objects.filter(name=category_name, **query_kwargs)
        if not collection.exists():
            return JsonResponse({"message": f"Подборка {category_name} не была удалена для пользователя {user.username}, " \
                                "так как не была найдена"}, status=400)

        collection.first().delete()

        collections = render_to_string("watchlist/_categories_list.html", {"request": request})

        return JsonResponse({"message": f"Подборка {category_name} успешно удалена для пользователя {user.username}",
                            "collections": collections})


class AddPoolToCollectionView(View):
    def post(self, request):
        pool = Pools.objects.filter(address=request.POST.get("pool_address"))
        if not pool.exists():
            return JsonResponse({"message": f"Пул не был добавлен в подборку, пул не был найден"}, status=400,)

        query_kwargs = {'user': request.user} if request.user.is_authenticated \
                                else {'session_key': request.session.session_key}
        collection = UserCollections.objects.filter(
            name=request.POST.get("collection_name"),
            **query_kwargs
        )
        if not collection.exists():
            return JsonResponse(
                {"message": f"Пул не был добавлен в подборку, у пользователя нет подборки с таким именем"}, status=400,
            )

        pool = pool.first()
        collection = collection.first()

        is_pool_in_category = collection.pools.filter(id=pool.id).exists()
        if is_pool_in_category:
            return JsonResponse({"message": f"Пул уже добавлен в эту подборку"}, status=400,)

        collection.pools.add(pool)

        response_data = {
            "message": f"Пул успешно добавлен в вашу подборку {collection.name}"
        }

        return JsonResponse(response_data)


class DelPoolFromCollectionView(View):
    def post(self, request):
        pool_address = request.POST.get('pool_address')
        category_name = request.POST.get('collection_name')

        query_kwargs = {'user': request.user} if request.user.is_authenticated \
                                else {'session_key': request.session.session_key}
        collection = UserCollections.objects.filter(
            name=category_name,
            **query_kwargs
        )
        if not collection.exists():
            return JsonResponse({'message': 'Этот категория не была найдена'})
        collection = collection.first()

        pool = Pools.objects.filter(address=pool_address)
        if not pool.exists():
            return JsonResponse({'message': 'Этот пул не был найден'})
        pool = pool.first()

        collection.pools.remove(pool)

        return JsonResponse(
                {
                    'message': f'Пул {pool_address} был успешно удален из категории {category_name}', 
                    'pool_address': pool_address,
                    }
            )

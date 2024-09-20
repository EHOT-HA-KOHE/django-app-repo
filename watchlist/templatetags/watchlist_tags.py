from django import template

from watchlist.utils import get_user_collections


register = template.Library()

@register.simple_tag(takes_context=True)
def user_collections(context):
    request = context.get('request')
    if not request:
        return []
    return get_user_collections(request)


@register.filter()
def len_of_collection(collection):
    return len(collection.pools.all())

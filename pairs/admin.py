from django.contrib import admin

from pairs.models import Blockchains, DexNames, Tokens, Pools


admin.site.register(Blockchains)
admin.site.register(DexNames)
admin.site.register(Tokens)
admin.site.register(Pools)

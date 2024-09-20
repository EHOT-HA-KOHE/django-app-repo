from typing import Any

from django.views.generic import TemplateView

from pairs.models import Blockchains, DexNames, Pools


class NewPairsView(TemplateView):
    template_name = 'new_pairs/new_pairs.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = 'New Pairs'
        
        chain = self.kwargs.get('chain')
        context['content'] = chain

        if chain == 'all':
            pools = Pools.objects.prefetch_related('prices').all()
        else:
            blockchain = Blockchains.objects.filter(name=chain).exists()
            if blockchain:
                blockchain = Blockchains.objects.get(name=chain)
                dex = DexNames.objects.filter(blockchain=blockchain)
                pools = Pools.objects.filter(dex_name__in=dex).prefetch_related('prices')

            else:
                self.template_name = 'new_pairs/not_working_blockchain.html'
                pools = []


        context['pools'] = pools

        return context

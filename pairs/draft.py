data = {
    'blockchains': [
        {'name': 'ethereum'},
        {'name': 'bsc'},
        {'name': 'solana'},
        {'name': 'ton'},
        {'name': 'base'}
    ],
    'dex_names': [
        {'name': 'uniswap_v1', 'blockchain': 'ethereum'},
        {'name': 'uniswap_v2', 'blockchain': 'ethereum'},
        {'name': 'sushiswap', 'blockchain': 'ethereum'},
        {'name': 'radium', 'blockchain': 'solana'},
    ],
}


import hashlib
import random
from itertools import cycle
import random

from datetime import timedelta
from django.utils import timezone

from pairs.models import Tokens, Pools, TokenPools, DexNames, Blockchains, PoolTokenPrice
from users.models import User


def craete_chains_and_dexes():
    for chain in data.get('blockchains'):
        Blockchains.objects.get_or_create(name=chain['name'])

    for dex in data.get('dex_names'):
        blockchain = Blockchains.objects.get(name=dex['blockchain'])
        DexNames.objects.get_or_create(name=dex['name'], address=f'Address of - {dex['name']}', blockchain=blockchain)


def custom_hash(data):
    number_bytes = str(data).encode()
    hash_object = hashlib.sha256(number_bytes)
    custom_hash = hash_object.hexdigest()
    return custom_hash


def create_pairs_objects(quantity_to_gen=7):
    craete_chains_and_dexes()
    dexes = cycle(DexNames.objects.all())
    pools_hashs = cycle([custom_hash(random.randint(0, 100000)) for _ in range(quantity_to_gen)])

    for _ in range(quantity_to_gen):
        i = random.randint(0, 100000)
        hash_hex = custom_hash(i)

        dex = next(dexes)

        # 1. Создаем или находим токен
        token, created = Tokens.objects.get_or_create(
            address=f'0.1x{hash_hex}',
            defaults={'name': f'Token{i}', 'symbol': f'TKN{i}'},
            blockchain=dex.blockchain
        )

        pool_hash = next(pools_hashs)
        # 4. Создаем или находим пул ликвидности
        pool, created = Pools.objects.get_or_create(
            address=f'0x{pool_hash}',
            makers = random.randint(50, 20_000),
            transactions = random.randint(100, 300_000),
            volume = random.randint(3_000, 20_000_000),
            liquidity = random.randint(5_000, 1_200_000),
            mcap = random.randint(5_000, 1_200_000),

            price_change_5m = random.uniform(-99, 99),
            price_change_1h = random.uniform(-99, 99),
            price_change_6h = random.uniform(-99, 99),
            price_change_24h = random.uniform(-99, 99),

            token=token,
            blockchain=dex.blockchain,
            dex_name=dex
        )

        for i in range(5):
            # Добавляем цену
            pool_token_price = PoolTokenPrice.objects.get_or_create(
                pool=pool,
                timestamp=timezone.now() - timedelta(minutes=i),
                usd_price=round(random.uniform(0.000000001, 1.2), random.randint(5, 9)),
                native_token_price=round(random.uniform(0.000000001, 1.2), random.randint(5, 9)),
                )

        # 5. Связываем токен с пулом в token_pools
        token_1_to_pool, created = TokenPools.objects.get_or_create(
            token=token,
            pool=pool
        )


def del_all_pools():
    TokenPools.objects.filter(token_id__in=Pools.objects.all()).delete()
    TokenPools.objects.filter(pool_id__in=Pools.objects.all()).delete()
    Pools.objects.all().delete()

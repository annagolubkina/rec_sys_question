import pandas as pd


def prefilter_items(data, item_features=None, take_n_popular=5000):

    # Убирем самые популярные товары
    popularity_idx = data.groupby('item_id')['user_id'].nunique().reset_index() / data['user_id'].nunique()
    popularity_idx.rename(columns={'user_id': 'share_unique_users'}, inplace=True)
    most_popular = popularity_idx[popularity_idx['share_unique_users'] > 0.5].item_id.tolist()
    data = data[~data['item_id'].isin(most_popular)]

    # Уберем самые НЕ популярные товары
    most_unpopular = popularity_idx[popularity_idx['share_unique_users'] < 0.01].item_id.tolist()
    data = data[~data['item_id'].isin(most_unpopular)]

    # Уберем товары, которые не продавались за последние 12 месяцев
    last_year_items = data.loc[data['week_no'] < data['week_no'].max() - 52, 'item_id'].unique().tolist()
    data = data[~data['item_id'].isin(last_year_items)]

    # Уберем слишком дешевые товары
    data = data[data.sales_value >= data.sales_value.quantile(q=0.01)]

    # Уберем слишком дорогие товары
    data = data[data.sales_value <= data.sales_value.quantile(q=0.99)]

    # Находим топ-5000 наиболее популярных товаров среди оставшихся. Остальным присваиваю индекс 999999
    popularity = data.groupby('item_id')['quantity'].sum().reset_index()
    popularity.rename(columns={'quantity': 'n_sold'}, inplace=True)
    top_n = popularity.sort_values('n_sold', ascending=False).head(take_n_popular).item_id.tolist()
    data.loc[~data['item_id'].isin(top_n), 'item_id'] = 999999

    return data


def postfilter_items(user_id, recommednations):
    pass

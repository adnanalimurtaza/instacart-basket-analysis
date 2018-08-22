""" Exploratory data analysis EDA on insta-cart data-set.
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


def load_data():
    """ Loads the data.

    :return: dictionary of DataFrames with file names as keys.
    """
    data_in_dict = dict()
    data_path = Path.cwd().parent.joinpath('data')
    for file in list(sorted(data_path.rglob('*.csv'))):
        data_in_dict[file.stem] = pd.read_csv(file)
    return data_in_dict


def join_frames(left, right, key=None):
    """ Join/Merge two DataFrames

    :param left: Left table (DataFrame)
    :param right: Right table (DataFrame)
    :param key: key for join
    :return: Merged DataFrame
    """
    if key is None:
        print("Key for join is None.")
        return None
    joined = pd.merge(left, right, on=key)
    return joined


def n_products(data_frame, n=10, view_type='head'):
    """ Finds the top or bottom n products in orders/sales.

    :param data_frame: DataFrame containing order_products data.
    :param n: number of products
    :param view_type: Defines the type either head or tail.
    :return: DataFrame of top or bottom n products
    """
    grouped = data_frame.groupby('product_id')
    count = grouped.size().reset_index(name='order_id_count')
    sort_count = count.sort_values(by='order_id_count', ascending=False)
    if view_type is 'head':
        return sort_count.head(n)
    elif view_type is 'tail':
        return sort_count.tail(n)
    else:
        print('view_type can either be head or tail.')


def orders_by_dow(data_frame):
    """ Gives orders_count by day of week.

    :param data_frame: DataFrame containing orders data.
    :return: DataFrame of order_ids count by day of week.
    """
    grouped = data_frame.groupby(['order_dow'], as_index=False)
    # count by column: 'order_id'
    count = grouped.agg({'order_id': 'count'}).rename(
        columns={'order_id': 'order_id_count'})
    count['week_day'] = ['Saturday', 'Sunday', 'Monday', 'Tuesday',
                         'Wednesday', 'Thursday', 'Friday']
    return count


def plot_n_product(data_frame):
    """ Plot n products using pandas.

    :param data_frame: DataFrame containing n products data.
    :return: None
    """
    data_frame.copy().rename(
        columns={'product_name': 'Products',
                 'order_id_count': 'Total Order Count'}).plot(
        x='Products', y='Total Order Count', kind='barh',
        title='Best Selling Products.', figsize=(12, 8))


def plot_orders_dow(data_frame):
    """ Plot n products using pandas.

    :param data_frame: DataFrame containing order counts by day of week.
    :return: None
    """
    data_frame.copy().rename(
        columns={'week_day': 'Days',
                 'order_id_count': 'Total Order Count'}).plot(
        x='Days', y='Total Order Count', kind='barh',
        title='Order Counts by Week Days.', figsize=(8, 8))


if __name__ == '__main__':
    # load data into data frames
    data_frames = load_data()
    if len(data_frames) == 0:
        print('Download instacart market analysis data-set using the link: '
              'https://www.instacart.com/datasets/grocery-shopping-2017')
        exit(0)

    # set rcParams to adjust auto-layout for plots.
    plt.rcParams.update({'figure.autolayout': True})

    # data frames
    order_products = data_frames['order_products_train']
    orders = data_frames['orders']

    # find top n best selling products
    top_n_products = n_products(order_products.iloc[:, :], view_type='head')
    reduced_products = data_frames['products'].copy()
    reduced_products = reduced_products.loc[:, ['product_id', 'product_name']]
    merged = join_frames(top_n_products, reduced_products, key='product_id')
    plot_n_product(merged)

    # find order counts by day of week
    orders_dow = orders_by_dow(orders)
    plot_orders_dow(orders_dow)
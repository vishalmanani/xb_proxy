from django.conf import settings
from ebaysdk.trading import Connection as Trading

API_MAP = dict()

api = Trading(
    appid=settings.APP_ID,
    devid=settings.DEV_ID,
    certid=settings.CERT_ID,
    token=settings.TOKEN,
    config_file=None,
    domain=settings.DOMAIN
)


def register(api_name):
    def wrapper(api_function):
        API_MAP[api_name] = api_function
        return api_function
    return wrapper


@register('GetNotificationPreferences')
def get_notification_preferences(data):
    response = api.execute('GetNotificationPreferences', {
        'PreferenceLevel': 'User',
    })
    return response


@register('GetOrders')
def get_orders(data):
    response = api.execute('GetOrders', {
        'OrderIDArray': [
            {
                'OrderID': '222037993704-2070296061012'
            }
        ]
    })
    return response


@register('ReviseInventoryStatus')
def revise_inventory_status(data):

    item_id = data.get('ItemID', None)
    quantity = data.get('Quantity', None)
    sku = data.get('SKU', None)

    if item_id and quantity and sku:
        response = api.execute('ReviseInventoryStatus', {
            'InventoryStatus': [
                {
                    'ItemID': item_id,
                    'Quantity': quantity,
                    'SKU': sku,
                }
            ]
        })
        return response

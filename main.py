import requests
import pprint
import os

SCHEDULED_CLASS_API_URL = 'https://api.onepeloton.com/ecomm/studio/{}/scheduled_classes'
NY_STUDIO_ID = '25900000001'

pp = pprint.PrettyPrinter(indent=4)


def main(event, context):
    url = SCHEDULED_CLASS_API_URL.format(NY_STUDIO_ID)
    res = requests.get(url)
    data = res.json()

    reservable_classes = [c for c in data['data']['classes'] if c['bookable'] and not (c['full'] and c['waitlist_full'])]
    pp.pprint(reservable_classes)


if __name__ == '__main__':
    main(None, None)

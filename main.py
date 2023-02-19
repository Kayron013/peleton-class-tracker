import requests
import pprint
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = 'https://api.onepeloton.com'
SCHEDULED_CLASS_ENDPOINT_TEMPLATE = API_BASE_URL + '/ecomm/studio/{}/scheduled_classes'

RESERVE_CLASS_URL_TEMPLATE = 'https://studio.onepeloton.com/new-york/schedule/{}/reserve'

NY_STUDIO_ID = '25900000001'

pp = pprint.PrettyPrinter(indent=4)

session = requests.Session()


def main(event, context):
    pp.pprint(get_classes())


def get_classes():
    url = SCHEDULED_CLASS_ENDPOINT_TEMPLATE.format(NY_STUDIO_ID)
    res = session.get(url)

    if res.status_code >= 400:
        pp.pprint(res)
        raise RuntimeError('Failed to get classes')

    data = res.json()

    reservable_classes = [transform_class(c, data['data']['instructors']) for c in data['data']['classes'] if c['bookable'] and not (c['full'] and c['waitlist_full'])]
    return reservable_classes


def transform_class(clazz, instructors):
    return {
        'instructor': [{'name': i['full_name'], 'img': i['image_url']} for i in instructors if i['id'] == clazz['instructor_id']][0],
        'disciplines': [c['name'] for c in clazz['disciplines']],
        'duration': clazz['duration'],
        'id': clazz['id'],
        'reserve_link': RESERVE_CLASS_URL_TEMPLATE.format(clazz['id']),
        'name': '',
        'start_time': clazz['start'],
        'free': clazz['free'],
        'waitlist_full': clazz['waitlist_full']
    }


if __name__ == '__main__':
    main(None, None)

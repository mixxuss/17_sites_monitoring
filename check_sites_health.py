import requests
import argparse
import time
import datetime

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', help='Path to sites list')
    return parser


def load_urls4check_list(path):
    with open(path, 'r') as text:
        return text.read().split()


def is_server_respond_with_200(url):
    response = requests.get(url)
    if response.status_code == 200:
        return True
    return False


def get_domain_expiration_date(domain_name):
    params = {
        'url': domain_name,
        'whois': '',
        'json': ''
    }
    response = requests.get('http://htmlweb.ru/analiz/api.php', params=params)
    return response.json()['paid']


def is_domain_expires_in_month(expire_date_str):
    expire_date = datetime.datetime.strptime(expire_date_str, '%d.%m.%Y')
    plus_month_date = datetime.datetime.today() + datetime.timedelta(days=30)
    if expire_date > plus_month_date:
        return False
    else:
        return True

if __name__ == '__main__':
    parsed_args = create_parser()
    args = parsed_args.parse_args()
    sites_list_path = args.path
    delay_between_requests = 5
    for site in load_urls4check_list(sites_list_path):
        is_200 = is_server_respond_with_200(site)
        domain_expire = get_domain_expiration_date(site)
        if is_200:
            print('Site {} is reachable by http'.format(site))
        else:
            print('Site {} is not reachable by http'.format(site))
        if is_domain_expires_in_month(domain_expire):
            print('Domain expires less than in month ({})'.format(domain_expire))
        else:
            print('Domain expires more than in month ({})'.format(domain_expire))
        time.sleep(delay_between_requests)

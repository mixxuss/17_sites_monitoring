import requests
import argparse
import time


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


if __name__ == '__main__':
    parsed_args = create_parser()
    args = parsed_args.parse_args()
    sites_list_path = args.path
    delay_between_requests = 5
    for site in load_urls4check_list(sites_list_path):
        is_200 = is_server_respond_with_200(site)
        domain_expire = get_domain_expiration_date(site)
        if is_200:
            print('Site {} is reachable by http, domain expires {}'.format(site,domain_expire))
        else:
            print('Site {} is not reachable by http, domain expires {}'.format(site, domain_expire))
        time.sleep(delay_between_requests)
import os
import requests

from urllib.parse import urlparse


def shorten_link(token: str, url: str) -> str:
    """Shortens the link via Bitly API"""
    headers = {
        'Authorization': f'Bearer {token}'
    }

    payload = {
        "long_url": url
    }

    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=payload)
    response.raise_for_status()

    bitlink = response.json()['link']
    return bitlink

def count_clicks(token: str, link: str) -> str:
    """Gets click count from bitly"""
    headers = {
        'Authorization': f'Bearer {token}'
    }

    u = urlparse(link)
    link = ''.join([u.netloc,u.path])

    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}/clicks/summary', headers=headers)
    response.raise_for_status()

    return response.json()['total_clicks']


def is_bitlink(token: str, link: str) -> bool:
    """Checks if the link is a bitlink"""
    headers = {
        'Authorization': f'Bearer {token}'
    }
    u = urlparse(link)
    link = ''.join([u.netloc,u.path])
    response = requests.get(f'https://api-ssl.bitly.com/v4/bitlinks/{link}', headers=headers)

    return response.ok


if __name__ == '__main__':
    
    token = os.environ['BITLY_TOKEN']
    url = input('Введите ссылку:')

    try:
        if is_bitlink(token, url):
            print(f'Количество переходов по битлинку {url}: {count_clicks(token, url)}')
        else:
            print(f'Для url {url} создан битлинк {shorten_link(token, url)}')
            
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as ex:
        print(f'произошла ошибка обращения к API Bitlinks: \n {ex}')

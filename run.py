#!/usr/bin/env python3

import requests
import random
import string
import time

from bs4 import BeautifulSoup as BS
from user_agent import generate_user_agent
import ipdb

# lenght = 6-7 (6)
# numbers count = 0-2 (1)


def string_generator(length):
    while True:
        chars_list = string.ascii_lowercase + string.digits
        comb_list = random.choices(chars_list, k=length)
        yield "".join(comb_list)


def get_image_by_string(string):
    url = "https://prnt.sc/" + string
    headers = {'user-agent': generate_user_agent()}

    response = requests.get(url, headers=headers)
    soup = BS(response.text, "html.parser")

    image_html = soup.find("img", class_="screenshot-image")
    
    if image_html:
        image_url = image_html.get('src')

        if 'http' in image_url:
            return image_url


def main():
    try:
        str_gen = string_generator(6)
        #ipdb.set_trace(context=8)

        for some_str in str_gen:
            image = get_image_by_string(some_str)

            print(f'image: {image}')
    except KeyboardInterrupt:
        print('\nExiting.')
        exit()


if __name__ == "__main__":
    main()

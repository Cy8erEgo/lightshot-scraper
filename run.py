#!/usr/bin/env python3

import requests
import random
import string

from bs4 import BeautifulSoup as BS
from user_agent import generate_user_agent


def string_generator(length):
    while True:
        chars_list = string.ascii_lowercase + string.digits
        comb_list = random.choices(chars_list, k=length)
        yield "".join(comb_list)


def get_image_by_string(string):
    url = "https://prnt.sc/" + string
    headers = {"user-agent": generate_user_agent()}

    response = requests.get(url, headers=headers)
    soup = BS(response.text, "html.parser")

    image_html = soup.find("img", class_="screenshot-image")

    if image_html:
        image_url = image_html.get("src")

        if "http" in image_url:
            return image_url


def main():
    clear = input("Do you want to clear images.html? [Y/n]: ")
    count = int(input("Enter the number of images: "))

    if clear.lower() == "y":
        file_mode = "w"
    else:
        file_mode = "a"

    f = open("images.html", file_mode)

    try:
        counter = 0
        str_gen = string_generator(6)

        for some_str in str_gen:
            image = get_image_by_string(some_str)

            if image:
                counter += 1

                print(f"{counter}. image:\t{image}")

                f.write(f'<img src="{image}" style="border: 3px solid red">')

                if counter >= count:
                    break

    except KeyboardInterrupt:
        print("\nExiting.")
        exit()
    finally:
        f.close()


if __name__ == "__main__":
    main()

import requests
import random
import string
import os
from bs4 import BeautifulSoup as BS
from user_agent import generate_user_agent


DISCORD_WEBHOOK_URL = os.environ['webhook_url']


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


def send_to_discord(image_url):
    response = requests.head(image_url)
    if response.status_code == 200:
        data = {
            "embeds": [
                {
                    "title": "Image Found",
                    "description": f"Image URL: {image_url}",
                    "image": {
                        "url": image_url
                    }
                }
            ]
        }

        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        return response.status_code
    return None


def main():
    # scraping
    str_gen = string_generator(6)
    counter = 0

    for some_str in str_gen:
        image = get_image_by_string(some_str)
        if not image:
            continue

        counter += 1

        print(f"{counter}. image:\t{image}")

        send_to_discord(image)

        if counter >= 100:
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting.")
        exit()

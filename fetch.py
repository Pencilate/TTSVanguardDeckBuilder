import argparse
from io import BytesIO
from PIL import Image
import json
import requests
from urllib.parse import quote_plus
from bs4 import BeautifulSoup

from canvas import CFVCanvasGeneration

parser = argparse.ArgumentParser(description='Cardfight Vanguard Deck Builder for Tabletop Simulator')
parser.add_argument('jsonfile', help="Name of the json file containing deck information")
parser.add_argument('-o', '--output', help="Name of the output file (Must include file extension)")

args = vars(parser.parse_args())

def get_image(img_url):
    response = requests.get(img_url)
    image_bytes_io = BytesIO()
    image_bytes_io.write(response.content)
    return Image.open(image_bytes_io)

unique_card_list = []
unique_bypass_card_dict = {}

card_order_list = []
card_image_dictionary = {}

card_prefix_blacklist = ["BWC","PR"]

json_deck = None
with open(args['jsonfile']) as deck:
    json_deck = json.load(deck)

for deck in json_deck['cards']:
    if "img" in deck:
        unique_bypass_card_dict[deck['name']] = deck['img']
    else:
        unique_card_list.append(deck['name'])

    for i in range(deck['quantity']):
        card_order_list.append(deck['name'])

regulation = json_deck["regulation"] if json_deck["regulation"] else "P"

for cardname in unique_card_list:
    cardname_formatted = quote_plus(cardname)

    card_url = f"https://en.cf-vanguard.com/cardlist/cardsearch/?regulation={regulation}&nation=&clan=&keyword={cardname_formatted}&keyword_type%5B%5D=name&kind%5B%5D=all&grade%5B%5D=all&power_from=&power_to=&rare=&trigger%5B%5D=all&view=text"
    html_doc_req = requests.get(card_url)
    if not html_doc_req.ok:
        print(f"Failed to retrieve page for {cardname}")
    
    print(f"Retrieved HTML for {cardname}")
    soup = BeautifulSoup(html_doc_req.text, 'html.parser')

    img_url = None
    card_list = soup.find_all("div","cardlist_imagelist")[0].find_all("a")
    for card_entry in card_list:
        card_entry_name = card_entry.h5.text.strip()
        if card_entry_name.lower() != cardname.strip().lower():
            continue

        card_entry_number = card_entry.select("div.number")[0].text.strip()
        if any(word in card_entry_number for word in card_prefix_blacklist):
            continue

        img_url = card_entry.img['src']

    image = get_image(img_url)
    card_image_dictionary[cardname] = image

for cardname, link in unique_bypass_card_dict.items():
    image = get_image(link)
    print(f"Retrieved image for {cardname}")
    card_image_dictionary[cardname] = image

bc_img = get_image(json_deck['backcover_img_url'])

result = CFVCanvasGeneration().generate(card_order_list,card_image_dictionary,last_card_cover=bc_img)
output_cover_filename = "cover-{0}".format(args["output"]) if args["output"] else "cover.png"
bc_img.save(output_cover_filename)
output_filename = args["output"] if args["output"] else "output.png"
result.save(output_filename)

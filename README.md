# Vanguard Deck Builder for Tabletop Simulator

This is a deck builder that retrieves images from the official CardFight Vanguard Card List and constructs the deck into a format compatible with Tabletop Simulator.

## Usage:

1. Clone/Download this repo
2. Create a new JSON file and fill in your deck details in the following format.

    ```
    {
        "backcover_img_url": "https://example.com/cover.jpg",
        "regulation": "P", 
        "cards" : [
            {
                "name": "Card A",
                "quantity": 1
            },
            {
                "name": "Card B",
                "quantity": 1,
                "img": "https://example.com/img.jpg"
            }
        ]
    }
    ```
        
    Inside each card entry, you will be able to specify a image link using the optional `"img"` key. You might want to use this if you are unsatisfied with the image quality of the card.
3. Run `fetch.py` script with the following command. (Assume `deck.json` is json file created in the previous step.)
    ```
        python ./fetch.py deck.json
    ```
    Optionally, a `-o` option can be added to specify a output name:
    ```
        python ./fetch.py deck.json -o output.png
    ```

4. After the command ran successfully, you should see 2 PNG files: `cover*.png` for the cover image and `output.png`/`<yourchosenoutputname>.png` for the Tabletop Simulator deck image.

## Note:
This is still an early release, please report any bugs using Github Issues. Also, feel free to fork.
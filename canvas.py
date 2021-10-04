from PIL import Image

class CanvasGeneration:
    def __init__(self):
        self.single_card_height = 100
        self.single_card_width = 100
        self.rows = 7
        self.columns = 10

    def generate(self, card_order_list, card_image_dictionary, last_card_cover=None):
        canvas_height = self.single_card_height * self.rows
        canvas_width = self.single_card_width * self.columns
        print(f"Canvas Size(WxH): {canvas_width} by {canvas_height}")

        canvas = Image.new('RGB',(canvas_width,canvas_height))

        break_loop = False

        for r_idx in range(self.rows):
            for c_idx in range(self.columns):
                canvas_index = (r_idx * self.columns) + c_idx
                if canvas_index >= len(card_order_list):
                    break_loop = True
                    break

                image = card_image_dictionary[card_order_list[canvas_index]]
                
                image_width, image_height = image.size
                if image_width > self.single_card_width or image_height > self.single_card_height:
                    image = image.resize((self.single_card_width,self.single_card_height))
                    card_image_dictionary[card_order_list[canvas_index]] = image

                canvas.paste(im=image,box=((self.single_card_width * c_idx),(self.single_card_height * r_idx)))
            
            if break_loop:
                break
        
        if last_card_cover:
            resized_last_card_cover = last_card_cover.resize((self.single_card_width,self.single_card_height))
            canvas.paste(im=resized_last_card_cover,box=((self.single_card_width * (self.columns - 1)),(self.single_card_height * (self.rows - 1))))

        return canvas

class CFVCanvasGeneration(CanvasGeneration):
    def __init__(self):
        super().__init__()
        self.single_card_height = 511
        self.single_card_width = 350


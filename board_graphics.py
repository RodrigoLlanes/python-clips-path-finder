from tkinter import *
from PIL import Image
from PIL import ImageTk

blue = "#05f"

class Board():
    def __init__(self, static_data, start_dynamic, title='Robot', cell_size=150, close_callback=None, get_selected_piece=lambda:None):
        self.static_data = static_data
        self.start_dynamic = start_dynamic
        self.cell_size = cell_size
        self.get_selected_piece = get_selected_piece

        display_width = static_data['size'][0] * self.cell_size
        display_height = static_data['size'][1] * self.cell_size

        self.window = Tk()
        self.window.resizable(width=False, height=False)
        if close_callback != None:
            self.window.protocol('WM_DELETE_WINDOW', close_callback)
        
        self.box_img = ImageTk.PhotoImage(Image.open('resources/images/box.png').resize((self.cell_size, self.cell_size), Image.ANTIALIAS))
        self.bot_img = ImageTk.PhotoImage(Image.open('resources/images/robot.png').resize((self.cell_size, self.cell_size), Image.ANTIALIAS))
        self.enemy_img = ImageTk.PhotoImage(Image.open('resources/images/enemy.png').resize((self.cell_size, self.cell_size), Image.ANTIALIAS))
        self.lader_img = ImageTk.PhotoImage(Image.open('resources/images/lader.png').resize((self.cell_size, self.cell_size), Image.ANTIALIAS))

        self.gameDisplay = Canvas(self.window, bg="white", height=display_height, width=display_width)
        self.draw(self.box_img, 1, 1)
        self.gameDisplay.pack(fill=BOTH, expand=1)
        self.window.title(title)


        self.gameDisplay.bind("<Button-1>", self.click_callback)

    def click_callback(self, event):
        piece = self.get_selected_piece()
        if piece != None:
            x, y = self.to_robot_coords(event.x//self.cell_size, event.y//self.cell_size)
            if 0 < x <= self.static_data['size'][0] and 0 < y <= self.static_data['size'][1] and [x, y] != self.start_dynamic['pos']:
                if [x, y] in self.static_data['holes']:
                    self.static_data['holes'].remove([x, y])
                if [x, y] in self.static_data['leaders']:
                    self.static_data['leaders'].remove([x, y])
                if [x, y] in self.start_dynamic['enemies']:
                    self.start_dynamic['enemies'].remove([x, y])
                if [x, y] in self.start_dynamic['boxes']:
                    self.start_dynamic['boxes'].remove([x, y])
                
                if piece != 'clear':
                    if piece == 'player':
                        self.start_dynamic['pos'] = [x, y]
                    elif piece == 'holes' or piece == 'leaders':
                        self.static_data[piece].append([x, y])
                    else:
                        self.start_dynamic[piece].append([x, y])


    def to_robot_coords(self, x, y):
        return (x+1, self.static_data['size'][1] - y)

    def from_robot_coords(self, x, y):
        return (x-1, self.static_data['size'][1] - y)

    def draw(self, img, x, y):
        self.gameDisplay.create_image(x * self.cell_size, y * self.cell_size, anchor=NW, image=img)

    def draw_static(self):
        for x in range(self.static_data['size'][0]):
            for y in range(self.static_data['size'][1]):
                x1, y1 = self.to_robot_coords(x, y)
                if [x1,y1] in self.static_data['leaders']:
                    self.draw(self.lader_img, x, y)
                if [x1,y1] not in self.static_data['holes']:
                    h = self.cell_size // 4
                    self.gameDisplay.create_rectangle(x * self.cell_size, y * self.cell_size + (self.cell_size - h), (x * self.cell_size) + self.cell_size, ((y+1) * self.cell_size), outline=blue, fill=blue)

    def draw_dynamic(self, dynamic_data):
        for x, y in dynamic_data['enemies']:
            x, y = self.from_robot_coords(x, y)
            self.draw(self.enemy_img, x, y)
        for x, y in dynamic_data['boxes']:
            x, y = self.from_robot_coords(x, y)
            self.draw(self.box_img, x, y)
            
        x, y = dynamic_data['pos']
        x, y = self.from_robot_coords(x, y)
        self.draw(self.bot_img, x, y)
    
    def set_static(self, static_data):
        self.static_data = static_data
        display_width = static_data['size'][0] * self.cell_size
        display_height = static_data['size'][1] * self.cell_size
        self.gameDisplay.config(width=display_width, height=display_height)

    def refresh_size(self):
        display_width = self.static_data['size'][0] * self.cell_size
        display_height = self.static_data['size'][1] * self.cell_size
        self.gameDisplay.config(width=display_width, height=display_height)


    def update(self, dynamic_data):
        self.gameDisplay.delete("all")
        self.draw_static()
        self.draw_dynamic(dynamic_data)
        self.window.update()

    def close(self):
        self.window.destroy()
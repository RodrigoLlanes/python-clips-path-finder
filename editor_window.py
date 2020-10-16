from tkinter import *

class Editor():
    def __init__(self, static_data, dynamic_data, board, title="Robot App Config", run_callback=lambda:None, close_callback=None, set_selected_piece=lambda v:None):
        self.root = Tk()
        self.static_data = static_data
        self.dynamic_data = dynamic_data
        self.board = board

        self.root.title(title)
        self.root.resizable(width=False, height=False)
        self.root.geometry('200x200')

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)

        if close_callback != None:
            self.root.protocol('WM_DELETE_WINDOW', close_callback)

        lbl = Label(self.root, text="Map width: ")
        lbl.grid(column=0, row=0)
        default = StringVar(self.root, value=static_data['size'][0])
        w_entry = Entry(self.root, width=3, textvariable=default)
        w_entry.grid(column=1, row=0)   
        button = Button(self.root, text="Update", command=lambda:self.set_size(w_entry, 0))
        button.grid(column=2, row=0)

        lbl = Label(self.root, text="Map height: ")
        lbl.grid(column=0, row=1)
        default = StringVar(self.root, value=static_data['size'][1])
        h_entry = Entry(self.root, width=3, textvariable=default)
        h_entry.grid(column=1, row=1)    
        button = Button(self.root, text="Update", command=lambda:self.set_size(h_entry, 1))
        button.grid(column=2, row=1)

        lbl = Label(self.root, text="Bullets: ")
        lbl.grid(column=0, row=2)
        default = StringVar(self.root, value=dynamic_data['ammo'])
        b_entry = Entry(self.root, width=3, textvariable=default)
        b_entry.grid(column=1, row=2)    
        button = Button(self.root, text="Update", command=lambda:self.set_ammo(b_entry))
        button.grid(column=2, row=2)

        lbl = Label(self.root, text="Max depth: ")
        lbl.grid(column=0, row=3)
        default = StringVar(self.root, value=static_data['max_depth'])
        d_entry = Entry(self.root, width=3, textvariable=default)
        d_entry.grid(column=1, row=3)    
        button = Button(self.root, text="Update", command=lambda:self.set_max_depth(d_entry))
        button.grid(column=2, row=3)
        
        button = Button(self.root, text="Run", command=run_callback)
        button.grid(column=1, row=4)

        button = Button(self.root, text="Enemie", command=lambda: set_selected_piece('enemies'))
        button.grid(column=0, row=5, sticky='news')
        button = Button(self.root, text="Box", command=lambda: set_selected_piece('boxes'))
        button.grid(column=1, row=5, sticky='news')
        button = Button(self.root, text="Hole", command=lambda: set_selected_piece('holes'))
        button.grid(column=2, row=5, sticky='news')
        button = Button(self.root, text="Leaders", command=lambda: set_selected_piece('leaders'))
        button.grid(column=0, row=6, sticky='news')
        button = Button(self.root, text="Player", command=lambda: set_selected_piece('player'))
        button.grid(column=1, row=6, sticky='news')
        button = Button(self.root, text="Clear", command=lambda: set_selected_piece('clear'))
        button.grid(column=2, row=6, sticky='news')

        self.window = Frame(self.root)

    def set_size(self, entry, n):
        try:
            v = int(entry.get())
            if v > 0:
                self.static_data['size'][n] = v
                self.board.refresh_size()
            else:
                raise NameError("")
        except:
            entry.delete(0,END)
            entry.insert(0, self.static_data['size'][n])

    def set_max_depth(self, entry):
        try:
            v = int(entry.get())
            if v > 0:
                self.static_data['max_depth'] = v
            else:
                raise NameError("")
        except:
            entry.delete(0,END)
            entry.insert(0, self.static_data['max_depth'])

    def set_ammo(self, entry):
        try:
            v = int(entry.get())
            if v > -1:
                self.dynamic_data['ammo'] = v
            else:
                raise NameError("")
        except:
            entry.delete(0,END)
            entry.insert(0, self.dynamic_data['ammo'])


    def update(self):
        self.window.update()

    def close(self):
        self.window.destroy()
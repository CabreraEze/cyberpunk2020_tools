
import datetime
import os
import copy
import tkinter as tk

from tkinter import Button, Label, Entry, Listbox
from tkinter import filedialog, END, messagebox

import tool
import classes


class cbpnkGUI:

    def __init__(self):
        self.save_status = ''
        self.load_status = ''
        self.__save: bool = False
        self.__load: bool = False

        self.session = None

        self.master = tk.Tk()
        #self.master.geometry('380x420')
        self.__initialize: bool = False
        self.menu_main()
    
    def menu_main(self):
        if self.__initialize:
            for widget in self.master.winfo_children():
                widget.destroy()
        else:
            self.__initialize = True

        self.characters_b = Button(self.master, text='Characters', command=self.menu_characters)\
            .grid(column=0, row=0, pady=10)
        self.create_session_b = Button(self.master, text='Create/Edit session', command=self.menu_create_session)\
            .grid(column=0, row=1, pady=10)
        self.save_session_b = Button(self.master, text='Save session', command=self.save_session)\
            .grid(column=0, row=2, pady=10)
        self.load_session_b = Button(self.master, text='Load session', command=self.load_session)\
            .grid(column=0, row=3, pady=10)

        self.save_check = Label(self.master, text=self.save_status)
        self.save_check.grid(column=1, row=2)

        self.load_check = Label(self.master, text=self.load_status)
        self.load_check.grid(column=1, row=3)

        self.master.mainloop()

    def save_session(self):
        if not self.__load:
            messagebox.showwarning("Warning", 'Please load a session first.')
        else:
            self.session_folder = filedialog.askdirectory(title='Save session folder')
            self.session.save(self.session_folder)
            self.__save = True
            
            ct = datetime.datetime.now()
            self.save_status = 'Last save: '+ct.hour+':'+ct.minute+':'+ct.second
            self.save_check.config(text=self.save_status)

    def load_session(self):
        self.session_folder = filedialog.askdirectory(title='Load session folder')
        files = [f for f in os.listdir(self.session_folder) if f.endswith('.dcm')]
        self.session = classes.Session(files)

        self.load_status = u'\u2713'
        self.load_check.config(text=self.load_status)
        self.__load = True

        self.save_status = ''
        self.save_check.config(text='')
        self.__save = False

    def menu_create_session(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        def add_player():
            new_player = self.players_e.get()
            if new_player:
                session_players.append(tool.create_template(new_player))
                update_players_list()
                self.players_e.delete(0, END)
            else:
                messagebox.showwarning("Warning", "Please enter a player.")

        def delete_player():
            selected_player_index = self.players_lst.curselection()
            if selected_player_index:
                selected_player_index = selected_player_index[0]
                del session_players[selected_player_index]
                update_players_list()
            else:
                messagebox.showwarning("Warning", "Please select a player to delete.")

        def edit_player():
            quick_save()
            selected_player_index = self.players_lst.curselection()
            if selected_player_index:
                selected_player_index = selected_player_index[0]
                session_players[selected_player_index] = tool.edit_player_tool(
                    self.master,
                    session_players[selected_player_index]
                )
            else:
                messagebox.showwarning("Warning", "Please select a player to edit.")

        def update_players_list():
            self.players_lst.delete(0, END)
            for character in session_players:
                self.players_lst.insert(END, character.player)

        def quick_save():
            self.session = classes.Session([p.dictionary for p in session_players])

            self.load_status = u'\u2713'
            self.__load = True
            self.save_status = ''
            self.__save = False

        def save_session():
            quick_save()
            self.menu_main()

        self.players_e = Entry(self.master, width=30)
        self.players_e.grid(row=0, column=0, padx=10, pady=10)

        self.players_lst = Listbox(self.master, selectmode=tk.SINGLE, width=40, height=10)
        self.players_lst.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        if self.__load:
            session_players = self.session.players
            update_players_list()
        else:
            session_players = []

        self.add_b = Button(self.master, text="Add player", command=add_player)\
            .grid(row=0, column=1, padx=10, pady=10)
        self.delete_b = Button(self.master, text="Delete player", command=delete_player)\
            .grid(row=2, column=1, pady=10)
        self.edit_b = Button(self.master, text='Edit player', command=edit_player)\
            .grid(row=2, column=3, pady=10)

        self.main_menu_b = Button(self.master, text='Main menu', command=self.menu_main)\
            .grid(row=2, column=0, pady=10)
        self.save_newsession_b = Button(self.master, text='Save session', command=save_session)\
            .grid(row=2, column=2, pady=10)

        self.master.mainloop()

    def menu_characters(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        row = 0

        self.player_b = []
        for player in self.session.players:
            button_name = f'{player.name} ({player.player})'
            self.player_b.append(Button(self.master, text=button_name, command=lambda p=player: self.menu_player_attacker(p)).grid(row=row))
            row += 1

        self.main_menu_b = Button(self.master, text='Main menu', command=self.menu_main)\
            .grid(row=row, pady=5)

        self.master.mainloop()

    def menu_player_attacker(self, player):
        for widget in self.master.winfo_children():
            widget.destroy()

        attacker_label = f'{player.name} ({player.player}) is going to attack:'
        self.attacker_l = Label(self.master, text=attacker_label).grid(row=0)

        row = 1
        self.attacked_player_b = []
        for attacked_player in self.session.players:
            if attacked_player.player != player.player:

                button_name = f'{attacked_player.name} ({attacked_player.player})'
                self.attacked_player_b.append(Button(self.master, text=button_name,
                    command=lambda m=self.master, p=player, e=attacked_player: tool.damage_resolve(m,p,e)).grid(row=row))
                row += 1

        self.back_b = Button(self.master, text='Back', command=self.menu_characters).grid(row=row, pady=10)

        self.master.mainloop()
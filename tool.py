import classes
import tkinter as tk
from tkinter import Entry, Label, Button, Listbox, Checkbutton, messagebox, END



'''
TEMPLATE MAKER
'''
def create_template(player):
    print('creando template')
    template = {
        'player': player,
        'name': 'N/A',
        'weapons':
            [
                {
                    'name': 'N/A',
                    'n_bullets': 0,
                    'dice': 0,
                    'n_dice': 0,
                    'dmg_mod': 0
                },
            ]
            ,
        'btm': 0,
        'armor':
            {
                'head': 0,
                'r_arm': 0,
                'l_arm': 0,
                'torso': 0,
                'r_leg': 0,
                'l_leg': 0
            },
        'alive': True,
        'limbs': 
            {
                'r_arm': True,
                'l_arm': True,
                'r_leg': True,
                'l_leg': True
            },
        'life': 0
    }

    return classes.Character(template)



'''
WEAPON GUI
'''
def weapon_gui(main_master):

    def validate_int(text):
        return text.replace('-','').isdigit() or text==''

    def save_weapon():
        new_weapon = {
            'name': name_e.get(),
            'n_bullets': int(n_bullets_e.get() or 0),
            'dice': int(dice_e.get() or 0),
            'n_dice': int(n_dice_e.get() or 0),
            'dmg_mod': int(dmg_mod_e.get() or 0)
        }
        global weapon_data
        weapon_data = classes.Weapon(new_weapon)
        master.destroy()

    master = tk.Toplevel(main_master)

    name_l = Label(master, text='Name:').grid(row=0, column=0)
    name_e = Entry(master)
    name_e.grid(row=0, column=1)

    n_bullets_l = Label(master, text='N° bullets:').grid(row=1, column=0)
    n_bullets_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    n_bullets_e.grid(row=1, column=1)

    dice_l = Label(master, text='Die').grid(row=2, column=0)
    dice_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    dice_e.grid(row=2, column=1)

    n_dice_l = Label(master, text='N° Dice').grid(row=3, column=0)
    n_dice_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    n_dice_e.grid(row=3, column=1)

    dmg_mod_l = Label(master, text='DMG modifier').grid(row=4, column=0)
    dmg_mod_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    dmg_mod_e.grid(row=4, column=1)

    save = Button(master, text='Save changes', command=save_weapon, background='green').grid(row=5, column=0)

    master.grab_set()
    master.wait_window()
    master.grab_release()

    return weapon_data


'''
PLAYER EDIT
'''
def edit_player_tool(main_master, player_edit):
    master = tk.Toplevel(main_master)
    player = player_edit
    player.print_attributes()

    def validate_int(text):
        return text.replace('-','').isdigit() or text==''

    def insert_entry(entry, text):
        entry.delete(0,END)
        entry.insert(0,text)

    def add_weapon():
        new_weapon = weapon_gui(master)
        player.weapons.append(new_weapon)
        refresh_weapons()

    def delete_weapon():
        selected_weapon_index = weapons_lst.curselection()
        if selected_weapon_index:
            selected_weapon_index = selected_weapon_index[0]
            del player.weapons[selected_weapon_index]
            refresh_weapons()
        else:
            messagebox.showwarning("Warning", "Please select a weapon to delete.")

    def info_weapon():
        selected_weapon_index = weapons_lst.curselection()

        if selected_weapon_index:
            selected_weapon_index = selected_weapon_index[0]

            pop = tk.Toplevel(master)

            for key, item in player.weapons[selected_weapon_index].dictionary.items():
                label_info = Label(pop, text=f'{key}: {item}').pack()
            close = Button(pop, text='Close', command=pop.destroy).pack()

            pop.grab_set()
            pop.wait_window()
            pop.grab_release()

        else:
            messagebox.showwarning("Warning", "Please select a weapon to get info.")

    def refresh_weapons():
        weapons_lst.delete(0, END)
        for weapon in player.weapons:
            weapons_lst.insert(END, weapon.name)
    
    def get_values():
        armor = {
            'head': int(armor_head_e.get() or 0),
            'r_arm': int(armor_rarm_e.get() or 0),
            'l_arm': int(armor_larm_e.get() or 0),
            'torso': int(armor_torso_e.get() or 0),
            'r_leg': int(armor_rleg_e.get() or 0),
            'l_leg': int(armor_lleg_e.get() or 0)
        }
        armor = classes.Armor(armor)

        limbs = {
            'r_arm': rarm_bool.get(),
            'l_arm': larm_bool.get(),
            'r_leg': rleg_bool.get(),
            'l_leg': lleg_bool.get()
        }
        limbs = classes.Limbs(limbs)

        new_player = {
            'player': player_e.get(),
            'name': name_e.get(),
            'btm': int(btm_e.get() or 0),
            'armor': armor,
            'alive': alive_bool.get(),
            'limbs': limbs,
            'life': int(life_e.get() or 0)
        }

        player.actualize(new_player)
        master.destroy()

    # NAME/PLAYER
    player_l = Label(master, text='Player:').grid(row=0, column=0)
    player_e = Entry(master)
    player_e.grid(row=0, column=1)
    insert_entry(player_e, player.player)

    name_l = Label(master, text='Character:').grid(row=1, column=0)
    name_e = Entry(master)
    name_e.grid(row=1, column=1)
    insert_entry(name_e, player.name)


    # WEAPONS
    weapons_l = Label(master, text='Weapons:').grid(row=2, column=0)
    weapons_lst = Listbox(master, selectmode=tk.SINGLE, width=10, height=10)
    weapons_lst.grid(row=2, column=1, columnspan=2)
    refresh_weapons()

    weapon_add = Button(master, text='Add', command=add_weapon).grid(row=3, column=0)
    weapon_delete = Button(master, text='Delete', command=delete_weapon).grid(row=3, column=1)
    weapon_info = Button(master, text='Info', command=info_weapon).grid(row=3, column=2)


    # ARMOR/BTM
    armor_l = Label(master, text='Armor:').grid(row=4, column=0)

    armor_head_l = Label(master, text='Head').grid(row=5, column=0)
    armor_head_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_head_e.grid(row=5, column=1)
    insert_entry(armor_head_e, str(player.armor.head))

    armor_torso_l = Label(master, text='Torso').grid(row=5, column=2)
    armor_torso_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_torso_e.grid(row=5, column=3)
    insert_entry(armor_torso_e, str(player.armor.torso))

    armor_rarm_l = Label(master, text='R.Arm').grid(row=6, column=0)
    armor_rarm_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_rarm_e.grid(row=6, column=1)
    insert_entry(armor_rarm_e, str(player.armor.r_arm))

    armor_larm_l = Label(master, text='L.Arm').grid(row=6, column=2)
    armor_larm_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_larm_e.grid(row=6, column=3)
    insert_entry(armor_larm_e, str(player.armor.l_arm))

    armor_rleg_l = Label(master, text='R.Leg').grid(row=7, column=0)
    armor_rleg_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_rleg_e.grid(row=7, column=1)
    insert_entry(armor_rleg_e, str(player.armor.r_leg))

    armor_lleg_l = Label(master, text='L.Leg').grid(row=7, column=2)
    armor_lleg_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    armor_lleg_e.grid(row=7, column=3)
    insert_entry(armor_lleg_e, str(player.armor.l_leg))

    btm_l = Label(master, text='BTM').grid(row=8, column=0)
    btm_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    btm_e.grid(row=8, column=1)
    insert_entry(btm_e, str(player.btm))

    # LIMBS
    limbs_l = Label(master, text='Limbs:').grid(row=9, column=0)
    rarm_bool = tk.BooleanVar(value=player.limbs.r_arm)
    larm_bool = tk.BooleanVar(value=player.limbs.l_arm)
    rleg_bool = tk.BooleanVar(value=player.limbs.r_leg)
    lleg_bool = tk.BooleanVar(value=player.limbs.l_leg)

    rarm_ck = Checkbutton(master, text='R.Arm', variable=rarm_bool).grid(row=9,column=1)
    larm_ck = Checkbutton(master, text='L.Arm', variable=larm_bool).grid(row=9,column=2)
    rleg_ck = Checkbutton(master, text='R.Leg', variable=rleg_bool).grid(row=9,column=3)
    lleg_ck = Checkbutton(master, text='L.Leg', variable=lleg_bool).grid(row=9,column=4)

    # LIFE/STATUS
    alive_bool = tk.BooleanVar(value=player.alive)
    alive_ck = Checkbutton(master, text='Alive?', variable=alive_bool).grid(row=10, column=0)

    life_l = Label(master, text='Damage taken:').grid(row=11, column=0)
    life_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    life_e.grid(row=11, column=1)
    insert_entry(life_e, str(player.life))

    save = Button(master, text='Save changes', command=get_values, background='green').grid(row=12, column=0, columnspan=2, pady=10)

    master.grab_set()
    master.wait_window()
    master.grab_release()

    return player


'''
DAMGE RESOLVER
'''
def damage_resolve(main_master, player, enemy):
    master = tk.Toplevel(main_master)
    under_cover = tk.BooleanVar(value=False)

    def validate_int(text):
        return text.replace('-','').isdigit() or text==''
    
    def display_cover(under_cover):
        if under_cover:
            cover_cp = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
            cover_cp.grid(row=2, column=1)
        else:
            cover_cp.destroy()
            

    attack_title = f'{player.name} ({player.player}) is going to attack {enemy.name} ({enemy.player})'
    title_l = Label(master, text=attack_title).grid(row=0)
    
    n_shoots_l = Label(master, text='Number of impacts').grid(row=1, column=0)
    n_shoots_e = Entry(master, validate='key', validatecommand=(master.register(validate_int), '%P'))
    n_shoots_e.grid(row=1, column=1)

    cover_ck = Checkbutton(master, text='Cover?', command=lambda: display_cover(under_cover.get()))
    cover_ck.grid(row=2, column=0)

    close_b = Button(master, text='Close', command=master.destroy)
    close_b.grid(row=3, column=0)

    master.grab_set()
    master.wait_window()
    master.grab_release()
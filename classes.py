import numpy as np

class Character:
    def __init__(self, dictionary):
        self.dictionary = dictionary

        self.player = dictionary['player']
        self.name = dictionary['name']
        self.weapons = [Weapon(weapon) for weapon in dictionary['weapons']]
        
        self.btm = dictionary['btm']
        self.armor = Armor(dictionary['armor'])
        self.limbs = Limbs(dictionary['limbs'])

        self.alive = dictionary['alive']
        self.life = dictionary['life']
        self.set_status()

    def actualize(self, dictionary):
        print('actualizando')
        for key, item in dictionary.items():
            setattr(self, key, item)
            try:
                item.__dict__
            except:
                self.dictionary[key] = item
            else:
                for item_key, item_item in [[atr_key, atr_item] for atr_key, atr_item in item.__dict__.items() if atr_key[:1] != '_']:
                    self.dictionary[key][item_key] = item_item

        self.set_status()

    def set_status(self):
        self.status = self.life // 5

    def print_attributes(self):
        for attributes in [atr for atr in self.__dict__.keys() if atr[:1] != '_']:
            print(f'{attributes}: {getattr(self, attributes)}')





class Limbs:
    def __init__(self, dictionary):
        self.r_arm = dictionary['r_arm']
        self.r_leg = dictionary['r_leg']
        self.l_arm = dictionary['l_arm']
        self.l_leg = dictionary['l_leg']




class Weapon:
    def __init__(self, dictionary):
        self.dictionary = dictionary
        
        self.name = dictionary['name']
        self.n_bullets = dictionary['n_bullets']
        self.dice = dictionary['dice']
        self.n_dice = dictionary['n_dice']
        self.dmg_mod = dictionary['dmg_mod']




class Armor:
    def __init__(self, dictionary):
        self.head = dictionary['head']
        self.torso = dictionary['torso']
        self.r_arm = dictionary['r_arm']
        self.l_arm = dictionary['l_arm']
        self.r_leg = dictionary['r_leg']
        self.l_leg = dictionary['l_leg']




class Session:
    def __init__(self, files) -> None:
        self.players = []
        self.dicts = []

        for file in files:
            if file is str:
                player = np.load(file, allow_pickle='TRUE').item()
                self.players.append(Character(player))
                self.dicts.append(player)
            else:
                self.players.append(Character(file))
                self.dicts.append(file)

    def save_session(self, folder):
        for dictionary in self.dicts:
            np.save(folder+'/'+dictionary['player']+'.npy', dictionary)

import os
from random import choice, randint

import pygame

from ..cat.history import History
from ..housekeeping.datadir import get_save_dir
from ..game_structure.windows import ChangeCatName, SpecifyCatGender, KillCat, SaveAsImage

import ujson

from scripts.utility import event_text_adjust, scale, ACC_DISPLAY, process_text, chunks

from .Screens import Screens

from scripts.utility import get_text_box_theme, scale_dimentions, generate_sprite, shorten_text_to_fit, get_cluster
from scripts.cat.cats import Cat, BACKSTORIES
from scripts.cat.pelts import Pelt
from scripts.game_structure import image_cache
import pygame_gui
from re import sub
from scripts.events_module.relationship.pregnancy_events import Pregnancy_Events
from scripts.game_structure.image_button import UIImageButton, UITextBoxTweaked
from scripts.game_structure.game_essentials import game, screen_x, screen_y, MANAGER, screen
from scripts.cat.names import names, Name
from scripts.clan_resources.freshkill import FRESHKILL_ACTIVE

class FlirtScreen(Screens):

    def __init__(self, name=None):
        super().__init__(name)
        self.back_button = None
        self.resource_dir = "resources/dicts/lifegen_talk/"
        self.texts = ""
        self.text_frames = [[text[:i+1] for i in range(len(text))] for text in self.texts]

        self.scroll_container = None
        self.life_text = None
        self.header = None
        self.the_cat = None
        self.text_index = 0
        self.frame_index = 0
        self.typing_delay = 20
        self.next_frame_time = pygame.time.get_ticks() + self.typing_delay
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.text = None
        self.profile_elements = {}
        self.talk_box_img = None


    def screen_switches(self):
        self.update_camp_bg()
        self.hide_menu_buttons()
        self.text_index = 0
        self.frame_index = 0
        self.the_cat = Cat.all_cats.get(game.switches['cat'])
        self.profile_elements = {}
        self.clan_name_bg = pygame_gui.elements.UIImage(
            scale(pygame.Rect((450, 875), (380, 70))),
            pygame.transform.scale(
                image_cache.load_image(
                    "resources/images/clan_name_bg.png").convert_alpha(),
                (500, 870)),
            manager=MANAGER)
        self.profile_elements["cat_name"] = pygame_gui.elements.UITextBox(str(self.the_cat.name),
                                                                          scale(pygame.Rect((500, 870), (-1, 80))),
                                                                          object_id="#text_box_34_horizcenter_light",
                                                                          manager=MANAGER)
        self.texts = self.get_possible_text(self.the_cat)
        self.text_frames = [[text[:i+1] for i in range(len(text))] for text in self.texts]
        self.talk_box_img = image_cache.load_image("resources/images/talk_box.png").convert_alpha()

        self.talk_box = pygame_gui.elements.UIImage(
                scale(pygame.Rect((178, 942), (1248, 302))),
                self.talk_box_img
            )
        self.back_button = UIImageButton(scale(pygame.Rect((50, 50), (210, 60))), "",
                                        object_id="#back_button", manager=MANAGER)
        self.scroll_container = pygame_gui.elements.UIScrollingContainer(scale(pygame.Rect((500, 970), (900, 300))))
        self.text = pygame_gui.elements.UITextBox("", 
                                                  scale(pygame.Rect((0, 0), (900, -100))),
                                                  object_id="#text_box_30_horizleft",
                                                  container=self.scroll_container, manager=MANAGER)
        self.profile_elements["cat_image"] = pygame_gui.elements.UIImage(scale(pygame.Rect((70, 900), (400, 400))),

                                                                         pygame.transform.scale(
                                                                             generate_sprite(self.the_cat),
                                                                             (400, 400)), manager=MANAGER)
        self.paw = pygame_gui.elements.UIImage(
                scale(pygame.Rect((1370, 1180), (30, 30))),
                image_cache.load_image("resources/images/cursor.png").convert_alpha()
            )
        self.paw.visible = False


    def exit_screen(self):
        self.text.kill()
        del self.text
        self.scroll_container.kill()
        del self.scroll_container
        self.back_button.kill()
        del self.back_button
        self.profile_elements["cat_image"].kill()
        self.profile_elements["cat_name"].kill()
        del self.profile_elements
        self.clan_name_bg.kill()
        del self.clan_name_bg
        self.talk_box.kill()
        del self.talk_box
        self.paw.kill()
        del self.paw

    def update_camp_bg(self):
        light_dark = "light"
        if game.settings["dark mode"]:
            light_dark = "dark"

        camp_bg_base_dir = 'resources/images/camp_bg/'
        leaves = ["newleaf", "greenleaf", "leafbare", "leaffall"]
        camp_nr = game.clan.camp_bg

        if camp_nr is None:
            camp_nr = 'camp1'
            game.clan.camp_bg = camp_nr

        available_biome = ['Forest', 'Mountainous', 'Plains', 'Beach']
        biome = game.clan.biome
        if biome not in available_biome:
            biome = available_biome[0]
            game.clan.biome = biome
        biome = biome.lower()

        all_backgrounds = []
        for leaf in leaves:
            platform_dir = f'{camp_bg_base_dir}/{biome}/{leaf}_{camp_nr}_{light_dark}.png'
            all_backgrounds.append(platform_dir)

        self.newleaf_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[0]).convert(), (screen_x, screen_y))
        self.greenleaf_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[1]).convert(), (screen_x, screen_y))
        self.leafbare_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[2]).convert(), (screen_x, screen_y))
        self.leaffall_bg = pygame.transform.scale(
            pygame.image.load(all_backgrounds[3]).convert(), (screen_x, screen_y))
    
    def on_use(self):
        if game.clan.clan_settings['backgrounds']:
            if game.clan.current_season == 'Newleaf':
                screen.blit(self.newleaf_bg, (0, 0))
            elif game.clan.current_season == 'Greenleaf':
                screen.blit(self.greenleaf_bg, (0, 0))
            elif game.clan.current_season == 'Leaf-bare':
                screen.blit(self.leafbare_bg, (0, 0))
            elif game.clan.current_season == 'Leaf-fall':
                screen.blit(self.leaffall_bg, (0, 0))    
        now = pygame.time.get_ticks()
        if self.text_index < len(self.text_frames):
            if now >= self.next_frame_time and self.frame_index < len(self.text_frames[self.text_index]) - 1:
                self.frame_index += 1
                self.next_frame_time = now + self.typing_delay

        if self.text_index == len(self.text_frames) - 1:
            if self.frame_index == len(self.text_frames[self.text_index]) - 1:
                self.paw.visible = True
        # Always render the current frame
        self.text.html_text = self.text_frames[self.text_index][self.frame_index]
        self.text.rebuild()
        self.clock.tick(60)

    def handle_event(self, event):
        if game.switches['window_open']:
            pass
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.back_button:
                self.change_screen('profile screen')
        
        elif event.type == pygame.KEYDOWN and game.settings['keybinds']:
            if event.key == pygame.K_ESCAPE:
                self.change_screen('profile screen')
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.frame_index == len(self.text_frames[self.text_index]) - 1:
                    if self.text_index < len(self.texts) - 1:
                        self.text_index += 1
                        self.frame_index = 0
                else:
                    self.frame_index = len(self.text_frames[self.text_index]) - 1  # Go to the last frame
        return
    
    def get_possible_text(self, cat):
        trait = cat.personality.trait
        cluster, second_cluster = get_cluster(trait)
        success = self.is_flirt_success(cat)
        text = ""
        resource_dir = "resources/dicts/lifegen_talk/"
        possible_texts = None
        with open(f"{resource_dir}flirt.json", 'r') as read_file:
            possible_texts = ujson.loads(read_file.read())
            
        texts_list = []
        for talk in possible_texts.values():
            if game.clan.your_cat.status not in talk[0] and "Any" not in talk[0]:
                continue
            if "heartbroken" not in cat.illnesses.keys() and "heartbroken" in talk[0]:
                continue
            elif not success and "reject" not in talk[0]:
                continue
            elif success and "reject" in talk[0]:
                continue
            if talk[0] and (cluster not in talk[0] and second_cluster not in talk[0]):
                if len(talk[0]) != 1 and len(talk[0]) != 2:
                    continue
                else:
                    if len(talk[0]) == 2 and "reject" not in talk[0]:
                        continue
            if "mate" in talk[0] and cat.ID not in game.clan.your_cat.mate:
                continue
            if ('leafbare' in talk[0] and game.clan.current_season != 'Leaf-bare') or ('newleaf' in talk[0] and game.clan.current_season != 'Newleaf') or ('leaffall' in talk[0] and game.clan.current_season != 'Leaf-bare') or ('greenleaf' in talk[0] and game.clan.current_season != 'Greenleaf'):
                continue
            if any(i in ['bloodthirsty', 'cold', 'gloomy', 'childish', 'faithful', 'strict', 'insecure', "nervous", "lonesome", "vengeful", "fierce"] for i in talk[0]):
                if trait not in talk[0]:
                    continue
            if any(i in ['beach', 'forest', 'plains', 'mountainous', 'wetlands'] for i in talk[0]):
                if game.clan.biome not in talk[0]:
                    continue
            if (not game.clan.your_cat.is_ill() and not game.clan.your_cat.is_injured()) and 'injured' in talk[0]:
                continue
            if (game.clan.your_cat.status == 'kitten') and 'no_kit' in talk[0]:
                continue
            if ("you_insecure" in talk[0]) and game.clan.your_cat.personality.trait != "insecure":
                continue
            if game.clan.your_cat.ID in cat.relationships:
                if cat.relationships[game.clan.your_cat.ID].dislike < 50 and 'hate' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].romantic_love < 30 and 'romantic_like' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].platonic_like < 30 and 'platonic_like' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].jealousy < 30 and 'jealousy' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].dislike < 30 and 'dislike' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].comfortable < 30 and 'comfort' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].admiration < 30 and 'respect' in talk[0]:
                    continue
                if cat.relationships[game.clan.your_cat.ID].trust < 30 and 'trust' in talk[0]:
                    continue
                texts_list.append(talk[1])
            else:
                if any(i in ['hate', 'crush', 'romantic_like', 'platonic_like', 'jealousy', 'dislike', 'comfort', 'respect', 'trust'] for i in talk[0]):
                    continue
                if "talk_dead" in talk[0]:
                    dead_cat = str(Cat.all_cats.get(choice(game.clan.starclan_cats)).name)
                    text = [t1.replace("d_c", dead_cat) for t1 in text]
                    texts_list.append(talk[1])
                    continue
                texts_list.append(talk[1])
        if not texts_list:
            resource_dir = "resources/dicts/lifegen_talk/"
            possible_texts = None
            with open(f"{resource_dir}general.json", 'r') as read_file:
                possible_texts = ujson.loads(read_file.read())
            texts_list.append(possible_texts['general'][1])
        
        text = choice(texts_list)
        text = [t1.replace("c_n", game.clan.name) for t1 in text]
        text = [t1.replace("y_c", str(game.clan.your_cat.name)) for t1 in text]
        text = [t1.replace("r_c", str(Cat.all_cats[choice(game.clan.clan_cats)].name)) for t1 in text]
        return text
    
    
        
    def is_flirt_success(self, cat):
        cat_relationships = cat.relationships.get(game.clan.your_cat.ID)
        chance = 40
        if cat_relationships:
            if cat_relationships.romantic_love > 10:
                chance += 50
            if cat_relationships.platonic_like > 10:
                chance += 20
            if cat_relationships.comfortable > 10:
                chance += 20
            if cat_relationships.admiration > 10:
                chance += 20
            if cat_relationships.dislike > 10:
                chance -= 30
            r = randint(1,100) < chance
            if r:
                cat.relationships.get(game.clan.your_cat.ID).romantic_love += randint(1,10)
                game.clan.your_cat.relationships.get(cat.ID).romantic_love += randint(1,10)
            return r
        else:
            return False
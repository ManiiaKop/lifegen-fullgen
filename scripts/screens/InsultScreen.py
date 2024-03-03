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

class InsultScreen(Screens):

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
    
    def get_cluster_list(self):
        return ["assertive", "brooding", "cool", "upstanding", "introspective", "neurotic", "silly", "stable", "sweet", "unabashed", "unlawful"]
    
    def get_cluster_list_you(self):
        return ["you_assertive", "you_brooding", "you_cool", "you_upstanding", "you_introspective", "you_neurotic", "you_silly", "you_stable", "you_sweet", "you_unabashed", "you_unlawful"]
    
    
    def relationship_check(self, talk, cat_relationship):
        relationship_conditions = {
            'hate': 50,
            'romantic_like': 30,
            'platonic_like': 30,
            'jealousy': 30,
            'dislike': 30,
            'comfort': 30,
            'respect': 30,
            'trust': 30
        }
        
        for key, value in relationship_conditions.items():
            if key in talk[0] and cat_relationship < value:
                return True
        return False
    
    def handle_random_cat(self, cat):
        random_cat = Cat.all_cats.get(choice(game.clan.clan_cats))
        counter = 0
        while random_cat.outside or random_cat.dead or random_cat.ID in [game.clan.your_cat.ID, cat.ID]:
            counter += 1
            if counter == 15:
                break
            random_cat = Cat.all_cats.get(choice(game.clan.clan_cats))
        return random_cat
        
    def get_possible_text(self, cat):
        text = ""
        texts_list = []
        you = game.clan.your_cat

        resource_dir = "resources/dicts/lifegen_talk/"
        possible_texts = None
        with open(f"{resource_dir}{cat.status}.json", 'r') as read_file:
            possible_texts = ujson.loads(read_file.read())
            
        if cat.status not in ['kitten', "newborn"] and you.status not in ['kitten', 'newborn']:
            with open(f"{resource_dir}general_no_kit.json", 'r') as read_file:
                possible_texts2 = ujson.loads(read_file.read())
                possible_texts.update(possible_texts2)
        
        if cat.status not in ['kitten', "newborn"] and you.status in ['kitten', 'newborn']:
            with open(f"{resource_dir}general_you_kit.json", 'r') as read_file:
                possible_texts3 = ujson.loads(read_file.read())
                possible_texts.update(possible_texts3)
        
        cluster1, cluster2 = get_cluster(cat.personality.trait)
        cluster3, cluster4 = get_cluster(you.personality.trait)
        
        their_trait_list = ['troublesome', 'fierce', 'bold', 'daring', 'confident', 'adventurous', 'arrogant', 'competitive', 'rebellious', 'bloodthirsty', 'cold', 'strict', 'vengeful', 'grumpy', 'charismatic', 'sneaky', 'cunning', 'arrogant', 'righteous', 'ambitious', 'strict', 'competitive', 'responsible', 'lonesome', 'righteous', 'calm', 'gloomy', 'wise', 'thoughtful', 'nervous', 'insecure', 'lonesome', 'troublesome', 'childish', 'playful', 'strange', 'loyal', 'responsible', 'wise', 'faithful', 'compassionate', 'faithful', 'loving', 'oblivious', 'sincere', 'childish', 'confident', 'bold', 'shameless', 'strange', 'oblivious', 'flamboyant', 'troublesome', 'bloodthirsty', 'sneaky', 'rebellious']
        you_trait_list = ['you_troublesome', 'you_fierce', 'you_bold', 'you_daring', 'you_confident', 'you_adventurous', 'you_arrogant', 'you_competitive', 'you_rebellious', 'you_bloodthirsty', 'you_cold', 'you_strict', 'you_vengeful', 'you_grumpy', 'you_charismatic', 'you_sneaky', 'you_cunning', 'you_arrogant', 'you_righteous', 'you_ambitious', 'you_strict', 'you_competitive', 'you_responsible', 'you_lonesome', 'you_righteous', 'you_calm', 'you_gloomy', 'you_wise', 'you_thoughtful', 'you_nervous', 'you_insecure', 'you_lonesome', 'you_troublesome', 'you_childish', 'you_playful', 'you_strange', 'you_loyal', 'you_responsible', 'you_wise', 'you_faithful', 'you_compassionate', 'you_faithful', 'you_loving', 'you_oblivious', 'you_sincere', 'you_childish', 'you_confident', 'you_bold', 'you_shameless', 'you_strange', 'you_oblivious', 'you_flamboyant', 'you_troublesome', 'you_bloodthirsty', 'you_sneaky', 'you_rebellious']
        you_backstory_list = [
            "you_clanfounder",
            "you_clanborn",
            "you_outsiderroots",
            "you_half-Clan",
            "you_formerlyloner",
            "you_formerlyrogue",
            "you_formerlykittypet",
            "you_formerlyoutsider",
            "you_originallyanotherclan",
            "you_orphaned",
            "you_abandoned"
        ]
        they_backstory_list = ["they_clanfounder",
            "they_clanborn",
            "they_outsiderroots",
            "they_half-Clan",
            "they_formerlyloner",
            "they_formerlyrogue",
            "they_formerlykittypet",
            "they_formerlyoutsider",
            "they_originallyanotherclan",
            "they_orphaned",
            "they_abandoned"
        ]
        skill_list = ['teacher', 'hunter', 'fighter', 'runner', 'climber', 'swimmer', 'speaker', 'mediator1', 'clever', 'insightful', 'sense', 'kit', 'story', 'lore', 'camp', 'healer', 'star', 'omen', 'dream', 'clairvoyant', 'prophet', 'ghost', 'explorer', 'tracker', 'artistan', 'guardian', 'tunneler', 'navigator', 'song', 'grace', 'clean', 'innovator', 'comforter', 'matchmaker', 'thinker', 'cooperative', 'scholar', 'time', 'treasure', 'fisher', 'language', 'sleeper']
        you_skill_list = ['you_teacher', 'you_hunter', 'you_fighter', 'you_runner', 'you_climber', 'you_swimmer', 'you_speaker', 'you_mediator1', 'you_clever', 'you_insightful', 'you_sense', 'you_kit', 'you_story', 'you_lore', 'you_camp', 'you_healer', 'you_star', 'you_omen', 'you_dream', 'you_clairvoyant', 'you_prophet', 'you_ghost', 'you_explorer', 'you_tracker', 'you_artistan', 'you_guardian', 'you_tunneler', 'you_navigator', 'you_song', 'you_grace', 'you_clean', 'you_innovator', 'you_comforter', 'you_matchmaker', 'you_thinker', 'you_cooperative', 'you_scholar', 'you_time', 'you_treasure', 'you_fisher', 'you_language', 'you_sleeper']
        for talk_key, talk in possible_texts.items():
            tags = talk[0]
            for i in range(len(tags)):
                tags[i] = tags[i].lower()
                
            if "insult" not in tags:
                continue

            # Status tags
            if you.status not in tags and "any" not in tags and "young elder" not in tags and "no_kit" not in tags and "newborn" not in tags:
                continue
            elif "young elder" in tags and cat.status == 'elder' and cat.moons >= 100:
                continue
            elif "no_kit" in tags and you.status in ['kitten', 'newborn']:
                continue
            elif "newborn" in tags and you.moons != 0:
                continue
            
            if "they_grieving" not in tags and "grief stricken" in cat.illnesses:
                continue
            if "they_grieving" in tags and "grief stricken" not in cat.illnesses:
                continue
            
            # Cluster tags
            if any(i in self.get_cluster_list() for i in tags):
                if cluster1 not in tags and cluster2 not in tags:
                    continue
            if any(i in self.get_cluster_list_you() for i in tags):
                if ("you_"+cluster3) not in tags and ("you_"+cluster4) not in tags:
                    continue
            
            # Trait tags
            if any(i in you_trait_list for i in tags):
                ts = you_trait_list
                for j in range(len(ts)):
                    ts[j] = ts[j][3:]
                if you.personality.trait not in ts:
                    continue
            if any(i in their_trait_list for i in tags):
                if cat.personality.trait not in tags:
                    continue
                
            # Backstory tags
            if any(i in you_backstory_list for i in tags):
                ts = you_backstory_list
                for j in range(len(ts)):
                    ts[j] = ts[j][3:]
                if you.backstory not in ts:
                    continue
            if any(i in they_backstory_list for i in tags):
                ts = they_backstory_list
                for j in range(len(ts)):
                    ts[j] = ts[j][4:]
                if cat.backstory not in ts:
                    continue
                
            # Skill tags
            if any(i in you_skill_list for i in tags):
                ts = you_skill_list
                for j in range(len(ts)):
                    ts[j] = ts[j][3:]
                    ts[j] = ''.join([q for q in ts[j] if not q.isdigit()])
                if (you.skills.primary.path not in ts) or (you.skills.secondary.path not in ts):
                    continue
            if any(i in skill_list for i in tags):
                ts = skill_list
                for j in range(len(ts)):
                    ts[j] = ''.join([q for q in ts[j] if not q.isdigit()])
                if (cat.skills.primary.path not in ts) or (cat.skills.secondary.path not in ts):
                    continue
                
            # Season tags
            if ('leafbare' in talk[0] and game.clan.current_season != 'Leaf-bare') or ('newleaf' in talk[0] and game.clan.current_season != 'Newleaf') or ('leaffall' in talk[0] and game.clan.current_season != 'Leaf-bare') or ('greenleaf' in talk[0] and game.clan.current_season != 'Greenleaf'):
                continue
            
            # Biome tags
            if any(i in ['beach', 'forest', 'plains', 'mountainous', 'wetlands', 'desert'] for i in talk[0]):
                if game.clan.biome.lower() not in talk[0]:
                    continue
                
            # Injuries, grieving and illnesses tags
            
            if "you_pregnant" in tags and "pregnant" not in you.injuries:
                continue
            if "they_pregnant" in tags and "pregnant" not in cat.injuries:
                continue
            
            if "grief stricken" not in you.illnesses and "you_grieving" in tags:
                continue
            
            if any(i in ["you_ill", "you_injured"] for i in tags):
                ill_injured = False

                if you.is_ill() and "you_ill" in tags and "grief stricken" not in you.illnesses:
                    for illness in you.illnesses:
                        if you.illnesses[illness]['severity'] == 'major':
                            ill_injured = True
                if you.is_injured() and "you_injured" in tags and "pregnant" not in you.injuries:
                    for injury in you.injuries:
                        if you.injuries[injury]['severity'] == 'major':
                            ill_injured = True
                
                if not ill_injured:
                    continue 
            
            if any(i in ["they_ill", "they_injured"] for i in tags):
                ill_injured = False
                
                if cat.is_ill() and "they_ill" in tags and "grief stricken" not in cat.illnesses:
                    for illness in cat.illnesses:
                        if cat.illnesses[illness]['severity'] == 'major':
                            ill_injured = True
                if cat.is_injured() and "they_injured" in tags and "pregnant" not in cat.injuries:
                    for injury in cat.injuries:
                        if cat.injuries[injury]['severity'] == 'major':
                            ill_injured = True

                if not ill_injured:
                    continue 
            
            # Relationships
            # Family tags:
            if any(i in ["half sibling", "siblings_mate", "cousin", "adopted_sibling", "parents_siblings", "from_mentor", "from_your_apprentice", "from_mate", "from_parent", "adopted_parent", "from_kit", "sibling","from_adopted_kit"] for i in tags):
                
                fam = False
                if "from_mentor" in tags:
                    if you.mentor == cat.ID:
                        fam = True
                if "from_your_apprentice" in tags:
                    if cat.mentor == you.ID:
                        fam = True
                if "from_mate" in tags:
                    if cat.ID in you.mate:
                        fam = True   
                if "from_parent" in tags:
                    if you.parent1:
                        if you.parent1 == cat.ID:
                            fam = True
                    if you.parent2:
                        if you.parent2 == cat.ID:
                            fam = True
                if "adopted_parent" in tags:
                    if cat.ID in you.inheritance.get_no_blood_parents():
                        fam = True
                if "from_kit" in tags:
                    if cat.ID in you.inheritance.get_blood_kits():
                        fam = True
                if "from_adopted_kit" in tags:
                    if cat.ID in you.inheritance.get_not_blood_kits():
                        fam = True

                if "sibling" in tags:
                    if cat.ID in you.inheritance.get_siblings():
                        fam = True
                if "half sibling" in tags:
                    c_p1 = cat.parent1
                    if not c_p1:
                        c_p1 = "no_parent1_cat"
                    c_p2 = cat.parent2
                    if not c_p2:
                        c_p2 = "no_parent2_cat"
                    y_p1 = you.parent1
                    if not y_p1:
                        y_p1 = "no_parent1_you"
                    y_p2 = you.parent2
                    if not y_p2:
                        y_p2 = "no_parent2_you"
                    if ((c_p1 == y_p1 or c_p1 == y_p2) or (c_p2 == y_p1 or c_p2 == y_p2)) and not (c_p1 == y_p1 and c_p2 == y_p2) and not (c_p2 == y_p1 and c_p1 == y_p2) and not (c_p1 == y_p2 and c_p2 == y_p1):
                        fam = True
                if "adopted_sibling" in tags:
                    if cat.ID in you.inheritance.get_no_blood_siblings():
                        fam = True
                if "parents_siblings" in tags:
                    if cat.ID in you.inheritance.get_parents_siblings():
                        fam = True
                if "cousin" in tags:
                    if cat.ID in you.inheritance.get_cousins():
                        fam = True
                if "siblings_mate" in tags:
                    if cat.ID in you.inheritance.get_siblings_mates():
                        fam = True
                if not fam:
                    continue
                

            if "non-related" in tags:
                if cat.ID in you.inheritance.all_inheritances:
                    continue
                
            # If you have murdered someone and have been revealed
            if "murder" in talk[0]:
                if game.clan.your_cat.revealed:
                    if game.clan.your_cat.history:
                        if "is_murderer" in game.clan.your_cat.history.murder:
                            if len(game.clan.your_cat.history.murder["is_murderer"]) == 0:
                                continue
                            elif 'accomplices' in game.switches:
                                if cat.ID in game.switches['accomplices']:
                                    continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            
            if "war" in tags:
                if game.clan.war.get("at_war", False):
                    continue
        
            
            # Relationship conditions
            if you.ID in cat.relationships:
                if cat.relationships[you.ID].dislike < 30 and 'hate' in tags:
                    continue
                if cat.relationships[you.ID].romantic_love < 20 and 'romantic_like' in tags:
                    continue
                if cat.relationships[you.ID].platonic_like < 20 and 'platonic_like' in tags:
                    continue
                if cat.relationships[you.ID].platonic_like < 50 and 'platonic_love' in tags:
                    continue
                if cat.relationships[you.ID].jealousy < 5 and 'jealousy' in tags:
                    continue
                if cat.relationships[you.ID].dislike < 20 and 'dislike' in tags:
                    continue
                if cat.relationships[you.ID].comfortable < 5 and 'comfort' in tags:
                    continue
                if cat.relationships[you.ID].admiration < 5 and 'respect' in tags:
                    continue         
                if cat.relationships[you.ID].trust < 5 and 'trust' in tags:
                    continue
                if cat.relationships[you.ID].platonic_like > 10 and cat.relationships[you.ID].dislike > 10 and "neutral" in tags:
                    continue
            else:
                if any(i in ["hate","romantic_like","platonic_like","jealousy","dislike","comfort","respect","trust"] for i in tags):
                    continue
            
            if "talk_dead" in talk[0]:
                dead_cat = str(Cat.all_cats.get(choice(game.clan.starclan_cats)).name)
                text = [t1.replace("d_c", dead_cat) for t1 in talk[1]]
            
            if "random_cat" in talk[0]:
                random_cat = Cat.all_cats.get(choice(game.clan.clan_cats))
                counter = 0
                while random_cat.outside or random_cat.dead or random_cat.ID == you.ID or random_cat.ID == cat.ID:
                    counter+=1
                    if counter == 15:
                        continue
                    random_cat = Cat.all_cats.get(choice(game.clan.clan_cats))
                text = [t1.replace("r_c", str(random_cat.name)) for t1 in talk[1]]
                texts_list.append(text)
                continue
           
            texts_list.append(talk[1])
            
        if not texts_list:
            resource_dir = "resources/dicts/lifegen_talk/"
            possible_texts = None
            with open(f"{resource_dir}general.json", 'r') as read_file:
                possible_texts = ujson.loads(read_file.read())
            texts_list.append(possible_texts['general'][1])

        text = choice(texts_list)

        if any(abbrev in t for abbrev in ["r_k", "r_a", "r_w", "r_m", "r_d", "r_q", "r_e", "r_s", "r_i"] for t in text):
            living_meds = []
            living_mediators = []
            living_warriors = []
            living_apprentices = []
            living_queens = []
            living_kits = []
            living_elders = []
            sick_cats = []
            injured_cats = []
            
            for c in Cat.all_cats.values():
                if not c.dead and not c.outside and c.ID != you.ID and c.ID != cat.ID:
                    if c.status == "medicine cat":
                        living_meds.append(c)
                    elif c.status == "warrior":
                        living_warriors.append(c)
                    elif c.status == "mediator":
                        living_mediators.append(c)
                    elif c.status == 'queen':
                        living_queens.append(c)
                    elif c.status in ["apprentice", "medicine cat apprentice", "mediator apprentice", "queen's apprentice"]:
                        living_apprentices.append(c)
                    elif c.status in ["kitten", "newborn"]:
                        living_kits.append(c)
                    elif c.status == "elder":
                        living_elders.append(c)

            replace_mappings = {
                "r_k": living_kits,
                "r_a": living_apprentices,
                "r_w": living_warriors,
                "r_m": living_meds,
                "r_d": living_mediators,
                "r_q": living_queens,
                "r_e": living_elders
            }
            
            for abbrev, replace_list in replace_mappings.items():
                for idx, t in enumerate(text):
                    if abbrev in t:
                        text[idx] = t.replace(abbrev, str(choice(replace_list).name))
                        

        text = [t1.replace("c_n", game.clan.name) for t1 in text]
        text = [t1.replace("y_c", str(you.name)) for t1 in text]
        text = [t1.replace("t_c", str(cat.name)) for t1 in text]   
         
        other_clan = choice(game.clan.all_clans)
        if other_clan:
            text = [t1.replace("o_c", str(other_clan.name)) for t1 in text]
        if game.clan.leader:
            lead = game.clan.leader.name
            text = [t1.replace("l_n", str(lead)) for t1 in text]
        if game.clan.deputy:
            dep = game.clan.deputy.name
            text = [t1.replace("d_n", str(dep)) for t1 in text]
        if cat.mentor:
            mentor = Cat.all_cats.get(cat.mentor).name
            text = [t1.replace("tm_n", str(mentor)) for t1 in text]
        if you.mentor:
            mentor = Cat.all_cats.get(you.mentor).name
            text = [t1.replace("m_n", str(mentor)) for t1 in text]
        if "grief stricken" in cat.illnesses:
            try:
                dead_cat = Cat.all_cats.get(cat.illnesses['grief stricken'].get("grief_cat"))
                text = [t1.replace("d_c", str(dead_cat.name)) for t1 in text]  
            except:
                dead_cat = str(Cat.all_cats.get(game.clan.starclan_cats[-1]).name)
                text = [t1.replace("d_c", dead_cat) for t1 in text]    
        elif "grief stricken" in you.illnesses:
            try:
                dead_cat = Cat.all_cats.get(you.illnesses['grief stricken'].get("grief_cat"))
                text = [t1.replace("d_c", str(dead_cat.name)) for t1 in text]  
            except:
                dead_cat = str(Cat.all_cats.get(game.clan.starclan_cats[-1]).name)
                text = [t1.replace("d_c", dead_cat) for t1 in text]
        d_c_found = False
        for t in text:
            if "d_c" in t:
                d_c_found = True
        if d_c_found:
            dead_cat = str(Cat.all_cats.get(game.clan.starclan_cats[-1]).name)
            text = [t1.replace("d_c", dead_cat) for t1 in text]
        return text
import pygame.transform
import pygame_gui.elements
from random import choice, randint
import ujson

from scripts.cat_relations.inheritance import Inheritance
from scripts.cat.history import History
from scripts.event_class import Single_Event
from scripts.events import events_class

from .Screens import Screens
from scripts.utility import get_personality_compatibility, get_text_box_theme, scale, scale_dimentions, shorten_text_to_fit
from scripts.game_structure.ui_elements import IDImageButton, UIImageButton, UISpriteButton
from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
from scripts.cat.pelts import Pelt
from scripts.game_structure.windows import GameOver, PickPath, DeathScreen
from scripts.game_structure.game_essentials import game, screen, screen_x, screen_y, MANAGER
from scripts.game_structure.windows import RelationshipLog
from scripts.game_structure.propagating_thread import PropagatingThread

class MurderScreen(Screens):
    selected_cat = None
    current_page = 1
    list_frame = pygame.transform.scale(image_cache.load_image("resources/images/choosing_frame.png").convert_alpha(),
                                        (1300 / 1600 * screen_x, 452 / 1400 * screen_y))
    apprentice_details = {}
    selected_details = {}
    cat_list_buttons = {}
    stage = 'choose murder cat'

    def __init__(self, name=None):
        super().__init__(name)
        self.list_page = None
        self.next_cat = None
        self.previous_cat = None
        self.next_page_button = None
        self.previous_page_button = None
        self.current_mentor_warning = None
        self.confirm_mentor = None
        self.back_button = None
        self.next_cat_button = None
        self.previous_cat_button = None
        self.mentor_icon = None
        self.app_frame = None
        self.mentor_frame = None
        self.current_mentor_text = None
        self.info = None
        self.heading = None
        self.mentor = None
        self.the_cat = None
        self.murder_cat = None
        self.next = None
        self.murderimg = None
        
    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.cat_list_buttons.values():
                self.selected_cat = event.ui_element.return_cat_object()
                self.update_selected_cat()

            elif event.ui_element == self.confirm_mentor and self.selected_cat and self.stage == 'choose murder cat':
                if not self.selected_cat.dead:
                    self.exit_screen()
                    self.update_selected_cat()
                    self.cat_to_murder = self.selected_cat
                    self.stage = 'choose accomplice'
                    self.screen_switches()
            
            elif event.ui_element == self.confirm_mentor and self.selected_cat:
                    r = randint(1,100)
                    accompliced = False
                    chance = self.get_accomplice_chance(game.clan.your_cat, self.selected_cat)
                    if game.config["accomplice_chance"] != -1:
                        try:
                            chance = game.config["accomplice_chance"]
                        except:
                            pass
                    if r < chance:
                        accompliced = True
                        if 'accomplices' in game.switches:
                            game.switches['accomplices'].append(self.selected_cat.ID)
                        else:
                            game.switches['accomplices'] = []
                            game.switches['accomplices'].append(self.selected_cat.ID)
                                                
                    self.change_cat(self.murder_cat, self.selected_cat, accompliced)
                    self.stage = 'choose murder cat'
                

            elif self.stage == 'choose accomplice' and event.ui_element == self.next:
                    self.change_cat(self.murder_cat, None, None)
                    self.stage = 'choose murder cat'
            
            elif event.ui_element == self.back_button:
                self.change_screen('profile screen')
                self.stage = 'choose murder cat'

            elif event.ui_element == self.next_cat_button:
                if isinstance(Cat.fetch_cat(self.next_cat), Cat):
                    game.switches['cat'] = self.next_cat
                    self.update_cat_list()
                    self.update_selected_cat()
                    # self.update_buttons()
                else:
                    print("invalid next cat", self.next_cat)
            elif event.ui_element == self.previous_cat_button:
                if isinstance(Cat.fetch_cat(self.previous_cat), Cat):
                    game.switches['cat'] = self.previous_cat
                    self.update_cat_list()
                    self.update_selected_cat()
                    # self.update_buttons()
                else:
                    print("invalid previous cat", self.previous_cat)
            elif event.ui_element == self.next_page_button:
                self.current_page += 1
                self.update_cat_list()
            elif event.ui_element == self.previous_page_button:
                self.current_page -= 1
                self.update_cat_list()

    def screen_switches(self):

        if self.stage == 'choose murder cat':
            self.the_cat = game.clan.your_cat
            self.mentor = Cat.fetch_cat(self.the_cat.mentor)
            self.selected_cat = None
            self.next = None
            self.heading = pygame_gui.elements.UITextBox("Choose your target",
                                                        scale(pygame.Rect((300, 50), (1000, 80))),
                                                        object_id=get_text_box_theme("#text_box_34_horizcenter"),
                                                        manager=MANAGER)
            
            # Layout Images:
            self.mentor_frame = pygame_gui.elements.UIImage(scale(pygame.Rect((200, 226), (569, 399))),
                                                            pygame.transform.scale(
                                                                image_cache.load_image(
                                                                    "resources/images/murder_select.png").convert_alpha(),
                                                                (569, 399)), manager=MANAGER)
            self.murderimg = pygame_gui.elements.UIImage(scale(pygame.Rect((850, 150), (446, 494))),
                                                            pygame.transform.scale(
                                                                image_cache.load_image(
                                                                    "resources/images/choose_victim.png").convert_alpha(),
                                                                (446, 494)), manager=MANAGER)
    
            
            self.back_button = UIImageButton(scale(pygame.Rect((50, 1290), (210, 60))), "", object_id="#back_button")
            self.confirm_mentor = UIImageButton(scale(pygame.Rect((270, 610), (208, 52))), "",
                                                object_id="#patrol_select_button")
        
            self.previous_page_button = UIImageButton(scale(pygame.Rect((630, 1155), (68, 68))), "",
                                                    object_id="#relation_list_previous", manager=MANAGER)
            self.next_page_button = UIImageButton(scale(pygame.Rect((902, 1155), (68, 68))), "",
                                                object_id="#relation_list_next", manager=MANAGER)

            self.update_selected_cat()  # Updates the image and details of selected cat
            self.update_cat_list()
        else:
            self.the_cat = game.clan.your_cat
            self.mentor = Cat.fetch_cat(self.the_cat.mentor)
            self.selected_cat = None

            self.heading = pygame_gui.elements.UITextBox("Choose an accomplice",
                                                        scale(pygame.Rect((300, 50), (1000, 80))),
                                                        object_id=get_text_box_theme("#text_box_34_horizcenter"),
                                                        manager=MANAGER)
            
            # Layout Images:
            self.mentor_frame = pygame_gui.elements.UIImage(scale(pygame.Rect((200, 226), (569, 399))),
                                                            pygame.transform.scale(
                                                                image_cache.load_image(
                                                                    "resources/images/murder_select.png").convert_alpha(),
                                                                (569, 399)), manager=MANAGER)

            
            self.murderimg = pygame_gui.elements.UIImage(scale(pygame.Rect((850, 150), (446, 494))),
                                                            pygame.transform.scale(
                                                                image_cache.load_image(
                                                                    "resources/images/proceed_accomplice.png").convert_alpha(),
                                                                (446, 494)), manager=MANAGER)

            self.back_button = UIImageButton(scale(pygame.Rect((50, 1290), (210, 60))), "", object_id="#back_button")
            self.confirm_mentor = UIImageButton(scale(pygame.Rect((235, 610), (208, 52))), "",
                                                object_id="#patrol_select_button")
        
            self.previous_page_button = UIImageButton(scale(pygame.Rect((630, 1155), (68, 68))), "",
                                                    object_id="#relation_list_previous", manager=MANAGER)
            self.next_page_button = UIImageButton(scale(pygame.Rect((902, 1155), (68, 68))), "",
                                                object_id="#relation_list_next", manager=MANAGER)
            
            self.next = UIImageButton(scale(pygame.Rect((450, 595), (68, 68))), "",
                                                tool_tip_text= "Proceed without an accomplice.",
                                                object_id="#relation_list_next", manager=MANAGER)

            self.update_selected_cat2()  # Updates the image and details of selected cat
            self.update_cat_list2()


    def exit_screen(self):

       
        for ele in self.cat_list_buttons:
            self.cat_list_buttons[ele].kill()
        self.cat_list_buttons = {}

        for ele in self.apprentice_details:
            self.apprentice_details[ele].kill()
        self.apprentice_details = {}

        for ele in self.selected_details:
            self.selected_details[ele].kill()
        self.selected_details = {}
        
        if self.heading:
            self.heading.kill()
            del self.heading
        
        if self.murderimg:
            self.murderimg.kill()
            del self.murderimg

        if self.mentor_frame:
            self.mentor_frame.kill()
            del self.mentor_frame

        if self.back_button:
            self.back_button.kill()
            del self.back_button
        if self.confirm_mentor:
            self.confirm_mentor.kill()
            del self.confirm_mentor
        if self.previous_page_button:
            self.previous_page_button.kill()
            del self.previous_page_button
            
        if self.next_page_button:
            self.next_page_button.kill()
            del self.next_page_button
        
        if self.next:
            self.next.kill()
            del self.next

    def find_next_previous_cats(self):
        """Determines where the previous and next buttons lead"""
        is_instructor = False
        if self.the_cat.dead and game.clan.instructor.ID == self.the_cat.ID:
            is_instructor = True

        self.previous_cat = 0
        self.next_cat = 0
        if self.the_cat.dead and not is_instructor and not self.the_cat.df:
            self.previous_cat = game.clan.instructor.ID

        if is_instructor:
            self.next_cat = 1

        for check_cat in Cat.all_cats_list:
            if check_cat.ID == self.the_cat.ID:
                self.next_cat = 1

            if self.next_cat == 0 and check_cat.ID != self.the_cat.ID and check_cat.dead == self.the_cat.dead and \
                    check_cat.ID != game.clan.instructor.ID and not check_cat.exiled and check_cat.status in \
                    ["apprentice", "medicine cat apprentice", "mediator apprentice", "queen's apprentice"] \
                    and check_cat.df == self.the_cat.df:
                self.previous_cat = check_cat.ID

            elif self.next_cat == 1 and check_cat.ID != self.the_cat.ID and check_cat.dead == self.the_cat.dead and \
                    check_cat.ID != game.clan.instructor.ID and not check_cat.exiled and check_cat.status in \
                    ["apprentice", "medicine cat apprentice", "mediator apprentice", "queen's apprentice"] \
                    and check_cat.df == self.the_cat.df:
                self.next_cat = check_cat.ID

            elif int(self.next_cat) > 1:
                break

        if self.next_cat == 1:
            self.next_cat = 0

    def change_cat(self, new_mentor=None, accomplice=None, accompliced=None):
        self.exit_screen()
        r = randint(0,100)
        r2 = randint(-10, 10)
        chance = self.get_kill(game.clan.your_cat, self.cat_to_murder, accomplice, accompliced)
        if game.config["murder_chance"] != -1:
            try:
                chance = game.config["murder_chance"]
            except:
                pass
        murdered = r < max(5, chance + r2)
        you = game.clan.your_cat
        cat_to_murder = self.cat_to_murder
        game.clan.murdered = True
        if murdered:
            self.choose_murder_text(you, cat_to_murder, accomplice, accompliced)
        else:
            self.handle_murder_fail(you, cat_to_murder, accomplice, accompliced)

        game.switches['cur_screen'] = "events screen"
    
    RESOURCE_DIR = "resources/dicts/events/lifegen_events/"
    def choose_murder_text(self, you, cat_to_murder, accomplice, accompliced):
        with open(f"{self.RESOURCE_DIR}murder.json",
                encoding="ascii") as read_file:
            self.m_txt = ujson.loads(read_file.read())
        with open(f"{self.RESOURCE_DIR}murder_unsuccessful.json",
                encoding="ascii") as read_file:
            self.mu_txt = ujson.loads(read_file.read())
            
        try:
            ceremony_txt = self.m_txt["murder " + game.clan.your_cat.status.replace(" ", "") + " " + cat_to_murder.status.replace(" ", "")]
            ceremony_txt.extend(self.m_txt["murder general"])
            ceremony_txt = choice(ceremony_txt)
        except:
            ceremony_txt = choice(self.m_txt["murder general"])
            
        other_clan = choice(game.clan.all_clans)
        ceremony_txt = ceremony_txt.replace('v_c', str(cat_to_murder.name))
        ceremony_txt = ceremony_txt.replace('c_n', game.clan.name)
        ceremony_txt = ceremony_txt.replace("o_c", str(other_clan.name))
        if cat_to_murder.status == 'leader':
            game.clan.leader_lives = 0
        cat_to_murder.die()
        game.cur_events_list.insert(0, Single_Event(ceremony_txt))

        discover_chance = self.get_discover_chance(you, cat_to_murder, accomplice, accompliced)
        r_num = randint(1,100)

        discover_chance = 2
        r_num = 3
        # debug ^^

        discovered = False
        if r_num < discover_chance:
            discovered = True
        else:
            discovered = False
            
        if discovered:
            if accomplice and accompliced:
                game.cur_events_list.insert(1, Single_Event("You successfully murdered "+ str(cat_to_murder.name) + " with the help of " + str(accomplice.name) + "."))
                History.add_death(cat_to_murder, f"{you.name} and {accomplice.name} murdered this cat.")
                History.add_murders(cat_to_murder, accomplice, True, f"{you.name} murdered this cat along with {accomplice.name}.")
                History.add_murders(cat_to_murder, you, True, f"{you.name} murdered this cat with the help of {accomplice.name}.")
                
                accguiltchance = randint(1,2)
                if accguiltchance == 1:
                    accomplice.get_injured("guilt")

                youguiltchance = randint(1,4)
                if youguiltchance == 1:
                    accomplice.get_injured("guilt")

            else:
                game.cur_events_list.insert(1, Single_Event("You successfully murdered "+ str(cat_to_murder.name) + "."))
                History.add_death(cat_to_murder, f"{you.name} murdered this cat.")
                History.add_murders(cat_to_murder, you, True, f"{you.name} murdered this cat.")
            self.choose_discover_punishment(you, cat_to_murder, accomplice, accompliced)
        else:
            game.clan.focus = "unknown_murder"
            game.clan.focus_cat = cat_to_murder
            if accomplice:
                if accompliced:
                    History.add_death(cat_to_murder, f"{you.name} and {accomplice.name} murdered this cat.")
                    History.add_murders(cat_to_murder, you, True, f"{you.name} murdered this cat along with {accomplice.name}.")
                    History.add_murders(cat_to_murder, accomplice, True, f"{you.name} murdered this cat along with {accomplice.name}.")
                    game.cur_events_list.insert(1, Single_Event("You successfully murdered "+ str(cat_to_murder.name) + " along with " + str(accomplice.name) + ". It seems no one is aware of your actions."))

                    accguiltchance = randint(1,4)
                    if accguiltchance == 1:
                        accomplice.get_injured("guilt")

                    youguiltchance = randint(1,6)
                    if youguiltchance == 1:
                        accomplice.get_injured("guilt")


                else:
                    History.add_death(cat_to_murder, f"{you.name} murdered this cat.")
                    History.add_murders(cat_to_murder, you, True, f"{you.name} murdered this cat.")
                    game.cur_events_list.insert(1, Single_Event("You successfully murdered "+ str(cat_to_murder.name) + " but " + str(accomplice.name) + " chose not to help. It seems no one is aware of your actions."))
            else:
                History.add_death(cat_to_murder, f"{you.name} murdered this cat.")
                History.add_murders(cat_to_murder, you, True, f"{you.name} murdered this cat.")
                game.cur_events_list.insert(1, Single_Event("You successfully murdered "+ str(cat_to_murder.name) + ". It seems no one is aware of your actions."))
        
        
          
    def choose_discover_punishment(self, you, cat_to_murder, accomplice, accompliced):
        # 1 = you punished, 2 = accomplice punished, 3 = both punished
        punishment_chance = randint(1,3)
        if not accomplice or not accompliced:
            punishment_chance = 1
        if punishment_chance == 1:
            if accomplice and not accompliced:
                a_s = randint(1,2)
                if a_s == 1 and accomplice.status != "leader":
                    game.cur_events_list.insert(2, Single_Event(f"Shocked at your request to be an accomplice to murder, {accomplice.name} reports your actions to the Clan leader."))
                you.shunned = 1
            txt = ""
            if game.clan.your_cat.status in ['kitten', 'leader', 'deputy', 'medicine cat']:
                txt = choice(self.mu_txt["murder_discovered " + game.clan.your_cat.status])
            else:
                txt = choice(self.mu_txt["murder_discovered general"])
            txt = txt.replace('v_c', str(cat_to_murder.name))
            game.cur_events_list.insert(2, Single_Event(txt))
            you.shunned = 1
            you.faith -= 0.5
        elif punishment_chance == 2:
            txt = f"{accomplice.name} is blamed for the murder of v_c. However, you were not caught."
            txt = txt.replace('v_c', str(cat_to_murder.name))
            game.cur_events_list.insert(2, Single_Event(txt))
            accomplice.shunned = 1
            accomplice.faith -= 0.5
        else:
            txt = f"The unsettling truth of v_c's death is discovered, with you and {accomplice.name} responsible. The Clan decides both of your punishments."
            txt = txt.replace('v_c', str(cat_to_murder.name))
            game.cur_events_list.insert(2, Single_Event(txt))
            you.shunned = 1
            accomplice.shunned = 1
            accomplice.faith -= 0.5
        
        if punishment_chance == 1 or punishment_chance == 3:
            kit_punishment = ["You are assigned counseling by the Clan's medicine cat to help you understand the severity of your actions and to guide you to make better decisions in the future.",
                                "You are to be kept in the nursery under the watchful eye of the queens at all times until you become an apprentice."]
            gen_punishment = ["You are assigned counseling by the Clan's medicine cat to help you understand the severity of your actions and to guide you to make better decisions in the future.",
                                "You will be required to take meals last and are forced to sleep in a separate den away from your clanmates.",
                                "You are assigned to several moons of tasks that include cleaning out nests, checking elders for ticks, and other chores alongside your normal duties.",
                                "You are assigned a mentor who will better educate you about the Warrior Code and the sacredness of life."]
            # demote_leader = ["Your lives will be stripped away and you will be demoted to a warrior, no longer trusted to be the Clan's leader."]
            # demote_deputy = ["The Clan decides that you will be demoted to a warrior, no longer trusting you as their deputy."]
            # demote_medicine_cat = ["The Clan decides that you will be demoted to a warrior, no longer trusting you as their medicine cat."]
            # exiled = ["The Clan decides that they no longer feel safe with you as a Clanmate. You will be exiled from the Clan."]
            
            if you.status == 'kitten' or you.status == 'newborn':
                game.cur_events_list.insert(3, Single_Event(choice(kit_punishment)))
            elif you.status == 'leader':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
            elif you.status == 'deputy':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
            elif you.status == 'medicine cat':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
            else:
                lead_choice = randint(1,5)
                if lead_choice in [1, 2, 3, 4]:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
        
        if accomplice and accompliced and (punishment_chance == 2 or punishment_chance == 3):
            a_n = str(accomplice.name)
            kit_punishment = [f"{a_n} is assigned counseling by the Clan's medicine cat to help them understand the severity of their actions and to guide them to make better decisions in the future.",
                            f"{a_n} is to be kept in the nursery under the watchful eye of the queens at all times until they become an apprentice."]
            gen_punishment = [f"{a_n} is assigned counseling by the Clan's medicine cat to help them understand the severity of their actions and to guide them to make better decisions in the future.",
                                f"{a_n} is required to take meals last and is forced to sleep in a separate den away from their clanmates.",
                                f"{a_n} is assigned to several moons of tasks that include cleaning out nests, checking elders for ticks, and other chores alongside their normal duties.",
                                f"{a_n} is assigned a mentor who will better educate them about the Warrior Code and the sacredness of life."]
            
            # demote_leader = [f"{a_n}'s lives will be stripped away and they will be demoted to a warrior, no longer trusted to be the Clan's leader."]
            # demote_deputy = [f"The Clan decides that {a_n} will be demoted to a warrior, no longer trusting them as their deputy."]
            # demote_medicine_cat = [f"The Clan decides that {a_n} will be demoted to a warrior, no longer trusting them as their medicine cat."]
            # exiled = [f"The Clan decides that they no longer feel safe with {a_n} as a Clanmate. They will be exiled from the Clan."]

            if accomplice.status == 'kitten' or accomplice.status == 'newborn':
                game.cur_events_list.insert(3, Single_Event(choice(kit_punishment)))
            elif accomplice.status == 'leader':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
                
            elif accomplice.status == 'deputy':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
               
            elif accomplice.status == 'medicine cat':
                lead_choice = randint(1,3)
                if lead_choice == 1:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
                
            else:
                lead_choice = randint(1,5)
                if lead_choice in [1, 2, 3, 4]:
                    game.cur_events_list.insert(3, Single_Event(choice(gen_punishment)))
    
    def get_discover_chance(self, you, cat_to_murder, accomplice=None, accompliced=None):
        chance = 30
        if you.status == 'kitten':
            chance += 40
        elif you.age == 'adolescent':
            chance += 30
        if you.experience >= 100:
            chance -= 10
        elif you.experience <= 30:
            chance += 20
        if cat_to_murder.status in ['leader', 'deputy', 'medicine cat']:
            chance += 20
        if you.status in ['leader', 'deputy', 'medicine cat']:
            chance -= 10
        if accomplice and accompliced:
            chance -= 10
        return chance + randint(-10,10)

    def handle_murder_fail(self, you, cat_to_murder, accomplice, accompliced):
        c_m = str(cat_to_murder.name)
        discover_chance = randint(1,2)
        fail_texts = []
        if discover_chance == 1:
            fail_texts = ["You attempted to murder "+ c_m + ", but were unsuccessful. They were oblivious of your attempt.",
                            "You attempted to murder "+ c_m + ", but they sidestepped the peril you'd arranged. They remained oblivious to your intent.",
                            "You made an effort to end "+ c_m + "'s life, but fortune favored them. They were none the wiser of your deadly plot.",
                            "Your plot to murder "+ c_m + " fell through, and they went about their day, unaware of the fate you'd intended for them.",
                            "Despite your best efforts, "+ c_m + " remained unscathed. They continued on, blissfully ignorant of your lethal plan.",
                            "Your attempt to kill "+ c_m + " proved futile, and they stayed clueless about your ominous intentions."]
        else:
            if accomplice and accompliced:
                fail_texts = [f"You attempted to murder {c_m}, but your plot was unsuccessful. They appear to be slightly wary of you and {accomplice.name} now.",
                                f"Your effort to end {c_m}'s life was thwarted, and they now seem a bit more cautious around you and {accomplice.name}.",
                                f"Despite your intent to murder {c_m}, they remained unscathed. They now look at you and {accomplice.name} with a hint of suspicion.",
                                f"You and {accomplice.name} tried to kill {c_m}, but they survived. They now seem to watch you both with wary eyes.",
                                f"Your plot to murder {c_m} fell through, and they remain alive, now showing signs of mild suspicion towards you and {accomplice.name}."]
                cat_to_murder.relationships[you.ID].dislike += randint(1,20)
                cat_to_murder.relationships[you.ID].platonic_like -= randint(1,15)
                cat_to_murder.relationships[you.ID].comfortable -= randint(1,15)
                cat_to_murder.relationships[you.ID].trust -= randint(1,15)
                cat_to_murder.relationships[you.ID].admiration -= randint(1,15)
                cat_to_murder.relationships[accomplice.ID].dislike += randint(1,20)
                cat_to_murder.relationships[accomplice.ID].platonic_like -= randint(1,15)
                cat_to_murder.relationships[accomplice.ID].comfortable -= randint(1,15)
                cat_to_murder.relationships[accomplice.ID].trust -= randint(1,15)
                cat_to_murder.relationships[accomplice.ID].admiration -= randint(1,15)                
            else:
                fail_texts = ["You attempted to murder "+ c_m + ", but your plot was unsuccessful. They appear to be slightly wary now.",
                                "Your effort to end "+ c_m + "'s life was thwarted, and they now seem a bit more cautious around you.",
                                "Despite your intent to murder "+ c_m + ", they remained unscathed. They look at you now with a hint of suspicion.",
                                "You tried to kill "+ c_m + ", but they survived. They now seem to watch you with wary eyes.",
                                "Your plot to murder "+ c_m + " fell through, and they remain alive, now showing signs of mild suspicion towards you."]
                cat_to_murder.relationships[you.ID].dislike += randint(1,20)
                cat_to_murder.relationships[you.ID].platonic_like -= randint(1,15)
                cat_to_murder.relationships[you.ID].comfortable -= randint(1,15)
                cat_to_murder.relationships[you.ID].trust -= randint(1,15)
                cat_to_murder.relationships[you.ID].admiration -= randint(1,15)
        game.cur_events_list.insert(0, Single_Event(choice(fail_texts)))
        
    
    status_chances = {
        'warrior': 40,
        'medicine cat': 40,
        'mediator': 35,
        'apprentice': 30,
        'medicine cat apprentice': 25,
        'mediator apprentice': 20,
        "queen": 25,
        "queen's apprentice": 20,
        'deputy': 50,
        'leader': 60,
        'elder': 25,
        'kitten': 10,
    }

    skill_chances = {
        'warrior': -5,
        'medicine cat': -5,
        'mediator': 0,
        'apprentice': 5,
        'medicine cat apprentice': 5,
        'mediator apprentice': 5,
        "queen's apprentice": 10,
        'queen': 5,
        'deputy': -10,
        'leader': -15,
        'elder': 5,
        'kitten': 30
    }

    murder_skills = ["quick witted", "avid play-fighter", "oddly observant","never sits still"]
    good_murder_skills = ["clever", "good fighter", "natural intuition","fast runner"]
    great_murder_skills = ["very clever", "formidable fighter", "keen eye","incredible runner"]
    best_murder_skills = ["incredibly clever", "unusually strong fighter", "unnatural senses","fast as the wind"]


    def get_kill(self, you, cat_to_murder, accomplice, accompliced):
        chance = self.status_chances.get(you.status, 0)
        your_skills = []
        if you.skills.primary:
            your_skills.append(you.skills.primary.skill)
        if you.skills.secondary:
            your_skills.append(you.skills.secondary.skill)
        if any(skill in self.murder_skills for skill in your_skills):
            chance += 5
        if any(skill in self.good_murder_skills for skill in your_skills):
            chance += 10
        if any(skill in self.great_murder_skills for skill in your_skills):
            chance += 15
        if any(skill in self.best_murder_skills for skill in your_skills):
            chance += 20
        
        chance += self.skill_chances.get(cat_to_murder.status, 0)
        
        their_skills = []
        if cat_to_murder.skills.primary:
            their_skills.append(cat_to_murder.skills.primary.skill)
        if cat_to_murder.skills.secondary:
            their_skills.append(cat_to_murder.skills.secondary.skill)
        if any(skill in self.murder_skills for skill in their_skills):
            chance -= 5
        if any(skill in self.good_murder_skills for skill in their_skills):
            chance -= 10
        if any(skill in self.great_murder_skills for skill in their_skills):
            chance -= 15
        if any(skill in self.best_murder_skills for skill in their_skills):
            chance -= 20
        
        if you.is_ill() or you.is_injured():
            chance -= 20
        if cat_to_murder.is_ill() or cat_to_murder.is_injured():
            chance += 20
            
        if accomplice and accompliced:
            chance += 20
        
        return chance
    
    def update_selected_cat(self):
        """Updates the image and information on the currently selected mentor"""
        for ele in self.selected_details:
            self.selected_details[ele].kill()
        self.selected_details = {}
        if self.selected_cat:

            self.selected_details["selected_image"] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((233, 310), (270, 270))),
                pygame.transform.scale(
                    self.selected_cat.sprite,
                    (270, 270)), manager=MANAGER)

            info = self.selected_cat.status + "\n" + \
                   self.selected_cat.genderalign + "\n" + self.selected_cat.personality.trait + "\n"

            if self.selected_cat.moons < 1:
                info += "???"
            else:
                info += self.selected_cat.skills.skill_string(short=True)
            
            self.selected_details["selected_info"] = pygame_gui.elements.UITextBox(info,
                                                                                   scale(pygame.Rect((540, 325),
                                                                                                     (210, 250))),
                                                                                   object_id="#text_box_22_horizcenter_vertcenter_spacing_95",
                                                                                   manager=MANAGER)

            name = str(self.selected_cat.name)  # get name
            if 11 <= len(name):  # check name length
                short_name = str(name)[0:9]
                name = short_name + '...'
            self.selected_details["victim_name"] = pygame_gui.elements.ui_label.UILabel(
                scale(pygame.Rect((260, 230), (220, 60))),
                name,
                object_id="#text_box_34_horizcenter", manager=MANAGER)
            if self.stage == 'choose murder cat':
                if not self.selected_cat.dead and not self.selected_cat.outside:
                    c_text = ""
                    chance = self.get_kill(game.clan.your_cat, self.selected_cat, None, False)
                    if chance < 20:
                        c_text = "very low"
                    elif chance < 30:
                        c_text = "low"
                    elif chance < 40:
                        c_text = "average"
                    elif chance < 70:
                        c_text = "high"
                    else:
                        c_text = "very high"
                    if game.settings['dark mode']:
                        self.selected_details["chance"] = pygame_gui.elements.UITextBox("murder chance: " + c_text,
                                                                                                scale(pygame.Rect((540, 500),
                                                                                                                    (210, 250))),
                                                                                                object_id="#text_box_22_horizcenter_vertcenter_spacing_95_dark",
                                                                                                manager=MANAGER)

                    else:
                        self.selected_details["chance"] = pygame_gui.elements.UITextBox("murder chance: " + c_text,
                                                                                            scale(pygame.Rect((540, 500),
                                                                                                                (210, 250))),
                                                                                            object_id="#text_box_22_horizcenter_vertcenter_spacing_95",
                                                                                            manager=MANAGER)
            else:
                if not self.selected_cat.dead and not self.selected_cat.outside:
                    c_text = ""
                    chance = self.get_accomplice_chance(game.clan.your_cat, self.selected_cat)
                    if game.config["accomplice_chance"] != -1:
                        try:
                            chance = game.config["accomplice_chance"]
                        except:
                            pass
                    if chance < 30:
                        c_text = "very low"
                    elif chance < 40:
                        c_text = "low"
                    elif chance < 50:
                        c_text = "average"
                    elif chance < 70:
                        c_text = "high"
                    else:
                        c_text = "very high"
                    if game.settings['dark mode']:
                        self.selected_details["chance"] = pygame_gui.elements.UITextBox("willingness: " + c_text,
                                                                                                scale(pygame.Rect((540, 500),
                                                                                                                    (210, 250))),
                                                                                                object_id="#text_box_22_horizcenter_vertcenter_spacing_95_dark",
                                                                                                manager=MANAGER)

                    else:
                        self.selected_details["chance"] = pygame_gui.elements.UITextBox("willingness: " + c_text,
                                                                                            scale(pygame.Rect((540, 500),
                                                                                                                (210, 250))),
                                                                                            object_id="#text_box_22_horizcenter_vertcenter_spacing_95",
                                                                                            manager=MANAGER)
                        
    def get_accomplice_chance(self, you, accomplice):
        chance = 10
        if accomplice.relationships[you.ID].platonic_like > 10:
            chance += 10
        if accomplice.relationships[you.ID].dislike < 10:
            chance += 10
        if accomplice.relationships[you.ID].romantic_love > 10:
            chance += 10
        if accomplice.relationships[you.ID].comfortable > 10:
            chance += 10
        if accomplice.relationships[you.ID].trust > 10:
            chance += 10
        if accomplice.relationships[you.ID].admiration > 10:
            chance += 10
        if you.status in ['medicine cat', 'mediator', 'deputy', 'leader']:
            chance += 10
        if accomplice.status in ['medicine cat', 'mediator', 'deputy', 'leader']:
            chance -= 20
        if accomplice.ID in game.clan.your_cat.mate:
            chance += 50
        if game.clan.your_cat.is_related(accomplice, False):
            chance += 30
        return chance
                    
    def update_selected_cat2(self):
        """Updates the image and information on the currently selected mentor"""
        for ele in self.selected_details:
            self.selected_details[ele].kill()
        self.selected_details = {}
        if self.selected_cat:
            self.selected_details["selected_image"] = pygame_gui.elements.UIImage(
                scale(pygame.Rect((440, 300), (300, 300))),
                pygame.transform.scale(
                    self.selected_cat.sprite,
                    (300, 300)), manager=MANAGER)

            info = self.selected_cat.status + "\n" + \
                   self.selected_cat.genderalign + "\n" + self.selected_cat.personality.trait + "\n"
            
            if self.selected_cat.moons < 1:
                info += "???"
            else:
                info += self.selected_cat.skills.skill_string(short=True)
            
            self.selected_details["selected_info"] = pygame_gui.elements.UITextBox(info,
                                                                                   scale(pygame.Rect((540, 325),
                                                                                                     (210, 250))),
                                                                                   object_id="#text_box_22_horizcenter_vertcenter_spacing_95",
                                                                                   manager=MANAGER)

            name = str(self.selected_cat.name)  # get name
            if 11 <= len(name):  # check name length
                short_name = str(name)[0:9]
                name = short_name + '...'
            self.selected_details["mentor_name"] = pygame_gui.elements.ui_label.UILabel(
                scale(pygame.Rect((890, 230), (220, 60))),
                name,
                object_id="#text_box_34_horizcenter", manager=MANAGER)
            

    def update_cat_list(self):
        """Updates the cat sprite buttons. """
        valid_mentors = self.chunks(self.get_valid_cats(), 30)

        # If the number of pages becomes smaller than the number of our current page, set
        #   the current page to the last page
        if self.current_page > len(valid_mentors):
            self.list_page = len(valid_mentors)

        # Handle which next buttons are clickable.
        if len(valid_mentors) <= 1:
            self.previous_page_button.disable()
            self.next_page_button.disable()
        elif self.current_page >= len(valid_mentors):
            self.previous_page_button.enable()
            self.next_page_button.disable()
        elif self.current_page == 1 and len(valid_mentors) > 1:
            self.previous_page_button.disable()
            self.next_page_button.enable()
        else:
            self.previous_page_button.enable()
            self.next_page_button.enable()
        display_cats = []
        if valid_mentors:
            display_cats = valid_mentors[self.current_page - 1]

        # Kill all the currently displayed cats.
        for ele in self.cat_list_buttons:
            self.cat_list_buttons[ele].kill()
        self.cat_list_buttons = {}

        pos_x = 0
        pos_y = 40
        i = 0
        for cat in display_cats:
            self.cat_list_buttons["cat" + str(i)] = UISpriteButton(
                scale(pygame.Rect((200 + pos_x, 730 + pos_y), (100, 100))),
                cat.sprite, cat_object=cat, manager=MANAGER)
            pos_x += 120
            if pos_x >= 1100:
                pos_x = 0
                pos_y += 120
            i += 1
            
    def update_cat_list2(self):
        """Updates the cat sprite buttons. """
        valid_mentors = self.chunks(self.get_valid_cats2(), 30)

        # If the number of pages becomes smaller than the number of our current page, set
        #   the current page to the last page
        if self.current_page > len(valid_mentors):
            self.list_page = len(valid_mentors)

        # Handle which next buttons are clickable.
        if len(valid_mentors) <= 1:
            self.previous_page_button.disable()
            self.next_page_button.disable()
        elif self.current_page >= len(valid_mentors):
            self.previous_page_button.enable()
            self.next_page_button.disable()
        elif self.current_page == 1 and len(valid_mentors) > 1:
            self.previous_page_button.disable()
            self.next_page_button.enable()
        else:
            self.previous_page_button.enable()
            self.next_page_button.enable()
        display_cats = []
        if valid_mentors and len(valid_mentors) > self.current_page - 1:
            display_cats = valid_mentors[self.current_page - 1]

        # Kill all the currently displayed cats.
        for ele in self.cat_list_buttons:
            self.cat_list_buttons[ele].kill()
        self.cat_list_buttons = {}

        pos_x = 0
        pos_y = 40
        i = 0
        for cat in display_cats:
            self.cat_list_buttons["cat" + str(i)] = UISpriteButton(
                scale(pygame.Rect((200 + pos_x, 730 + pos_y), (100, 100))),
                cat.sprite, cat_object=cat, manager=MANAGER)
            pos_x += 120
            if pos_x >= 1100:
                pos_x = 0
                pos_y += 120
            i += 1


    def get_valid_cats(self):
        valid_mentors = []

        for cat in Cat.all_cats_list:
            if not cat.dead and not cat.outside and not cat.ID == game.clan.your_cat.ID and not cat.moons == 0:
                valid_mentors.append(cat)
        
        return valid_mentors

    def get_valid_cats2(self):
        valid_mentors = []

        for cat in Cat.all_cats_list:
            if not cat.dead and not cat.outside and not cat.ID == game.clan.your_cat.ID and not cat.ID == self.cat_to_murder.ID and not cat.moons == 0:
                valid_mentors.append(cat)
        
        return valid_mentors

    def on_use(self):
        # Due to a bug in pygame, any image with buttons over it must be blited
        screen.blit(self.list_frame, (150 / 1600 * screen_x, 720 / 1400 * screen_y))

    def chunks(self, L, n):
        return [L[x: x + n] for x in range(0, len(L), n)]

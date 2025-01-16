import pygame.transform
import pygame_gui.elements
from random import choice, randint
import ujson

from scripts.cat_relations.inheritance import Inheritance
from scripts.cat.history import History
from scripts.event_class import Single_Event
from scripts.events import events_class
from .Screens import Screens

from scripts.utility import get_personality_compatibility, get_text_box_theme, shorten_text_to_fit
from scripts.cat.cats import Cat
from scripts.game_structure import image_cache
from scripts.cat.pelts import Pelt
from scripts.game_structure.windows import GameOver, PickPath, DeathScreen
from scripts.game_structure.game_essentials import game
from scripts.game_structure.windows import RelationshipLog
from scripts.game_structure.propagating_thread import PropagatingThread
from scripts.game_structure.ui_elements import UIImageButton, UITextBoxTweaked, UISpriteButton, UISurfaceImageButton
from ..ui.generate_box import BoxStyles, get_box
from scripts.utility import get_text_box_theme, ui_scale, ui_scale_blit, ui_scale_offset
from scripts.game_structure.screen_settings import MANAGER
from ..ui.generate_button import get_button_dict, ButtonStyles
from ..ui.get_arrow import get_arrow
from ..ui.icon import Icon


class NameKitsScreen(Screens):
    selected_cat = None
    current_page = 1
    list_frame = None
    apprentice_details = {}
    selected_details = {}
    cat_list_buttons = {}

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
        self.selected_details = {}

    def handle_event(self, event):
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element in self.cat_list_buttons.values():
                self.selected_cat = event.ui_element.return_cat_object()
                self.update_selected_cat()
                # self.update_buttons()
            elif event.ui_element == self.confirm_mentor and self.selected_cat:
                if not self.selected_cat.dead:
                    # self.update_selected_cat()
                    self.change_cat(self.selected_cat)
                    if "mentor_name" in self.selected_details:
                        self.selected_details['mentor_name'].kill()
                    name = str(self.selected_cat.name)  # get name
                    if self.selected_cat.name.prefix != "":
                        if 11 <= len(name):  # check name length
                            short_name = str(name)[0:9]
                            name = short_name + '...'
                        self.selected_details["mentor_name"] = pygame_gui.elements.ui_label.UILabel(
                            ui_scale(pygame.Rect((345, 115), (110, 30))),
                            name,
                            object_id="#text_box_34_horizcenter", manager=MANAGER)
                    # self.update_buttons()
            elif event.ui_element == self.back_button:
                for cat in Cat.all_cats_list:
                    if not cat.dead and not cat.outside and cat.age == 'newborn' and cat.ID in game.clan.your_cat.inheritance.get_children() and cat.name.prefix.strip() == "":
                        cat.name.give_prefix(cat.pelt.eye_colour, cat.pelt.colour, game.clan.biome)
                self.change_screen('events screen')
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
        super().screen_switches()
        self.the_cat = game.clan.your_cat
        list_frame = get_box(BoxStyles.ROUNDED_BOX, (650, 194))
        self.list_frame = pygame_gui.elements.UIImage(
            ui_scale(pygame.Rect((75, 360), (650, 194))), list_frame, starting_height=1
        )

        self.heading = pygame_gui.elements.UITextBox("",
                                                     ui_scale(pygame.Rect((150, 25), (500, 40))),
                                                     object_id=get_text_box_theme("#text_box_34_horizcenter"),
                                                     manager=MANAGER)
        
        # Layout Images:
        self.mentor_frame = pygame_gui.elements.UIImage(ui_scale(pygame.Rect((315, 113), (281, 197))),
                                                        pygame.transform.scale(
                                                            image_cache.load_image(
                                                                "resources/images/choosing_cat1_frame_ment.png").convert_alpha(),
                                                            (281, 197)), manager=MANAGER)
        
        self.questionmarks = pygame_gui.elements.UITextBox(
            "???",
            ui_scale(pygame.Rect((110, 192), (100, 25))),
            object_id="#text_box_30_horizcenter",
            manager=MANAGER)
        self.placeholder_kit = pygame_gui.elements.UITextBox(
            "-kit",
            ui_scale(pygame.Rect((160, 192), (100, 25))),
            object_id=get_text_box_theme("#text_box_30_horizcenter"),
            manager=MANAGER)
       
        self.back_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((25, 25), (105, 30))),
            get_arrow(2) + " Back",
            get_button_dict(ButtonStyles.SQUOVAL, (105, 30)),
            object_id="@buttonstyles_squoval",
            manager=MANAGER,
        )
        
        self.confirm_mentor = UISurfaceImageButton(
            ui_scale(pygame.Rect((92, 240), (153, 30))),
            "it's official!",
            get_button_dict(ButtonStyles.SQUOVAL, (153, 30)),
            object_id="@buttonstyles_squoval",
        )
        self.confirm_mentor.disable()

        self.previous_page_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((315, 579), (34, 34))),
            Icon.ARROW_LEFT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            starting_height=0,
        )
        self.next_page_button = UISurfaceImageButton(
            ui_scale(pygame.Rect((451, 579), (34, 34))),
            Icon.ARROW_RIGHT,
            get_button_dict(ButtonStyles.ICON, (34, 34)),
            object_id="@buttonstyles_icon",
            starting_height=0,
        )
        self.selected_cat = None
        self.update_selected_cat()  # Updates the image and details of selected cat
        self.update_cat_list()
        # self.update_buttons()

    def exit_screen(self):

        # self.selected_details["selected_image"].kill()
        # self.selected_details["selected_info"].kill()
        for ele in self.cat_list_buttons:
            self.cat_list_buttons[ele].kill()
        self.cat_list_buttons = {}

        for ele in self.apprentice_details:
            self.apprentice_details[ele].kill()
        self.apprentice_details = {}

        for ele in self.selected_details:
            self.selected_details[ele].kill()
        self.selected_details = {}

        self.heading.kill()
        del self.heading

        self.mentor_frame.kill()
        del self.mentor_frame

        self.back_button.kill()
        del self.back_button
        self.confirm_mentor.kill()
        del self.confirm_mentor

        self.previous_page_button.kill()
        del self.previous_page_button
        self.next_page_button.kill()
        del self.next_page_button

        self.list_frame.kill()
        del self.list_frame


   
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
                    ["newborn"] \
                    and check_cat.df == self.the_cat.df:
                self.previous_cat = check_cat.ID

            elif self.next_cat == 1 and check_cat.ID != self.the_cat.ID and check_cat.dead == self.the_cat.dead and \
                    check_cat.ID != game.clan.instructor.ID and not check_cat.exiled and check_cat.status in \
                    ["newborn"] \
                    and check_cat.df == self.the_cat.df:
                self.next_cat = check_cat.ID

            elif int(self.next_cat) > 1:
                break

        if self.next_cat == 1:
            self.next_cat = 0

    def change_cat(self, new_mentor=None):
        self.selected_cat.name.prefix = self.selected_details["name_entry"].get_text().strip()

    def update_selected_cat(self):
        """Updates the image and information on the currently selected mentor"""
        for ele in self.selected_details:
            self.selected_details[ele].kill()
        self.selected_details = {}

        if self.selected_cat:
            self.confirm_mentor.enable()
            name = str(self.selected_cat.name)  # get name
            if self.selected_cat.name.prefix.strip() != "":
                if 11 <= len(name):  # check name length
                    short_name = str(name)[0:9]
                    name = short_name + '...'
                self.selected_details["mentor_name"] = pygame_gui.elements.ui_label.UILabel(
                    ui_scale(pygame.Rect((345, 115), (110, 30))),
                    name,
                    object_id="#text_box_34_horizcenter", manager=MANAGER)
            self.selected_details["selected_image"] = pygame_gui.elements.UIImage(
                ui_scale(pygame.Rect((325, 150), (150, 150))),
                pygame.transform.scale(
                    self.selected_cat.sprite,
                    (150, 150)), manager=MANAGER)

            info = self.selected_cat.status + "\n" + \
                   self.selected_cat.genderalign + "\n" + self.selected_cat.personality.trait + "\n"

            if self.selected_cat.moons < 1:
                info += "???"
            else:
                info += self.selected_cat.skills.skill_string(short=True)

            self.selected_details["selected_info"] = pygame_gui.elements.UITextBox(
                info,
                ui_scale(pygame.Rect((490, 162), (105, 125))),
                object_id="#text_box_22_horizcenter_vertcenter_spacing_95",
                manager=MANAGER
                )
            self.selected_details["name_entry"] = pygame_gui.elements.UITextEntryLine(
                ui_scale(pygame.Rect((100, 192), (140, 29))),
                manager=MANAGER,
                initial_text=""
                )

            self.selected_details["name_entry"].set_allowed_characters(
                list("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_- "))
            self.selected_details["name_entry"].set_text_length_limit(11)
            self.selected_details["clan"] = pygame_gui.elements.UITextBox(
                "-kit",
                ui_scale(pygame.Rect((160, 192), (100, 25))),
                object_id="#text_box_30_horizcenter",
                manager=MANAGER)
        else:
            self.questionmarks.hide()
        
            self.placeholder_kit.hide()

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
        pos_y = 20
        i = 0
        for cat in display_cats:
            self.cat_list_buttons["cat" + str(i)] = UISpriteButton(
                ui_scale(pygame.Rect((100 + pos_x, 365 + pos_y), (50, 50))),
                cat.sprite, cat_object=cat, manager=MANAGER)
            pos_x += 60
            if pos_x >= 550:
                pos_x = 0
                pos_y += 60
            i += 1

    def get_valid_cats(self):
        valid_mentors = []

        for cat in Cat.all_cats_list:
            if not cat.dead and not cat.outside and cat.age == 'newborn' and cat.ID in game.clan.your_cat.inheritance.get_children():
                valid_mentors.append(cat)
                cat.name.prefix = ""
        
        return valid_mentors

    def on_use(self):
        # Due to a bug in pygame, any image with buttons over it must be blited
        # screen.blit(self.list_frame, (150 / 1600 * screen_x, 720 / 1400 * screen_y))
        super().on_use()

    def chunks(self, L, n):
        return [L[x: x + n] for x in range(0, len(L), n)]
import pygame
import pygame_gui

from scripts.cat.cats import Cat
from scripts.event_class import Single_Event
from scripts.events import events_class
<<<<<<< HEAD
from scripts.utility import get_living_clan_cat_count, get_text_box_theme, scale, shorten_text_to_fit
from scripts.game_structure.game_essentials import game, screen_x, screen_y, MANAGER
from scripts.game_structure.ui_elements import IDImageButton, UIImageButton, UISpriteButton
from scripts.game_structure.windows import GameOver
from scripts.utility import (
    get_living_clan_cat_count,
    get_text_box_theme,
    scale,
    shorten_text_to_fit,
    clan_symbol_sprite,
)
from .Screens import Screens
from ..cat.cats import Cat
from ..game_structure import image_cache
from scripts.event_class import Single_Event
from scripts.game_structure.windows import GameOver, PickPath, DeathScreen, EventLoading
import ujson
import random
from scripts.game_structure.propagating_thread import PropagatingThread
=======
from scripts.game_structure import image_cache
from scripts.game_structure.game_essentials import game, MANAGER
from scripts.game_structure.ui_elements import UIImageButton, UIModifiedScrollingContainer, IDImageButton
from scripts.game_structure.windows import GameOver
from scripts.screens.Screens import Screens
from scripts.utility import scale, clan_symbol_sprite, get_text_box_theme, shorten_text_to_fit, \
    get_living_clan_cat_count
>>>>>>> 2024-09


class EventsScreen(Screens):
    current_display = "all"
    selected_display = "all"

    all_events = ""
    ceremony_events = ""
    birth_death_events = ""
    relation_events = ""
    health_events = ""
    other_clans_events = ""
    misc_events = ""
<<<<<<< HEAD
    display_text = ""
    display_events = ""
    
    def __init__(self, name=None):
        super().__init__(name)
        self.clan_symbol = None
        self.misc_alert = None
        self.other_clans_alert = None
        self.health_alert = None
        self.relation_alert = None
        self.birth_death_alert = None
        self.ceremony_alert = None
        self.misc_events_button = None
        self.other_clans_events_button = None
        self.health_events_button = None
        self.birth_death_events_button = None
        self.ceremonies_events_button = None
        self.all_events_button = None
        self.relationship_events_button = None
        self.events_list_box = None
        self.toggle_borders_button = None
        self.timeskip_button = None
        self.death_button = None
        self.freshkill_pile_button = None
        self.events_frame = None
        self.clan_age = None
        self.season = None
        self.heading = None
        self.display_events_elements = {}
        self.involved_cat_buttons = []
        self.cat_profile_buttons = {}
        self.scroll_height = {}
        self.CEREMONY_TXT = None
        self.start = 0
        self.loading_window = None
        self.done_moon = False
        self.events_thread = None
        self.you = None

        self.faves1 = False
        self.faves2 = False
        self.faves3 = False
=======
    display_text = (
        "<center>See which events are currently happening in the Clan.</center>"
    )
    display_events = []
    tabs = ["all", "ceremony", "birth_death", "relationship", "health", "other_clans", "misc"]

    def __init__(self, name):
        super().__init__(name)

        self.events_thread = None
        self.event_screen_container = None
        self.clan_info = {}
        self.timeskip_button = None

        self.full_event_display_container = None
        self.events_frame = None
        self.event_buttons = {}
        self.alert = {}

        self.event_display = None
        self.event_display_elements = {}
        self.cat_profile_buttons = {}
        self.involved_cat_container = None
        self.involved_cat_buttons = {}
>>>>>>> 2024-09

        # Stores the involved cat button that currently has its cat profile buttons open
        self.open_involved_cat_button = None

        self.first_opened = False

    def handle_event(self, event):
<<<<<<< HEAD
        if game.switches['window_open']:
            return
        elif event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            try:
                if event.ui_element == self.ceremonies_events_button and self.ceremony_alert:
                    self.ceremony_alert.kill()
                elif event.ui_element == self.birth_death_events_button and self.birth_death_alert:
                    self.birth_death_alert.kill()
                elif event.ui_element == self.relationship_events_button and self.relation_alert:
                    self.relation_alert.kill()
                elif event.ui_element == self.health_events_button and self.health_alert:
                    self.health_alert.kill()
                elif event.ui_element == self.other_clans_events_button and self.other_clans_alert:
                    self.other_clans_alert.kill()
                elif event.ui_element == self.misc_events_button and self.misc_alert:
                    self.misc_alert.kill()
            except:
                print("too much button pressing!")
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            if event.ui_element == self.timeskip_button and game.clan.your_cat.dead_for >= 1 and not game.switches['continue_after_death']:
                DeathScreen('events screen')
                return
            elif self.death_button and event.ui_element == self.death_button:
                DeathScreen('events screen')
                return
            if event.ui_element == self.timeskip_button and game.clan.your_cat.moons == 5 and game.clan.your_cat.status == 'kitten' and not game.clan.your_cat.outside and not game.clan.your_cat.dead:
                PickPath('events screen')
            elif event.ui_element == self.you or ("you" in self.display_events_elements and event.ui_element == self.display_events_elements["you"]):
                game.switches['cat'] = game.clan.your_cat.ID
                self.change_screen("profile screen")
            elif event.ui_element == self.timeskip_button:
                # Save the start time, so the loading animation can be
                # set to only show up if timeskip is taking a good amount of time. 
                self.events_thread = self.loading_screen_start_work(events_class.one_moon)
                self.update_favourite_filters()
                self.yourcat_filter.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3.hide()
                self.fav_group_3_selected.hide()
                self.cat_icon.hide()
            
            elif game.clan.game_mode != "classic" and event.ui_element == self.freshkill_pile_button:
                self.change_screen('clearing screen')

            # Change the type of events displayed
            elif event.ui_element == self.all_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "all events"
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()
                # Update Display
                self.update_list_buttons(self.all_events_button)
                self.display_events = self.all_events
                self.update_events_display()
            elif event.ui_element == self.ceremonies_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "ceremony events"
                self.ceremonies_events_button.disable()
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()

                # Update Display
                self.update_list_buttons(
                    self.ceremonies_events_button, self.ceremony_alert
                )
                self.display_events = self.ceremony_events
                self.update_events_display()
            elif event.ui_element == self.birth_death_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "birth death events"
                self.birth_death_events_button.enable()
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()

                # Update Display
                self.update_list_buttons(
                    self.birth_death_events_button, self.birth_death_alert
                )
                self.display_events = self.birth_death_events
                self.update_events_display()
            elif event.ui_element == self.relationship_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "relationship events"
                self.relationship_events_button.enable()
                self.cat_icon.show()
                self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                # Update Display
                self.update_list_buttons(
                    self.relationship_events_button, self.relation_alert
                )
                self.display_events = self.relation_events
                self.update_events_display()
            elif event.ui_element == self.health_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "health events"
                self.health_events_button.disable()
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()

                # Update Display
                self.update_list_buttons(self.health_events_button, self.health_alert)
                self.display_events = self.health_events
                self.update_events_display()
            elif event.ui_element == self.other_clans_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "other clans events"
                self.other_clans_events_button.disable()
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()
                # Update Display
                self.update_list_buttons(
                    self.other_clans_events_button, self.other_clans_alert
                )
                self.display_events = self.other_clans_events
                self.update_events_display()
            elif event.ui_element == self.misc_events_button:
                if self.event_container.vert_scroll_bar:
                    self.scroll_height[self.event_display_type] = (
                        self.event_container.vert_scroll_bar.scroll_position
                        / self.event_container.vert_scroll_bar.scrollable_height
                    )
                self.event_display_type = "misc events"
                self.misc_events_button.disable()
                self.cat_icon.hide()
                self.yourcat_filter.hide()
                self.fav_group_1.hide()
                self.fav_group_2.hide()
                self.fav_group_3.hide()
                self.yourcat_filter_selected.hide()
                self.fav_group_1_selected.hide()
                self.fav_group_2_selected.hide()
                self.fav_group_3_selected.hide()
                # Update Display
                self.update_list_buttons(self.misc_events_button, self.misc_alert)
                self.display_events = self.misc_events
                self.update_events_display()
            elif event.ui_element == self.cat_icon:
                if not self.dropdown_pressed:
                    if game.clan.your_cat:
                        self.yourcat_filter.show()
                    if self.faves1:
                        self.fav_group_1.show()
                    if self.faves2:
                        self.fav_group_2.show()
                    if self.faves3:
                        self.fav_group_3.show()

                    self.yourcat_filter_selected.hide()
                    self.fav_group_1_selected.hide()
                    self.fav_group_2_selected.hide()
                    self.fav_group_3_selected.hide()

                    self.yourcat_pressed = False
                    self.f1_pressed = False
                    self.f2_pressed = False
                    self.f3_pressed = False
                    self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                    self.display_events = self.relation_events
                    self.update_events_display()
                    self.dropdown_pressed = True
                    self.update_favourite_filters()
                else:
                    self.yourcat_filter.hide()
                    self.fav_group_1.hide()
                    self.fav_group_2.hide()
                    self.fav_group_3.hide()
                    self.yourcat_filter_selected.hide()
                    self.fav_group_1_selected.hide()
                    self.fav_group_2_selected.hide()
                    self.fav_group_3_selected.hide()
                    self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                    self.display_events = self.relation_events
                    self.update_events_display()
                    self.dropdown_pressed = False
                    # self.update_favourite_filters()

            elif event.ui_element == self.yourcat_filter_selected:
                self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.yourcat_pressed = False
                self.update_favourite_filters()

            elif event.ui_element == self.yourcat_filter:
                self.relation_events = [x for x in game.cur_events_list if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.yourcat_pressed = True
                self.update_favourite_filters()
            
            elif event.ui_element == self.fav_group_1_selected:
                self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f1_pressed = False
                self.update_favourite_filters()

            elif event.ui_element == self.fav_group_1:
                # turning off the your_cat filter if your cat is in the toggle favourite group to avoid duped events
                if game.clan.your_cat.favourite == 1 and self.yourcat_pressed:
                    self.yourcat_pressed = False
                self.relation_events = [x for x in (game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f1_pressed = True
                self.update_favourite_filters()
                    
            elif event.ui_element == self.fav_group_2_selected:
                self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f2_pressed = False
                self.update_favourite_filters()

            elif event.ui_element == self.fav_group_2:
                 # turning off the your_cat filter if your cat is in the toggle favourite group to avoid duped events
                if game.clan.your_cat.favourite == 2 and self.yourcat_pressed:
                    self.yourcat_pressed = False
                self.relation_events = [x for x in (game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f2_pressed = True
                self.update_favourite_filters()

            elif event.ui_element == self.fav_group_3_selected:
                self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f3_pressed = False
                self.update_favourite_filters()

            elif event.ui_element == self.fav_group_3:
                 # turning off the your_cat filter if your cat is in the toggle favourite group to avoid duped events
                if game.clan.your_cat.favourite == 3 and self.yourcat_pressed:
                    self.yourcat_pressed = False
                self.relation_events = [x for x in (game.cur_events_list) if "relation" in x.types]
                self.display_events = self.relation_events
                self.update_events_display()
                self.f3_pressed = True
                self.update_favourite_filters()
                    
            elif event.ui_element in self.involved_cat_buttons:
                self.make_cat_buttons(event.ui_element)
            elif event.ui_element in self.cat_profile_buttons:
                game.switches["cat"] = event.ui_element.ids
=======
        if game.switches["window_open"]:
            return

        # ON HOVER
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            element = event.ui_element
            if element in self.event_buttons.values():
                for ele in self.event_buttons:
                    if self.event_buttons[ele] == element:
                        x_pos = int(self.alert[ele].get_relative_rect()[0] - 10)
                        y_pos = self.alert[ele].get_relative_rect()[1]
                        self.alert[ele].set_relative_position((x_pos, y_pos))

        # ON UNHOVER
        elif event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            element = event.ui_element
            if element in self.event_buttons.values():
                for ele in self.event_buttons:
                    if self.event_buttons[ele] == element:
                        x_pos = int(self.alert[ele].get_relative_rect()[0] + 10)
                        y_pos = self.alert[ele].get_relative_rect()[1]
                        self.alert[ele].set_relative_position((x_pos, y_pos))

        # ON START BUTTON PRESS
        elif event.type == pygame_gui.UI_BUTTON_START_PRESS:  # this happens on start press to prevent alert movement
            element = event.ui_element
            if element in self.event_buttons.values():
                for ele, val in self.event_buttons.items():
                    if val == element:
                        self.handle_tab_switch(ele)
                        break

        # ON FULL BUTTON PRESS
        elif event.type == pygame_gui.UI_BUTTON_PRESSED:  # everything else on button press to prevent blinking
            element = event.ui_element
            if element == self.timeskip_button:
                self.events_thread = self.loading_screen_start_work(
                    events_class.one_moon
                )
            elif element in self.involved_cat_buttons.values():
                self.make_cat_buttons(element)
            elif element in self.cat_profile_buttons.values():
                self.save_scroll_position()
                game.switches["cat"] = element.ids
>>>>>>> 2024-09
                self.change_screen("profile screen")
            else:
                self.save_scroll_position()
                self.menu_button_pressed(event)

<<<<<<< HEAD
        elif event.type == pygame.KEYDOWN and game.settings["keybinds"]:
            if event.key == pygame.K_RIGHT:
                self.change_screen("camp screen")
            elif event.key == pygame.K_UP:
                if self.event_display_type == "ceremony events":
                    self.event_display_type = "all events"
                    # Update Display
                    self.update_list_buttons(self.all_events_button)
                    self.display_events = self.all_events
                    self.update_events_display()
                elif self.event_display_type == "birth death events":
                    self.event_display_type = "ceremony events"
                    # Update Display
                    self.update_list_buttons(
                        self.ceremonies_events_button, self.ceremony_alert
                    )
                    self.display_events = self.ceremony_events
                    self.update_events_display()
                elif self.event_display_type == "relationship events":
                    self.event_display_type = "birth death events"
                    # Update Display
                    self.update_list_buttons(
                        self.birth_death_events_button, self.birth_death_alert
                    )
                    self.display_events = self.birth_death_events
                    self.update_events_display()
                elif self.event_display_type == "health events":
                    self.event_display_type = "relationship events"
                    # Update Display
                    self.update_list_buttons(
                        self.relationship_events_button, self.relation_alert
                    )
                    self.display_events = self.relation_events
                    self.update_events_display()
                elif self.event_display_type == "other clans events":
                    self.event_display_type = "health events"
                    # Update Display
                    self.update_list_buttons(
                        self.health_events_button, self.health_alert
                    )
                    self.display_events = self.health_events
                    self.update_events_display()
                elif self.event_display_type == "misc events":
                    self.event_display_type = "other clans events"
                    # Update Display
                    self.update_list_buttons(
                        self.other_clans_events_button, self.other_clans_alert
                    )
                    self.display_events = self.other_clans_events
                    self.update_events_display()
            elif event.key == pygame.K_DOWN:
                if self.event_display_type == "all events":
                    self.event_display_type = "ceremony events"
                    # Update Display
                    self.update_list_buttons(
                        self.ceremonies_events_button, self.ceremony_alert
                    )
                    self.display_events = self.ceremony_events
                    self.update_events_display()
                elif self.event_display_type == "ceremony events":
                    self.event_display_type = "birth death events"
                    # Update Display
                    self.update_list_buttons(
                        self.birth_death_events_button, self.birth_death_alert
                    )
                    self.display_events = self.birth_death_events
                    self.update_events_display()
                elif self.event_display_type == "birth death events":
                    self.event_display_type = "relationship events"
                    # Update Display
                    self.update_list_buttons(
                        self.relationship_events_button, self.relation_alert
                    )
                    self.display_events = self.relation_events
                    self.update_events_display()
                elif self.event_display_type == "relationship events":
                    self.event_display_type = "health events"
                    # Update Display
                    self.update_list_buttons(
                        self.health_events_button, self.health_alert
                    )
                    self.display_events = self.health_events
                    self.update_events_display()
                elif self.event_display_type == "health events":
                    self.event_display_type = "other clans events"
                    # Update Display
                    self.update_list_buttons(
                        self.other_clans_events_button, self.other_clans_alert
                    )
                    self.display_events = self.other_clans_events
                    self.update_events_display()
                elif self.event_display_type == "other clans events":
                    self.event_display_type = "misc events"
                    # Update Display
                    self.update_list_buttons(self.misc_events_button, self.misc_alert)
                    self.display_events = self.misc_events
                    self.update_events_display()
            elif event.key == pygame.K_SPACE:
                if game.clan.your_cat.moons == 5 and game.clan.your_cat.status == 'kitten' and not game.clan.your_cat.outside and not game.clan.your_cat.dead:
                    PickPath('events screen')
                elif (game.clan.your_cat.dead_for == 1 or game.clan.your_cat.exiled):
                    DeathScreen('events screen')
                    return
                self.events_thread = self.loading_screen_start_work(events_class.one_moon)
=======
        # KEYBIND CONTROLS
        elif game.settings["keybinds"]:
            # ON PRESSING A KEY
            if event.type == pygame.KEYDOWN:
                # LEFT ARROW
                if event.key == pygame.K_LEFT:
                    self.change_screen("patrol screen")
                # RIGHT ARROW
                elif event.key == pygame.K_RIGHT:
                    self.change_screen("camp screen")
                # DOWN AND UP ARROW
                elif event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    self.handle_tab_select(event.key)
                elif event.key == pygame.K_RETURN:
                    self.handle_tab_switch(self.selected_display)

    def save_scroll_position(self):
        """
        adds current event display vert scroll bar position to game.switches["saved_scroll_positions"] dict
        """
        if self.event_display.vert_scroll_bar:
            game.switches["saved_scroll_positions"][self.current_display] = (
                    self.event_display.vert_scroll_bar.scroll_position
                    / self.event_display.vert_scroll_bar.scrollable_height
            )

    def handle_tab_select(self, event):

        # find next tab based on current tab
        current_index = self.tabs.index(self.selected_display)
        if event == pygame.K_DOWN:
            next_index = current_index + 1
            wrap_index = 0
        else:
            next_index = current_index - 1
            wrap_index = -1

        # unselect the currently selected display
        # unless it matches the current display, we don't want to mess with the state of that button
        if self.current_display != self.selected_display:
            self.event_buttons[self.selected_display].unselect()
            x_pos = int(self.alert[self.selected_display].get_relative_rect()[0] + 10)
            y_pos = self.alert[self.selected_display].get_relative_rect()[1]
            self.alert[self.selected_display].set_relative_position((x_pos, y_pos))

        # find the new selected display
        try:
            self.selected_display = self.tabs[next_index]
        except IndexError:
            self.selected_display = self.tabs[wrap_index]

        # select the new selected display
        # unless it matches the current display, we don't want to mess with the state of that button
        if self.current_display != self.selected_display:
            self.event_buttons[self.selected_display].select()
            x_pos = int(self.alert[self.selected_display].get_relative_rect()[0] - 10)
            y_pos = self.alert[self.selected_display].get_relative_rect()[1]
            self.alert[self.selected_display].set_relative_position((x_pos, y_pos))

    def handle_tab_switch(self, display_type):
        """
        saves current tab scroll position, removes alert, and then switches to the new tab
        """
        self.save_scroll_position()

        self.current_display = display_type
        self.update_list_buttons()

        if display_type == "all":
            self.display_events = self.all_events
        elif display_type == "ceremony":
            self.display_events = self.ceremony_events
        elif display_type == "birth_death":
            self.display_events = self.birth_death_events
        elif display_type == "relationship":
            self.display_events = self.relation_events
        elif display_type == "health":
            self.display_events = self.health_events
        elif display_type == "other_clans":
            self.display_events = self.other_clans_events
        elif display_type == "misc":
            self.display_events = self.misc_events

        self.alert[display_type].hide()

        self.update_events_display()
>>>>>>> 2024-09

    def screen_switches(self):
        # On first open, update display events list
        self.update_display_events_lists()

<<<<<<< HEAD
        self.clan_symbol = pygame_gui.elements.UIImage(
            scale(pygame.Rect((255, 220), (200, 200))),
=======
        self.event_screen_container = pygame_gui.core.UIContainer(
            scale(pygame.Rect((0, 0), (1600, 1400))),
            object_id="#event_screen_container",
            starting_height=1,
            manager=MANAGER
        )

        self.clan_info["symbol"] = pygame_gui.elements.UIImage(
            scale(pygame.Rect((455, 210), (200, 200))),
>>>>>>> 2024-09
            pygame.transform.scale(clan_symbol_sprite(game.clan), (200, 200)),
            object_id=f"clan_symbol",
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER,
        )

<<<<<<< HEAD
        self.heading = pygame_gui.elements.UITextBox("",
                                                     scale(pygame.Rect((600, 220), (400, 80))),
                                                     object_id=get_text_box_theme("#text_box_30_horizcenter"),
                                                     manager=MANAGER)
        self.season = pygame_gui.elements.UITextBox('',
                                                    scale(pygame.Rect((600, 280), (400, 80))),
                                                    object_id=get_text_box_theme("#text_box_30_horizcenter"),
                                                    manager=MANAGER)
        self.clan_age = pygame_gui.elements.UITextBox("",
                                                      scale(pygame.Rect((600, 280), (400, 80))),
                                                      object_id=get_text_box_theme("#text_box_30_horizcenter"),
                                                      manager=MANAGER)
        self.leaf = pygame_gui.elements.UITextBox("leafbare",
                                                      scale(pygame.Rect((500, 340), (600, 80))),
                                                      object_id=get_text_box_theme("#text_box_30_horizcenter"),
                                                      manager=MANAGER)
 
        self.events_frame = pygame_gui.elements.UIImage(scale(pygame.Rect((412, 532), (1068, 740))),
                                                        image_cache.load_image(
                                                            "resources/images/event_page_frame.png").convert_alpha()
                                                        , manager=MANAGER)
        self.events_frame.disable()
        self.dropdown_pressed = False
        self.yourcat_pressed = False
        self.f1_pressed = False
        self.f2_pressed = False
        self.f3_pressed = False
        if not game.clan.your_cat:
            print("Are you playing a normal ClanGen save? Switch to a LifeGen save or create a new cat!")
            print("Choosing random cat to play...")
            game.clan.your_cat = Cat.all_cats[random.choice(game.clan.clan_cats)]
            counter = 0
            while game.clan.your_cat.dead or game.clan.your_cat.outside:
                if counter == 25:
                    break
                game.clan.your_cat = Cat.all_cats[random.choice(game.clan.clan_cats)]
                counter+=1
                
            print("Chose " + str(game.clan.your_cat.name))
        # Set text for clan age
        if game.clan.your_cat.moons == -1:
            self.clan_age.set_text(f'Your age: Unborn')
        elif game.clan.your_cat.moons != 1:
            self.clan_age.set_text(f'Your age: {game.clan.your_cat.moons} moons')
        elif game.clan.your_cat.moons == 1:
            self.clan_age.set_text(f'Your age: {game.clan.your_cat.moons} moon')

=======
        self.clan_info["heading"] = pygame_gui.elements.UITextBox(
            "Timeskip to progress your Clan's life.",
            scale(pygame.Rect((680, 310), (500, -1))),
            object_id=get_text_box_theme("#text_box_30_horizleft_spacing_95"),
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER,
        )

        self.clan_info["season"] = pygame_gui.elements.UITextBox(
            f"Current season: {game.clan.current_season}",
            scale(pygame.Rect((680, 205), (1200, 80))),
            object_id=get_text_box_theme("#text_box_30"),
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER,
        )
        self.clan_info["age"] = pygame_gui.elements.UITextBox(
            "",
            scale(pygame.Rect((680, 245), (1200, 80))),
            object_id=get_text_box_theme("#text_box_30"),
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER,
        )

        # Set text for Clan age
        if game.clan.age == 1:
            self.clan_info["age"].set_text(f"Clan age: {game.clan.age} moon")
        if game.clan.age != 1:
            self.clan_info["age"].set_text(f"Clan age: {game.clan.age} moons")
>>>>>>> 2024-09

        self.timeskip_button = UIImageButton(
            scale(pygame.Rect((620, 436), (360, 60))),
            "",
            object_id="#timeskip_button",
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER,
        )

<<<<<<< HEAD
        self.death_button = UIImageButton(scale(pygame.Rect((1020, 430), (68, 68))), "", object_id="#warrior", tool_tip_text="Revive"
                                             , manager=MANAGER)
        self.death_button.hide()

        if game.switches['continue_after_death']:
            self.death_button.show()

        # Sets up the buttons to switch between the event types.
        self.all_events_button = UIImageButton(
            scale(pygame.Rect((120, 570), (300, 60))),
            "",
            object_id="#all_events_button",
            manager=MANAGER,
        )
        self.ceremonies_events_button = UIImageButton(
            scale(pygame.Rect((120, 672), (300, 60))),
            "",
            object_id="#ceremony_events_button",
            manager=MANAGER,
        )
        self.birth_death_events_button = UIImageButton(
            scale(pygame.Rect((120, 772), (300, 60))),
            "",
            object_id="#birth_death_events_button",
            manager=MANAGER,
        )
        self.relationship_events_button = UIImageButton(
            scale(pygame.Rect((120, 872), (300, 60))),
            "",
            object_id="#relationship_events_button")
        
        self.cat_icon = UIImageButton(
                scale(pygame.Rect((75, 875), (50, 50))),
                "",
                object_id="#faves_dropdown")
    
        self.cat_icon.hide()

        self.yourcat_filter = UIImageButton(
            scale(pygame.Rect((75, 815), (50, 62))),
            "",
            tool_tip_text="Toggle your events",
            object_id="#yourcat_filter")
        
        self.fav_group_1 = UIImageButton(
            scale(pygame.Rect((75, 926), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 1",
            object_id="#fave_filter_1")
        self.fav_group_2 = UIImageButton(
            scale(pygame.Rect((75, 988), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 2",
            object_id="#fave_filter_2")
        self.fav_group_3 = UIImageButton(
            scale(pygame.Rect((75, 1050), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 3",
            object_id="#fave_filter_3")
        
        self.yourcat_filter_selected = UIImageButton(
            scale(pygame.Rect((75, 815), (50, 62))),
            "",
            tool_tip_text="Toggle your events",
            object_id="#yourcat_filter_selected")
        self.fav_group_1_selected = UIImageButton(
            scale(pygame.Rect((75, 926), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 1",
            object_id="#fave_filter_1_selected")
        self.fav_group_2_selected = UIImageButton(
            scale(pygame.Rect((75, 988), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 2",
            object_id="#fave_filter_2_selected")
        self.fav_group_3_selected = UIImageButton(
            scale(pygame.Rect((75, 1050), (50, 62))),
            "",
            tool_tip_text="Toggle events from favourite group 3",
            object_id="#fave_filter_3_selected")
        
        self.yourcat_filter.hide()
        self.fav_group_1.hide()
        self.fav_group_2.hide()
        self.fav_group_3.hide()

        self.yourcat_filter_selected.hide()
        self.fav_group_1_selected.hide()
        self.fav_group_2_selected.hide()
        self.fav_group_3_selected.hide()
        
        self.health_events_button = UIImageButton(
            scale(pygame.Rect((120, 972), (300, 60))),
            "",
            object_id="#health_events_button",
            manager=MANAGER,
        )
        self.other_clans_events_button = UIImageButton(
            scale(pygame.Rect((120, 1072), (300, 60))),
            "",
            object_id="#other_clans_events_button",
            manager=MANAGER,
        )
        self.misc_events_button = UIImageButton(
            scale(pygame.Rect((120, 1172), (300, 60))),
            "",
            object_id="#misc_events_button",
            manager=MANAGER,
        )

        if self.event_display_type == "all events":
            self.all_events_button.disable()
        elif self.event_display_type == "ceremony events":
            self.ceremonies_events_button.disable()
        elif self.event_display_type == "birth death events":
            self.birth_death_events_button.disable()
        elif self.event_display_type == "relationship events":
            self.relationship_events_button.disable()
            self.cat_icon.show()
        elif self.event_display_type == "health events":
            self.health_events_button.disable()
        elif self.event_display_type == "other clans events":
            self.other_clans_events_button.disable()
        elif self.event_display_type == "misc events":
            self.misc_events_button.disable()
=======
        self.full_event_display_container = pygame_gui.core.UIContainer(
            scale(pygame.Rect((90, 532), (1400, 1400))),
            object_id="#event_display_container",
            starting_height=1,
            container=self.event_screen_container,
            manager=MANAGER
        )
        self.events_frame = pygame_gui.elements.UIImage(
            scale(pygame.Rect((322, 0), (1068, 740))),
            image_cache.load_image(
                "resources/images/event_page_frame.png"
            ).convert_alpha(),
            object_id="#events_frame",
            starting_height=2,
            container=self.full_event_display_container,
            manager=MANAGER,
        )

        y_pos = 0
        for event_type in self.tabs:
            self.event_buttons[f"{event_type}"] = UIImageButton(
                scale(pygame.Rect((30, 38 + y_pos), (300, 60))),
                "",
                object_id=f"#{event_type}_events_button",
                starting_height=1,
                container=self.full_event_display_container,
                manager=MANAGER
            )
>>>>>>> 2024-09

            if event_type:
                self.alert[f"{event_type}"] = pygame_gui.elements.UIImage(
                    scale(pygame.Rect((20, 48 + y_pos), (8, 44))),
                    pygame.transform.scale(
                        image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                    ),
                    container=self.full_event_display_container,
                    object_id=f"alert_mark_{event_type}",
                    manager=MANAGER,
                    visible=False
                )

            y_pos += 100

        self.event_buttons[self.current_display].disable()

        self.make_event_scrolling_container()
        self.open_involved_cat_button = None
        self.update_events_display()

        # Draw and disable the correct menu buttons.
        self.set_disabled_menu_buttons(["events_screen"])
        self.update_heading_text(f"{game.clan.name}Clan")
        self.show_menu_buttons()
<<<<<<< HEAD
        self.update_events_display()
        self.check_faves()

    def update_favourite_filters(self):
        """ Updates relations events based on the applied favourite filters. """
        self.relation_events = []
        if self.dropdown_pressed:
            if self.yourcat_pressed:
                for i in (game.other_events_list + game.cur_events_list):
                    for c in game.clan.clan_cats:
                        if Cat.all_cats.get(c).ID == game.clan.your_cat.ID:
                            if str(Cat.all_cats.get(c).name) in i.text and "relation" in i.types:
                                self.relation_events.append(i)
                                break
                self.display_events = self.relation_events
                self.update_events_display()
            if self.f1_pressed:
                for i in (game.other_events_list + game.cur_events_list):
                    for c in game.clan.clan_cats:
                        if Cat.all_cats.get(c).favourite == 1:
                            if str(Cat.all_cats.get(c).name) in i.text and "relation" in i.types:
                                self.relation_events.append(i)
                                break
                self.display_events = self.relation_events
                self.update_events_display()

            if self.f2_pressed:
                for i in (game.other_events_list + game.cur_events_list):
                    for c in game.clan.clan_cats:
                        if Cat.all_cats.get(c).favourite == 2:
                            if str(Cat.all_cats.get(c).name) in i.text and "relation" in i.types:
                                self.relation_events.append(i)
                                break
                self.display_events = self.relation_events
                self.update_events_display()

            if self.f3_pressed:
                for i in (game.other_events_list + game.cur_events_list):
                    for c in game.clan.clan_cats:
                        if Cat.all_cats.get(c).favourite == 3:
                            if str(Cat.all_cats.get(c).name) in i.text and "relation" in i.types:
                                self.relation_events.append(i)
                                break
                self.display_events = self.relation_events
                self.update_events_display()

            # swaps buttons out for "selected" versions when needed
            if self.yourcat_pressed:
                self.yourcat_filter.hide()
                self.yourcat_filter_selected.show()
            else:
                self.yourcat_filter.show()
                self.yourcat_filter_selected.hide()
            if self.f1_pressed:
                self.fav_group_1.hide()
                self.fav_group_1_selected.show()
            else:
                self.fav_group_1.show()
                self.fav_group_1_selected.hide()
            if self.f2_pressed:
                self.fav_group_2.hide()
                self.fav_group_2_selected.show()
            else:
                self.fav_group_2.show()
                self.fav_group_2_selected.hide()
            if self.f3_pressed:
                self.fav_group_3.hide()
                self.fav_group_3_selected.show()
            else:
                self.fav_group_3.show()
                self.fav_group_3_selected.hide()

            # disabling your_cat filter button if theyre already in a current favourite filter
            # and re-enabling them once that filter is turned off
            if self.f1_pressed and game.clan.your_cat.favourite == 1:
                self.yourcat_filter.disable()
            if self.f2_pressed and game.clan.your_cat.favourite == 2:
                self.yourcat_filter.disable()
            if self.f3_pressed and game.clan.your_cat.favourite == 3:
                self.yourcat_filter.disable()

            if not self.f1_pressed and game.clan.your_cat.favourite == 1:
                self.yourcat_filter.enable()
            if not self.f2_pressed and game.clan.your_cat.favourite == 2:
                self.yourcat_filter.enable()
            if not self.f3_pressed and game.clan.your_cat.favourite == 3:
                self.yourcat_filter.enable()


        else:
            self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
        

    def check_faves(self):
        """ Checks if each favourite group is populated and disables the appropriate button if it's not."""
        self.faves1 = False
        self.faves2 = False
        self.faves3 = False
        for c in game.clan.clan_cats:
            cat = Cat.all_cats.get(c)
            if cat.favourite == 1:
                self.faves1 = True
                break
        for c in game.clan.clan_cats:
            cat = Cat.all_cats.get(c)
            if cat.favourite == 2:
                self.faves2 = True
                break
        for c in game.clan.clan_cats:
            cat = Cat.all_cats.get(c)
            if cat.favourite == 3:
                self.faves3 = True
                break

        if not game.clan.your_cat:
            self.yourcat_filter.disable()
        if not self.faves1:
            self.fav_group_1.disable()
        if not self.faves2:
            self.fav_group_2.disable()
        if not self.faves3:
            self.fav_group_3.disable()

    def exit_screen(self):
        self.open_involved_cat_button = None
        self.clan_symbol.kill()
        self.timeskip_button.kill()
        del self.timeskip_button
        if self.death_button:
            self.death_button.kill()
        self.all_events_button.kill()
        del self.all_events_button
        self.ceremonies_events_button.kill()
        del self.ceremonies_events_button
        if self.ceremony_alert:
            self.ceremony_alert.kill()
            del self.ceremony_alert
        self.birth_death_events_button.kill()
        del self.birth_death_events_button
        if self.birth_death_alert:
            self.birth_death_alert.kill()
            del self.birth_death_alert
        self.relationship_events_button.kill()
        del self.relationship_events_button
        if self.relation_alert:
            self.relation_alert.kill()
            del self.relation_alert
        self.health_events_button.kill()
        del self.health_events_button
        if self.health_alert:
            self.health_alert.kill()
            del self.health_alert
        self.other_clans_events_button.kill()
        del self.other_clans_events_button
        if self.other_clans_alert:
            self.other_clans_alert.kill()
            del self.other_clans_alert
        self.misc_events_button.kill()
        del self.misc_events_button
        if self.misc_alert:
            self.misc_alert.kill()
            del self.misc_alert
        self.events_frame.kill()
        del self.events_frame
        self.clan_age.kill()
        del self.clan_age
        self.season.kill()
        del self.season
        self.leaf.kill()
        del self.leaf
        self.heading.kill()
        del self.heading
        self.event_container.kill()
        self.cat_icon.kill()
        del self.cat_icon
        self.yourcat_filter.kill()
        del self.yourcat_filter
        self.fav_group_1.kill()
        del self.fav_group_1
        self.fav_group_2.kill()
        del self.fav_group_2
        self.fav_group_3.kill()
        del self.fav_group_3
        self.yourcat_filter_selected.kill()
        del self.yourcat_filter_selected
        self.fav_group_1_selected.kill()
        del self.fav_group_1_selected
        self.fav_group_2_selected.kill()
        del self.fav_group_2_selected
        self.fav_group_3_selected.kill()
        del self.fav_group_3_selected
        if self.you:
            self.you.kill()
        for ele in self.display_events_elements:
            self.display_events_elements[ele].kill()
        self.display_events_elements = {}

        for ele in self.involved_cat_buttons:
            ele.kill()
        self.involved_cat_buttons = []

        for ele in self.cat_profile_buttons:
            ele.kill()
        self.cat_profile_buttons = []

        self.hide_menu_buttons()

    def on_use(self):

        self.loading_screen_on_use(self.events_thread, self.timeskip_done)

    def timeskip_done(self):
        """Various sorting and other tasks that must be done with the timeskip is over."""

        self.scroll_height = {}
        if get_living_clan_cat_count(Cat) == 0:
            GameOver('events screen')
        
        if self.event_display_type != 'relationship events':
            self.cat_icon.hide()
            self.yourcat_filter.hide()
            self.fav_group_1.hide()
            self.fav_group_2.hide()
            self.fav_group_3.hide()
            self.yourcat_filter_selected.hide()
            self.fav_group_1_selected.hide()
            self.fav_group_2_selected.hide()
            self.fav_group_3_selected.hide()

        self.update_display_events_lists()

        self.event_display_type = "all events"
        self.all_events_button.disable()
        self.all_events = [
            x for x in game.cur_events_list if "interaction" not in x.types
        ]

        self.ceremonies_events_button.enable()
        if self.ceremony_alert:
            self.ceremony_alert.kill()
        self.ceremony_events = [
            x for x in game.cur_events_list if "ceremony" in x.types
        ]
        if self.ceremony_events:
            self.ceremony_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 680), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.birth_death_alert:
            self.birth_death_alert.kill()
        self.birth_death_events_button.enable()
        self.birth_death_events = [
            x for x in game.cur_events_list if "birth_death" in x.types
        ]
        if self.birth_death_events:
            self.birth_death_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 780), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.relation_alert:
            self.relation_alert.kill()
        self.relationship_events_button.enable()
        self.relation_events = [
            x for x in game.cur_events_list if "relation" in x.types
        ]
        if self.relation_events:
            self.relation_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 880), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.health_alert:
            self.health_alert.kill()
        self.health_events_button.enable()
        self.health_events = [x for x in (game.other_events_list + game.cur_events_list) if "health" in x.types]
        if self.health_events:
            self.health_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 980), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.other_clans_alert:
            self.other_clans_alert.kill()
        self.other_clans_events_button.enable()
        self.other_clans_events = [
            x for x in game.cur_events_list if "other_clans" in x.types
        ]
        if self.other_clans_events:
            self.other_clans_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 1080), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.misc_alert:
            self.misc_alert.kill()
        self.misc_events_button.enable()
        if self.misc_events:
            self.misc_alert = pygame_gui.elements.UIImage(
                scale(pygame.Rect((110, 1180), (8, 44))),
                pygame.transform.scale(
                    image_cache.load_image("resources/images/alert_mark.png"), (8, 44)
                ),
                manager=MANAGER,
            )

        if self.event_display_type == "all events":
            # if events list is empty, add a single message the says nothing interesting happened
            if not self.all_events:
                self.all_events.append(
                    Single_Event("Nothing interesting happened this moon.")
                )
            self.display_events = self.all_events
            self.update_list_buttons(self.all_events_button)
        elif self.event_display_type == "ceremony events":
            self.display_events = self.ceremony_events
            self.update_list_buttons(self.ceremonies_events_button)
        elif self.event_display_type == "birth death events":
            self.display_events = self.birth_death_events
            self.update_list_buttons(self.birth_death_events_button)
        elif self.event_display_type == "relationship events":
            self.display_events = self.relation_events
            self.update_list_buttons(self.relationship_events_button)
        elif self.event_display_type == "health events":
            self.display_events = self.health_events
            self.update_list_buttons(self.health_events_button)
        elif self.event_display_type == "other clans events":
            self.display_events = self.other_clans_events
            self.update_list_buttons(self.other_clans_events_button)
        elif self.event_display_type == "misc events":
            self.display_events = self.misc_events
            self.update_list_buttons(self.misc_events_button)

        self.update_events_display()
        self.show_menu_buttons()

    def update_list_buttons(self, current_list, current_alert=None):
        """handles the disabling and enabling of the list buttons"""

        # enable all the buttons
        self.all_events_button.enable()
        self.ceremonies_events_button.enable()
        self.birth_death_events_button.enable()
        self.relationship_events_button.enable()
        self.health_events_button.enable()
        self.other_clans_events_button.enable()
        self.misc_events_button.enable()

        # disable the current button
        current_list.disable()
        if current_alert:
            current_alert.kill()

    def update_events_display(self):
        
        self.leaf.set_text(f'Season: {game.clan.current_season} - Clan Age: {game.clan.age}')
        self.heading.set_text(str(game.clan.your_cat.name))
        if game.clan.your_cat.moons == -1:
            self.clan_age.set_text(f'Your age: Unborn')
        elif game.clan.your_cat.moons != 1:
            self.clan_age.set_text(f'Your age: {game.clan.your_cat.moons} moons')
        elif game.clan.your_cat.moons == 1:
            self.clan_age.set_text(f'Your age: {game.clan.your_cat.moons} moon')

        for ele in self.display_events_elements:
            self.display_events_elements[ele].kill()
        if self.you:
            self.you.kill()
    
        for ele in self.involved_cat_buttons:
            ele.kill()
        self.involved_cat_buttons = []

        for ele in self.cat_profile_buttons:
            ele.kill()
        self.cat_profile_buttons = []

        if game.switches['continue_after_death'] and game.clan.your_cat.moons >= 0:
            self.death_button.show()
        else:
            self.death_button.hide()

        # In order to set-set the scroll-bar postion, we have to remake the scrolling container
        self.event_container.kill()
        self.make_events_container()

        # Stop if Clan is new, so that events from previously loaded Clan don't show up
        if game.clan.age == 0:
            return

        # Make display, with buttons and all that.
        box_length = self.event_container.get_relative_rect()[2]
        i = 0
        y = 0
        padding = 70 / 1400 * screen_y
        button_size = 68 / 1600 * screen_x
        button_padding = 80 / 1400 * screen_x
        for ev in self.display_events:
            if isinstance(ev.text, str):  # Check to make sure text is a string.
                self.display_events_elements["event" + str(i)] = (
                    pygame_gui.elements.UITextBox(
                        ev.text,
                        pygame.Rect((0, y), (box_length - 20, -1)),
                        object_id=get_text_box_theme("#text_box_30_horizleft"),
                        container=self.event_container,
                        starting_height=2,
                        manager=MANAGER,
                    )
                )
                self.display_events_elements["event" + str(i)].disable()
                # Find the next y-height by finding the height of the text box, and adding 35 for the cats button

                if i % 2 == 0:
                    if game.settings["dark mode"]:
                        self.display_events_elements["shading" + str(i)] = (
                            pygame_gui.elements.UIImage(
                                pygame.Rect(
                                    (0, y),
                                    (
                                        box_length + 100,
                                        self.display_events_elements[
                                            "event" + str(i)
                                        ].get_relative_rect()[3]
                                        + padding,
                                    ),
                                ),
                                image_cache.load_image(
                                    "resources/images/shading_dark.png"
                                ),
                                container=self.event_container,
                                manager=MANAGER,
                            )
                        )
                    else:
                        self.display_events_elements["shading" + str(i)] = (
                            pygame_gui.elements.UIImage(
                                pygame.Rect(
                                    (0, y),
                                    (
                                        box_length + 100,
                                        self.display_events_elements[
                                            "event" + str(i)
                                        ].get_relative_rect()[3]
                                        + padding,
                                    ),
                                ),
                                image_cache.load_image("resources/images/shading.png"),
                                container=self.event_container,
                                manager=MANAGER,
                            )
                        )

                    self.display_events_elements["shading" + str(i)].disable()

                y += self.display_events_elements["event" + str(i)].get_relative_rect()[
                    3
                ]

                self.involved_cat_buttons.append(
                    IDImageButton(
                        pygame.Rect(
                            (
                                self.event_container.get_relative_rect()[2]
                                - button_padding,
                                y - 10,
                            ),
                            (button_size, button_size),
                        ),
                        ids=ev.cats_involved,
                        container=self.event_container,
                        layer_starting_height=2,
                        object_id="#events_cat_button",
                        manager=MANAGER,
                    )
                )

                y += 68 / 1600 * screen_y
                i += 1
            else:
                print("Incorrectly formatted event:", ev.text, type(ev))

        # Set scrolling container length
        # This is a hack-y solution, but it was the easiest way to have the shading go all the way across the box
        self.event_container.set_scrollable_area_dimensions((box_length, y + 15))

        if self.event_container.vert_scroll_bar:
            for ele in self.involved_cat_buttons:
                ele.set_relative_position(
                    (ele.get_relative_rect()[0] - 20, ele.get_relative_rect()[1])
                )

        if self.event_container.horiz_scroll_bar:
            self.event_container.set_dimensions(
                (box_length, self.events_container_y + 20)
            )
            self.event_container.horiz_scroll_bar.hide()
        else:
            self.event_container.set_dimensions((box_length, self.events_container_y))
        # Set the scroll bar to the last position it was at
        if self.scroll_height.get(self.event_display_type):
            self.event_container.vert_scroll_bar.set_scroll_from_start_percentage(
                self.scroll_height[self.event_display_type]
            )
        if self.you:
            self.you.kill()
        if game.clan.your_cat.moons != -1:
            self.you = UISpriteButton(scale(pygame.Rect((1050, 200), (200, 200))),
                                game.clan.your_cat.sprite,
                                cat_object=game.clan.your_cat,
                                manager=MANAGER)
            
=======

    def make_event_scrolling_container(self):
        """
        kills and recreates the self.event_display container
        """
        if self.event_display:
            self.event_display.kill()

        self.event_display = UIModifiedScrollingContainer(
            scale(pygame.Rect((432, 552), (1080, 700))),
            object_id="#event_display",
            starting_height=3,
            manager=MANAGER,
            allow_scroll_y=True
        )

>>>>>>> 2024-09
    def make_cat_buttons(self, button_pressed):
        """Makes the buttons that take you to the profile."""

        # Check if the button you pressed doesn't have its cat profile buttons currently displayed.
        # if it does, clear the cat profile buttons
        if self.open_involved_cat_button == button_pressed:
            self.open_involved_cat_button = None
            for ele in self.cat_profile_buttons:
                self.cat_profile_buttons[ele].kill()
            self.cat_profile_buttons = {}
            return

        # If it doesn't have its buttons displayed, set the current open involved_cat_button to the pressed button,
        # clear all other buttons, and open the cat profile buttons.
        self.open_involved_cat_button = button_pressed
        if self.involved_cat_container:
            self.involved_cat_container.kill()

        x_pos = 655
        if game.settings["fullscreen"]:
            y_pos = button_pressed.get_relative_rect()[1]
        else:
            y_pos = button_pressed.get_relative_rect()[1] * 2

        self.involved_cat_container = UIModifiedScrollingContainer(
            scale(pygame.Rect((20, y_pos), (890, 108))),
            starting_height=3,
            object_id="#involved_cat_container",
            container=self.event_display,
            manager=MANAGER,
            allow_scroll_x=True
        )

        if game.settings["fullscreen"]:
            fullscreen_modifier = 0
        else:
            fullscreen_modifier = 1

        for i, cat_id in enumerate(button_pressed.ids):
            cat_ob = Cat.fetch_cat(cat_id)
            if cat_ob:
                # Shorten name if needed
                name = str(cat_ob.name)
                short_name = shorten_text_to_fit(name, 195, 26)

                self.cat_profile_buttons[f"profile_button{i}"] = IDImageButton(
                    scale(pygame.Rect((x_pos, 4), (232, 60))),
                    text=short_name,
                    ids=cat_id,
                    container=self.involved_cat_container,
                    object_id="#events_cat_profile_button",
                    layer_starting_height=1,
                    manager=MANAGER,
                )

                x_pos += -255
                if x_pos < 0:
                    x_pos += 54 * fullscreen_modifier
                    if i > 2:
                        x_pos += 73 * fullscreen_modifier

        self.involved_cat_container.set_view_container_dimensions(
            (self.involved_cat_container.get_relative_rect()[2], self.event_display.get_relative_rect()[3]))

    def exit_screen(self):
        self.event_display.kill()  # event display isn't put in the screen container due to lag issues
        self.event_screen_container.kill()

    def update_display_events_lists(self):
        """
        Categorize events from game.cur_events_list into display categories for screen
        """
        
        self.all_events = [x for x in game.cur_events_list if "interaction" not in x.types]
        self.ceremony_events = [x for x in (game.other_events_list + game.cur_events_list) if "ceremony" in x.types]
        self.birth_death_events = [x for x in (game.other_events_list + game.cur_events_list) if "birth_death" in x.types]
        self.relation_events = [x for x in (game.other_events_list + game.cur_events_list) if "relation" in x.types]
        self.health_events = [x for x in (game.other_events_list + game.cur_events_list) if "health" in x.types]
        self.other_clans_events = [x for x in (game.other_events_list + game.cur_events_list) if "other_clans" in x.types]
        self.misc_events = [x for x in (game.other_events_list + game.cur_events_list) if "misc" in x.types]

        if self.event_display_type == "all events":
            self.display_events = self.all_events
        elif self.event_display_type == "ceremony events":
            self.display_events = self.ceremony_events
        elif self.event_display_type == "birth death events":
            self.display_events = self.birth_death_events
        elif self.event_display_type == "relationship events":
            self.display_events = self.relation_events
        elif self.event_display_type == "health events":
            self.display_events = self.health_events
        elif self.event_display_type == "other clans events":
            self.display_events = self.other_clans_events
        elif self.event_display_type == "misc events":
            self.display_events = self.misc_events

<<<<<<< HEAD
=======
        self.all_events = [
            x for x in game.cur_events_list if "interaction" not in x.types
        ]
        self.ceremony_events = [
            x for x in game.cur_events_list if "ceremony" in x.types
        ]
        self.birth_death_events = [
            x for x in game.cur_events_list if "birth_death" in x.types
        ]
        self.relation_events = [
            x for x in game.cur_events_list if "relation" in x.types
        ]
        self.health_events = [
            x for x in game.cur_events_list if "health" in x.types
        ]
        self.other_clans_events = [
            x for x in game.cur_events_list if "other_clans" in x.types
        ]
        self.misc_events = [
            x for x in game.cur_events_list if "misc" in x.types
        ]
>>>>>>> 2024-09

    def update_events_display(self):
        """
        Kills and recreates the event display, updates the clan info, sets the event display scroll position if it was
        previously saved
        """

        # UPDATE CLAN INFO
        self.clan_info["season"].set_text(f"Current season: {game.clan.current_season}")
        if game.clan.age == 1:
            self.clan_info["age"].set_text(f"Clan age: {game.clan.age} moon")
        else:
            self.clan_info["age"].set_text(f"Clan age: {game.clan.age} moons")

        self.make_event_scrolling_container()

        for ele in self.event_display_elements:
            self.event_display_elements[ele].kill()
        self.event_display_elements = {}

        for ele in self.cat_profile_buttons:
            self.cat_profile_buttons[ele].kill()
        self.cat_profile_buttons = {}

        for ele in self.involved_cat_buttons:
            self.involved_cat_buttons[ele].kill()
        self.involved_cat_buttons = {}

        # Stop if Clan is new, so that events from previously loaded Clan don't show up
        if game.clan.age == 0:
            return

        y_pos = 0

        for i, event_object in enumerate(self.display_events):
            # checking that text is a string
            if not isinstance(event_object.text, str):
                print(f"Incorrectly Formatted Event: {event_object.text}, {type(event_object)}")
                continue

            # TEXT BOX
            self.event_display_elements[f"event{i}"] = pygame_gui.elements.UITextBox(
                event_object.text,
                scale(pygame.Rect((0, y_pos), (1018, -1))),
                object_id=get_text_box_theme("#text_box_30_horizleft"),
                starting_height=2,
                container=self.event_display,
                manager=MANAGER
            )

            if game.settings["fullscreen"]:
                text_box_len = self.event_display_elements[f"event{i}"].get_relative_rect()[3]
            else:
                text_box_len = self.event_display_elements[f"event{i}"].get_relative_rect()[3] * 2

            # SHADING
            if i % 2 == 0:
                image_path = "resources/images/shading"
                if game.settings["dark mode"]:
                    image_path += "_dark.png"
                else:
                    image_path += ".png"

                if event_object.cats_involved:
                    y_len = text_box_len + 125
                else:
                    y_len = text_box_len + 45

                self.event_display_elements[f"shading{i}"] = pygame_gui.elements.UIImage(
                    scale(pygame.Rect((0, y_pos), (1028, y_len))),
                    image_cache.load_image(image_path),
                    starting_height=1,
                    object_id=f"shading{i}",
                    container=self.event_display,
                    manager=MANAGER
                )
                self.event_display_elements[f"shading{i}"].disable()

            if event_object.cats_involved:
                # INVOLVED CAT BUTTON
                y_pos += text_box_len + 15

                self.involved_cat_buttons[f"cat_button{i}"] = IDImageButton(
                    scale(pygame.Rect((928, y_pos), (68, 68))),
                    ids=event_object.cats_involved,
                    layer_starting_height=3,
                    object_id="#events_cat_button",
                    container=self.event_display,
                    manager=MANAGER
                )

                y_pos += 110
            else:
                y_pos += text_box_len + 45

        # this HAS TO UPDATE before saved scroll position can be set
        self.event_display.scrollable_container.update(1)

        # don't ask me why we have to redefine these dimensions, we just do
        # otherwise the scroll position save will break
        self.event_display.set_dimensions(
            (self.event_display.get_relative_rect()[2], self.event_display.get_relative_rect()[3]))

        # set saved scroll position
        if game.switches["saved_scroll_positions"].get(self.current_display):
            self.event_display.vert_scroll_bar.set_scroll_from_start_percentage(
                game.switches["saved_scroll_positions"][self.current_display]
            )

    def update_list_buttons(self):
        """
        re-enable all event tab buttons, then disable the currently selected tab
        """
        for ele in self.event_buttons:
            self.event_buttons[ele].enable()

        self.event_buttons[self.current_display].disable()

    def on_use(self):
        self.loading_screen_on_use(self.events_thread, self.timeskip_done)
        pass

    def timeskip_done(self):
        """Various sorting and other tasks that must be done with the timeskip is over."""

        game.switches["saved_scroll_positions"] = {}

        if get_living_clan_cat_count(Cat) == 0:
            GameOver("events screen")

        self.update_display_events_lists()

        self.current_display = "all"
        self.event_buttons["all"].disable()

        for tab in self.event_buttons:
            if tab != "all":
                self.event_buttons[tab].enable()

        if not self.all_events:
            self.all_events.append(
                Single_Event("Nothing interesting happened this moon.")
            )

        self.display_events = self.all_events

        if self.ceremony_events:
            self.alert["ceremony"].show()
        else:
            self.alert["ceremony"].hide()

        if self.birth_death_events:
            self.alert["birth_death"].show()
        else:
            self.alert["birth_death"].hide()

        if self.relation_events:
            self.alert["relationship"].show()
        else:
            self.alert["relationship"].hide()

        if self.health_events:
            self.alert["health"].show()
        else:
            self.alert["health"].hide()

        if self.other_clans_events:
            self.alert["other_clans"].show()
        else:
            self.alert["other_clans"].hide()

        if self.misc_events:
            self.alert["misc"].show()
        else:
            self.alert["misc"].hide()

        self.update_events_display()

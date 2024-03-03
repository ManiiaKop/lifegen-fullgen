# pylint: disable=line-too-long
"""

This file contains:
  The start screen,
  The switch clan screen,
  The settings screen,
  And the statistics screen.



"""  # pylint: enable=line-too-long

import logging
import os
import platform
import subprocess
import traceback
import logging
import random
from html import escape

import pygame
import pygame_gui
import ujson
from requests.exceptions import RequestException, Timeout

from scripts.cat.cats import Cat
from scripts.clan import Clan
from scripts.game_structure import image_cache
from scripts.game_structure.discord_rpc import _DiscordRPC
from scripts.game_structure.game_essentials import game, screen, screen_x, screen_y, MANAGER
from scripts.game_structure.image_button import UIImageButton
from scripts.game_structure.windows import DeleteCheck, UpdateAvailablePopup, ChangelogPopup, SaveError
from scripts.utility import get_text_box_theme, scale, quit  # pylint: disable=redefined-builtin
from scripts.cat.history import History
from .Screens import Screens
from ..housekeeping.datadir import get_data_dir, get_cache_dir
from ..housekeeping.update import has_update, UpdateChannel, get_latest_version_number
from ..housekeeping.version import get_version_info

logger = logging.getLogger(__name__)
has_checked_for_update = False
update_available = False

class AchievementScreen(Screens):
    """
    TODO: DOCS
    """

    def screen_switches(self):
        """
        TODO: DOCS
        """
        
        self.set_disabled_menu_buttons(["stats"])
        self.show_menu_buttons()
        self.update_heading_text(f'{game.clan.name}Clan')
        a_txt = ""
        with open('resources/dicts/achievements.json', 'r', encoding='utf-8') as f:
            a_txt = ujson.load(f)

        self.check_achivements()
        
        
        # Determine stats
        stats_text = f"Achievements:"
        for i in game.clan.achievements:
            stats_text += "\n" + a_txt[i]
            
            

        self.stats_box = pygame_gui.elements.UITextBox(
            stats_text,
            scale(pygame.Rect((200, 300), (1200, 1000))),
            manager=MANAGER,
            object_id=get_text_box_theme("#text_box_30_horizcenter"))

    def check_achivements(self):
        you = game.clan.your_cat
        achievements = set()
        murder_history = History.get_murders(you)
        clan_cats = game.clan.clan_cats
        if murder_history:
            if 'is_murderer' in murder_history:
                num_victims = len(murder_history["is_murderer"])
                if num_victims >= 0:
                    achievements.add("1")
                if num_victims >= 5:
                    achievements.add("2")
                if num_victims >= 20:
                    achievements.add("3")
                if num_victims >= 50:
                    achievements.add("4")
        for cat in clan_cats:
            if Cat.all_cats.get(cat).pelt.tortiebase and Cat.all_cats.get(cat).gender == 'male':
                achievements.add("5")
            if Cat.all_cats.get(cat).status == 'apprentice' and Cat.all_cats.get(cat).name.prefix == "Pea" and Cat.all_cats.get(cat).pelt.white_colours:
                achievements.add("33")
        
        if you.joined_df:
            achievements.add("7")
        
        if len(you.former_apprentices) >= 1:
            achievements.add("8")
        if len(you.former_apprentices) >= 5:
            achievements.add("9")
        
        if you.inheritance.get_children():
            achievements.add("10")
        for i in you.relationships.keys():
            if you.relationships.get(i).dislike >= 60:
                achievements.add("11")
            if you.relationships.get(i).romantic_love >= 60:
                achievements.add('12')
            
        if len(you.mate) >= 5:
            achievements.add('13')
        if you.status == 'warrior':
            achievements.add('14')
        elif you.status == 'medicine cat':
            achievements.add('15')
        elif you.status == 'mediator':
            achievements.add('16')
        elif you.status == 'deputy':
            achievements.add('17')
        elif you.status == 'leader':
            achievements.add('18')
        elif you.status == 'elder':
            achievements.add('19')
        
        if you.moons >= 200:
            achievements.add('20')
        if you.exiled:
            achievements.add('21')
        elif you.outside:
            achievements.add('22')
        
        if len(clan_cats) == 1 and not you.dead:
            achievements.add('23')
        
        for i in game.clan.achievements:
            achievements.add(i)
        
        game.clan.achievements = list(achievements)

    def exit_screen(self):
        """
        TODO: DOCS
        """
        self.stats_box.kill()
        del self.stats_box

    def handle_event(self, event):
        """
        TODO: DOCS
        """
        if event.type == pygame_gui.UI_BUTTON_START_PRESS:
            self.menu_button_pressed(event)

    def on_use(self):
        """
        TODO: DOCS
        """

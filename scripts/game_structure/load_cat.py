import logging
import os
from math import floor
from random import choice, randint

import ujson

from scripts.cat.cats import Cat, BACKSTORIES
from ..cat.personality import Personality
from scripts.cat.pelts import Pelt
from scripts.cat_relations.inheritance import Inheritance
from scripts.housekeeping.version import SAVE_VERSION_NUMBER
from .game_essentials import game
from ..cat.skills import CatSkills
from ..housekeeping.datadir import get_save_dir

logger = logging.getLogger(__name__)


def load_cats():
    try:
        json_load()
    except FileNotFoundError as e:
        game.switches["error_message"] = "Can't find clan_cats.json!"
        game.switches["traceback"] = e
        raise


def json_load():
    all_cats = []
    cat_data = None
    clanname = game.switches["clan_list"][0]
    clan_cats_json_path = f"{get_save_dir()}/{clanname}/clan_cats.json"
    with open(f"resources/dicts/conversion_dict.json", "r") as read_file:
        convert = ujson.loads(read_file.read())
    try:
        with open(clan_cats_json_path, "r") as read_file:
            cat_data = ujson.loads(read_file.read())
    except PermissionError as e:
        game.switches["error_message"] = f"Can\t open {clan_cats_json_path}!"
        game.switches["traceback"] = e
        raise
    except ujson.JSONDecodeError as e:
        game.switches["error_message"] = f"{clan_cats_json_path} is malformed!"
        game.switches["traceback"] = e
        raise

    # create new cat objects
    for i, cat in enumerate(cat_data):
        try:
            if "shunned" not in cat:
                cat["shunned"] = False
            if "revealed" in cat:
                cat["forgiven"] = cat["revealed"]
            if cat["favourite"] is False:
                cat["favourite"] = 0
            elif cat["favourite"] is True:
                cat["favourite"] = 1

            if "accessories" not in cat:
                cat["accessories"] = []
            if "inventory" not in cat:
                cat["inventory"] = []
            if cat["accessory"] is not None:
                cat["accessories"].append(cat["accessory"])
                cat["inventory"].append(cat["accessory"])
                cat["accessory"] = None
            try:
                new_cat = Cat(ID=cat["ID"],
                        prefix=cat["name_prefix"],
                        suffix=cat["name_suffix"],
                        specsuffix_hidden=(cat["specsuffix_hidden"] if 'specsuffix_hidden' in cat else False),
                        gender=cat["gender"],
                        status=cat["status"],
                        parent1=cat["parent1"],
                        parent2=cat["parent2"],
                        moons=cat["moons"],
                        genotype=cat["genotype"],
                        white_patterns=cat["white_pattern"],
                        chim_white=cat["chim_white"] if 'chim_white' in cat else None,
                        loading_cat=True)
            except:
                new_cat = Cat(ID=cat["ID"],
                        prefix=cat["name_prefix"],
                        suffix=cat["name_suffix"],
                        specsuffix_hidden=(cat["specsuffix_hidden"] if 'specsuffix_hidden' in cat else False),
                        gender=cat["gender"],
                        status=cat["status"],
                        parent1=cat["parent1"],
                        parent2=cat["parent2"],
                        moons=cat["moons"],
                        loading_cat=True)
            new_cat.pelt = Pelt(
                new_cat.genotype,
                new_cat.phenotype,
                tint=cat.get('tint', 'none'),
                white_patches_tint=cat.get('white_tint', 'none'),
                paralyzed=cat["paralyzed"],
                kitten_sprite=(
                    cat["sprite_kitten"]
                    if "sprite_kitten" in cat
                    else cat["spirit_kitten"]
                ),
                adol_sprite=(
                    cat["sprite_adolescent"]
                    if "sprite_adolescent" in cat
                    else cat["spirit_adolescent"]
                ),
                adult_sprite=(
                    cat["sprite_adult"]
                    if "sprite_adult" in cat
                    else cat["spirit_adult"]
                ),
                senior_sprite=(
                    cat["sprite_senior"]
                    if "sprite_senior" in cat
                    else cat["spirit_elder"]
                ),
                para_adult_sprite=(
                    cat["sprite_para_adult"] if "sprite_para_adult" in cat else None
                ),
                reverse=cat["reverse"],
                scars=cat["scars"] if "scars" in cat else [],
                accessory=cat["accessory"],
                opacity=cat["opacity"] if "opacity" in cat else 100,
                accessories=cat["accessories"] if "accessories" in cat else [],
                inventory = cat["inventory"] if "inventory" in cat else []
            )

            # Runs a bunch of apperence-related convertion of old stuff.
            new_cat.pelt.check_and_convert(convert)

            # converting old specialty saves into new scar parameter
            if "specialty" in cat or "specialty2" in cat:
                if cat["specialty"] is not None:
                    new_cat.pelt.scars.append(cat["specialty"])
                if cat["specialty2"] is not None:
                    new_cat.pelt.scars.append(cat["specialty2"])

            new_cat.adoptive_parents = (
                cat["adoptive_parents"] if "adoptive_parents" in cat else []
            )

            new_cat.genderalign = cat["gender_align"]
            # new_cat.pronouns = cat["pronouns"]
            new_cat.pronouns = (
                cat["pronouns"]
                if "pronouns" in cat
                else [new_cat.default_pronouns[0].copy()]
            )
            new_cat.backstory = cat["backstory"] if "backstory" in cat else None
            if new_cat.backstory in BACKSTORIES["conversion"]:
                new_cat.backstory = BACKSTORIES["conversion"][new_cat.backstory]
            new_cat.birth_cooldown = (
                cat["birth_cooldown"] if "birth_cooldown" in cat else 0
            )
            new_cat.moons = cat["moons"]

            if "facets" in cat:
                facets = [int(i) for i in cat["facets"].split(",")]
                new_cat.personality = Personality(
                    trait=cat["trait"],
                    kit_trait=new_cat.age in ["newborn", "kitten"],
                    lawful=facets[0],
                    social=facets[1],
                    aggress=facets[2],
                    stable=facets[3],
                )
            else:
                new_cat.personality = Personality(
                    trait=cat["trait"], kit_trait=new_cat.age in ["newborn", "kitten"]
                )

            new_cat.mentor = cat["mentor"]
            new_cat.former_mentor = (
                cat["former_mentor"] if "former_mentor" in cat else []
            )
            new_cat.patrol_with_mentor = (
                cat["patrol_with_mentor"] if "patrol_with_mentor" in cat else 0
            )
            new_cat.no_kits = cat["no_kits"] if "no_kits" in cat else False
            new_cat.no_mates = cat["no_mates"] if "no_mates" in cat else False
            new_cat.no_retire = cat["no_retire"] if "no_retire" in cat else False
            new_cat.no_faith = cat["no_faith"] if "no_faith" in cat else False
            new_cat.lock_faith = cat["lock_faith"] if "lock_faith" in cat else "flexible"
            new_cat.exiled = cat["exiled"]
            new_cat.shunned = cat["shunned"]
            new_cat.driven_out = cat["driven_out"] if "driven_out" in cat else False

            if "skill_dict" in cat:
                new_cat.skills = CatSkills(cat["skill_dict"])
            elif "skill" in cat:
                if new_cat.backstory is None:
                    if "skill" == "formerly a loner":
                        backstory = choice(["loner1", "loner2", "rogue1", "rogue2"])
                        new_cat.backstory = backstory
                    elif "skill" == "formerly a kittypet":
                        backstory = choice(["kittypet1", "kittypet2"])
                        new_cat.backstory = backstory
                    else:
                        new_cat.backstory = "clanborn"
                new_cat.skills = CatSkills.get_skills_from_old(
                    cat["skill"], new_cat.status, new_cat.moons
                )

            new_cat.mate = cat["mate"] if type(cat["mate"]) is list else [cat["mate"]]
            if None in new_cat.mate:
                new_cat.mate = [i for i in new_cat.mate if i is not None]
            new_cat.previous_mates = (
                cat["previous_mates"] if "previous_mates" in cat else []
            )
            new_cat.dead = cat["dead"]
            new_cat.dead_for = cat["dead_moons"]
            new_cat.experience = cat["experience"]
            new_cat.apprentice = cat["current_apprentice"]
            new_cat.former_apprentices = cat["former_apprentices"]
            new_cat.df = cat["df"] if "df" in cat else False
            new_cat.shunned = cat["shunned"] if "shunned" in cat else False
            new_cat.outside = cat["outside"] if "outside" in cat else False
            new_cat.faded_offspring = (
                cat["faded_offspring"] if "faded_offspring" in cat else []
            )
            new_cat.prevent_fading = (
                cat["prevent_fading"] if "prevent_fading" in cat else False
            )
            new_cat.favourite = cat["favourite"] if "favourite" in cat else False
            new_cat.w_done = cat["w_done"] if "w_done" in cat else False
            new_cat.talked_to = cat["talked_to"] if "talked_to" in cat else False
            new_cat.insulted = cat["insulted"] if "insulted" in cat else False
            new_cat.flirted = cat['flirted'] if "flirted" in cat else False
            new_cat.backstory_str = cat["backstory_str"] if "backstory_str" in cat else ""
            new_cat.joined_df = cat["joined_df"] if "joined_df" in cat else False
            new_cat.forgiven = cat["forgiven"] if "forgiven" in cat else 0
            new_cat.revives = cat["revives"] if "revives" in cat else 0
            new_cat.courage = cat["courage"] if "courage" in cat else 0
            new_cat.intelligence = cat["intelligence"] if "intelligence" in cat else 0
            new_cat.empathy = cat["empathy"] if "empathy" in cat else 0
            new_cat.compassion = cat["compassion"] if "compassion" in cat else 0
            new_cat.did_activity = cat["did_activity"] if "did_activity" in cat else False
            new_cat.df_mentor = cat["df_mentor"] if "df_mentor" in cat else None
            new_cat.df_apprentices = cat["df_apprentices"] if "df_apprentices" in cat else []
            new_cat.faith = cat["faith"] if "faith" in cat else randint(-3,3)
            new_cat.connected_dialogue = cat["connected_dialogue"] if "connected_dialogue" in cat else {}
            if "died_by" in cat or "scar_event" in cat or "mentor_influence" in cat:
                new_cat.convert_history(
                    cat["died_by"] if "died_by" in cat else [],
                    cat["scar_event"] if "scar_event" in cat else [],
                )
            if "pronouns" in cat:
                for i in cat["pronouns"]:
                    if "sibling" not in i:
                        if new_cat.genderalign in ["male", "trans male"]:
                            i["sibling"] = "brother"
                        elif new_cat.genderalign in ["female", "trans female"]:
                            i["sibling"] = "sister"
                        else:
                            i["sibling"] = "sibling"

        
                    if "parent" not in i:
                        if new_cat.genderalign in ["male", "trans male"]:
                            i["parent"] = "father"
                        elif new_cat.genderalign in ["female", "trans female"]:
                            i["parent"] = "mother"
                        else:
                            i["parent"] = "parent"

            all_cats.append(new_cat)

        except KeyError as e:
            if "ID" in cat:
                key = f" ID #{cat['ID']} "
            else:
                key = f" at index {i} "
            game.switches["error_message"] = (
                f"Cat{key}in clan_cats.json is missing {e}!"
            )
            game.switches["traceback"] = e
            raise

    # replace cat ids with cat objects and add other needed variables
    for cat in all_cats:

        cat.load_conditions()

        # this is here to handle paralyzed cats in old saves
        if cat.pelt.paralyzed and "paralyzed" not in cat.permanent_condition:
            cat.get_permanent_condition("paralyzed")
        elif "paralyzed" in cat.permanent_condition and not cat.pelt.paralyzed:
            cat.pelt.paralyzed = True

        # load the relationships
        try:
            if not cat.dead:
                cat.load_relationship_of_cat()
                if cat.relationships is not None and len(cat.relationships) < 1:
                    cat.init_all_relationships()
            else:
                cat.relationships = {}
        except Exception as e:
            logger.exception(
                f"There was an error loading relationships for cat #{cat}."
            )
            game.switches["error_message"] = (
                f"There was an error loading relationships for cat #{cat}."
            )
            game.switches["traceback"] = e
            raise

        cat.inheritance = Inheritance(cat)

        try:
            # initialization of thoughts
            cat.thoughts()
        except Exception as e:
            logger.exception(
                f"There was an error when thoughts for cat #{cat} are created."
            )
            game.switches["error_message"] = (
                f"There was an error when thoughts for cat #{cat} are created."
            )
            game.switches["traceback"] = e
            raise

        # Save integrety checks
        if game.config["save_load"]["load_integrity_checks"]:
            save_check()

# csv load was gone from genemod but just in case i need it at some point...
# def csv_load(all_cats):
#     if game.switches["clan_list"][0].strip() == "":
#         cat_data = ""
#     else:
#         if os.path.exists(
#             get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.csv"
#         ):
#             with open(
#                 get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.csv", "r"
#             ) as read_file:
#                 cat_data = read_file.read()
#         else:
#             with open(
#                 get_save_dir() + "/" + game.switches["clan_list"][0] + "cats.txt", "r"
#             ) as read_file:
#                 cat_data = read_file.read()
#     if len(cat_data) > 0:
#         cat_data = cat_data.replace("\t", ",")
#         for i in cat_data.split("\n"):
#             # CAT: ID(0) - prefix:suffix(1) - gender(2) - status(3) - age(4) - trait(5) - parent1(6) - parent2(7) - mentor(8)
#             # PELT: pelt(9) - colour(10) - white(11) - length(12)
#             # SPRITE: kitten(13) - apprentice(14) - warrior(15) - elder(16) - eye colour(17) - reverse(18)
#             # - white patches(19) - pattern(20) - tortiebase(21) - tortiepattern(22) - tortiecolour(23) - skin(24) - skill(25) - NONE(26) - spec(27) - accessory(28) -
#             # spec2(29) - moons(30) - mate(31)
#             # dead(32) - SPRITE:dead(33) - exp(34) - dead for _ moons(35) - current apprentice(36)
#             # (BOOLS, either TRUE OR FALSE) paralyzed(37) - no kits(38) - exiled(39)
#             # genderalign(40) - former apprentices list (41)[FORMER APPS SHOULD ALWAYS BE MOVED TO THE END]
#             if i.strip() != "":
#                 attr = i.split(",")
#                 for x in range(len(attr)):
#                     attr[x] = attr[x].strip()
#                     if attr[x] in ["None", "None "]:
#                         attr[x] = None
#                     elif attr[x].upper() == "TRUE":
#                         attr[x] = True
#                     elif attr[x].upper() == "FALSE":
#                         attr[x] = False
#                 game.switches["error_message"] = (
#                     "1There was an error loading cat # " + str(attr[0])
#                 )
#                 the_pelt = Pelt(
#                     colour=attr[2], name=attr[11], length=attr[9], eye_color=attr[17]
#                 )
#                 game.switches["error_message"] = (
#                     "2There was an error loading cat # " + str(attr[0])
#                 )
#                 the_cat = Cat(
#                     ID=attr[0],
#                     prefix=attr[1].split(":")[0],
#                     suffix=attr[1].split(":")[1],
#                     gender=attr[2],
#                     status=attr[3],
#                     pelt=the_pelt,
#                     parent1=attr[6],
#                     parent2=attr[7],
#                 )

#                 game.switches["error_message"] = (
#                     "3There was an error loading cat # " + str(attr[0])
#                 )
#                 the_cat.age, the_cat.mentor = attr[4], attr[8]
#                 game.switches["error_message"] = (
#                     "4There was an error loading cat # " + str(attr[0])
#                 )
#                 (
#                     the_cat.pelt.cat_sprites["kitten"],
#                     the_cat.pelt.cat_sprites["adolescent"],
#                 ) = int(attr[13]), int(attr[14])
#                 game.switches["error_message"] = (
#                     "5There was an error loading cat # " + str(attr[0])
#                 )
#                 the_cat.pelt.cat_sprites["adult"], the_cat.pelt.cat_sprites["elder"] = (
#                     int(attr[15]),
#                     int(attr[16]),
#                 )
#                 game.switches["error_message"] = (
#                     "6There was an error loading cat # " + str(attr[0])
#                 )
#                 (
#                     the_cat.pelt.cat_sprites["young adult"],
#                     the_cat.pelt.cat_sprites["senior adult"],
#                 ) = int(attr[15]), int(attr[15])
#                 game.switches["error_message"] = (
#                     "7There was an error loading cat # " + str(attr[0])
#                 )
#                 (
#                     the_cat.pelt.reverse,
#                     the_cat.pelt.white_patches,
#                     the_cat.pelt.pattern,
#                 ) = (attr[18], attr[19], attr[20])
#                 game.switches["error_message"] = (
#                     "8There was an error loading cat # " + str(attr[0])
#                 )
#                 (
#                     the_cat.pelt.tortiebase,
#                     the_cat.pelt.tortiepattern,
#                     the_cat.pelt.tortiecolour,
#                 ) = (attr[21], attr[22], attr[23])
#                 game.switches["error_message"] = (
#                     "9There was an error loading cat # " + str(attr[0])
#                 )
#                 the_cat.trait, the_cat.pelt.skin, the_cat.specialty = (
#                     attr[5],
#                     attr[24],
#                     attr[27],
#                 )
#                 game.switches["error_message"] = (
#                     "10There was an error loading cat # " + str(attr[0])
#                 )
#                 the_cat.skill = attr[25]
#                 if len(attr) > 28:
#                     the_cat.pelt.accessory = attr[28]
#                 if len(attr) > 29:
#                     the_cat.specialty2 = attr[29]
#                 else:
#                     the_cat.specialty2 = None
#                 game.switches["error_message"] = (
#                     "11There was an error loading cat # " + str(attr[0])
#                 )
#                 if len(attr) > 34:
#                     the_cat.experience = int(attr[34])
#                     experiencelevels = [
#                         "very low",
#                         "low",
#                         "slightly low",
#                         "average",
#                         "somewhat high",
#                         "high",
#                         "very high",
#                         "master",
#                         "max",
#                     ]
#                     the_cat.experience_level = experiencelevels[
#                         floor(int(the_cat.experience) / 10)
#                     ]
#                 else:
#                     the_cat.experience = 0
#                 game.switches["error_message"] = (
#                     "12There was an error loading cat # " + str(attr[0])
#                 )
#                 if len(attr) > 30:
#                     # Attributes that are to be added after the update
#                     the_cat.moons = int(attr[30])
#                     if len(attr) >= 31:
#                         # assigning mate to cat, if any
#                         the_cat.mate = [attr[31]]
#                     if len(attr) >= 32:
#                         # Is the cat dead
#                         the_cat.dead = attr[32]
#                         the_cat.pelt.cat_sprites["dead"] = attr[33]
#                 game.switches["error_message"] = (
#                     "13There was an error loading cat # " + str(attr[0])
#                 )
#                 if len(attr) > 35:
#                     the_cat.dead_for = int(attr[35])
#                 game.switches["error_message"] = (
#                     "14There was an error loading cat # " + str(attr[0])
#                 )
#                 if len(attr) > 36 and attr[36] is not None:
#                     the_cat.apprentice = attr[36].split(";")
#                 game.switches["error_message"] = (
#                     "15There was an error loading cat # " + str(attr[0])
#                 )
#                 if len(attr) > 37:
#                     the_cat.pelt.paralyzed = bool(attr[37])
#                 if len(attr) > 38:
#                     the_cat.pelt.paralyzed = bool(attr[38])
#                 if len(attr) > 39:
#                     the_cat.no_kits = bool(attr[39])
#                 if len(attr) > 40:
#                     the_cat.genderalign = attr[40]
#                 if len(attr) > 41 and attr[41] is not None:  # KEEP THIS AT THE END
#                     the_cat.former_apprentices = attr[41].split(";")
#         game.switches["error_message"] = (
#             "There was an error loading this clan's mentors, apprentices, relationships, or sprite info."
#         )
#         for inter_cat in all_cats.values():
#             # Load the mentors and apprentices after all cats have been loaded
#             game.switches["error_message"] = (
#                 "There was an error loading this clan's mentors/apprentices. Last cat read was "
#                 + str(inter_cat)
#             )
#             inter_cat.mentor = Cat.all_cats.get(inter_cat.mentor)
#             apps = []
#             former_apps = []
#             for app_id in inter_cat.apprentice:
#                 app = Cat.all_cats.get(app_id)
#                 # Make sure if cat isn't an apprentice, they're a former apprentice
#                 if "apprentice" in app.status:
#                     apps.append(app)
#                 else:
#                     former_apps.append(app)
#             for f_app_id in inter_cat.former_apprentices:
#                 f_app = Cat.all_cats.get(f_app_id)
#                 former_apps.append(f_app)
#             inter_cat.apprentice = [
#                 a.ID for a in apps
#             ]  # Switch back to IDs. I don't want to risk breaking everything.
#             inter_cat.former_apprentices = [a.ID for a in former_apps]
#             if not inter_cat.dead:
#                 game.switches["error_message"] = (
#                     "There was an error loading this clan's relationships. Last cat read was "
#                     + str(inter_cat)
#                 )
#                 inter_cat.load_relationship_of_cat()
#             game.switches["error_message"] = (
#                 "There was an error loading a cat's sprite info. Last cat read was "
#                 + str(inter_cat)
#             )
#             # update_sprite(inter_cat)
#         # generate the relationship if some is missing
#         if not the_cat.dead:
#             game.switches["error_message"] = (
#                 "There was an error when relationships where created."
#             )
#             for id in all_cats.keys():
#                 the_cat = all_cats.get(id)
#                 game.switches["error_message"] = (
#                     f"There was an error when relationships for cat #{the_cat} are created."
#                 )
#                 if the_cat.relationships is not None and len(the_cat.relationships) < 1:
#                     the_cat.create_all_relationships()
#         game.switches["error_message"] = ""


def save_check():
    """Checks through loaded cats, checks and attempts to fix issues
    NOT currently working."""
    return

    for cat in Cat.all_cats:
        cat_ob = Cat.all_cats[cat]

        # Not-mutural mate relations
        # if cat_ob.mate:
        #    _temp_ob = Cat.all_cats.get(cat_ob.mate)
        #    if _temp_ob:
        #        # Check if the mate's mate feild is set to none
        #        if not _temp_ob.mate:
        #            _temp_ob.mate = cat_ob.ID
        #    else:
        #        # Invalid mate
        #        cat_ob.mate = None


def version_convert(version_info):
    """Does all save-conversion that require referencing the saved version number.
    This is a separate function, since the version info is stored in clan.json, but most conversion needs to be
    done on the cats. Clan data is loaded in after cats, however."""

    if version_info is None:
        return

    if version_info["version_name"] == SAVE_VERSION_NUMBER:
        # Save was made on current version
        return

    if version_info["version_name"] is None:
        version = 0
    else:
        version = version_info["version_name"]

    if version < 1:
        # Save was made before version number storage was implemented.
        # (ie, save file version 0)
        # This means the EXP must be adjusted.
        for c in Cat.all_cats.values():
            c.experience = c.experience * 3.2

    if version < 2:
        for c in Cat.all_cats.values():
            for con in c.injuries:
                moons_with = 0
                if "moons_with" in c.injuries[con]:
                    moons_with = c.injuries[con]["moons_with"]
                    c.injuries[con].pop("moons_with")
                c.injuries[con]["moon_start"] = game.clan.age - moons_with

            for con in c.illnesses:
                moons_with = 0
                if "moons_with" in c.illnesses[con]:
                    moons_with = c.illnesses[con]["moons_with"]
                    c.illnesses[con].pop("moons_with")
                c.illnesses[con]["moon_start"] = game.clan.age - moons_with

            for con in c.permanent_condition:
                moons_with = 0
                if "moons_with" in c.permanent_condition[con]:
                    moons_with = c.permanent_condition[con]["moons_with"]
                    c.permanent_condition[con].pop("moons_with")
                c.permanent_condition[con]["moon_start"] = game.clan.age - moons_with

    if version < 3 and game.clan.freshkill_pile:
        # freshkill start for older clans
        add_prey = game.clan.freshkill_pile.amount_food_needed() * 2
        game.clan.freshkill_pile.add_freshkill(add_prey)

import os
from copy import copy

import pygame

import os

import ujson

from scripts.game_structure.game_essentials import game


class Sprites:
    cat_tints = {}
    white_patches_tints = {}
    clan_symbols = []

    def __init__(self):
        """Class that handles and hold all spritesheets. 
        Size is normally automatically determined by the size
        of the lineart. If a size is passed, it will override 
        this value. """
        self.symbol_dict = None
        self.size = None
        self.spritesheets = {}
        self.images = {}
        self.sprites = {}

        # Shared empty sprite for placeholders
        self.blank_sprite = None

        self.load_tints()

    def load_tints(self):
        try:
            with open("sprites/dicts/tint.json", 'r') as read_file:
                self.cat_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading Tints")

        try:
            with open("sprites/dicts/white_patches_tint.json", 'r') as read_file:
                self.white_patches_tints = ujson.loads(read_file.read())
        except IOError:
            print("ERROR: Reading White Patches Tints")

    def spritesheet(self, a_file, name):
        """
        Add spritesheet called name from a_file.

        Parameters:
        a_file -- Path to the file to create a spritesheet from.
        name -- Name to call the new spritesheet.
        """
        self.spritesheets[name] = pygame.image.load(a_file).convert_alpha()

    def make_group(self,
                   spritesheet,
                   pos,
                   name,
                   sprites_x=3,
                   sprites_y=7,
                   no_index=False):  # pos = ex. (2, 3), no single pixels

        """
        Divide sprites on a spritesheet into groups of sprites that are easily accessible
        :param spritesheet: Name of spritesheet file
        :param pos: (x,y) tuple of offsets. NOT pixel offset, but offset of other sprites
        :param name: Name of group being made
        :param sprites_x: default 3, number of sprites horizontally
        :param sprites_y: default 3, number of sprites vertically
        :param no_index: default False, set True if sprite name does not require cat pose index
        """
        group_x_ofs = pos[0] * sprites_x * self.size
        group_y_ofs = pos[1] * sprites_y * self.size
        i = 0

        # splitting group into singular sprites and storing into self.sprites section
        for y in range(sprites_y):
            for x in range(sprites_x):
                if no_index:
                    full_name = f"{name}"
                else:
                    full_name = f"{name}{i}"

                try:
                    new_sprite = pygame.Surface.subsurface(
                        self.spritesheets[spritesheet],
                        group_x_ofs + x * self.size,
                        group_y_ofs + y * self.size,
                        self.size, self.size
                    )

                except ValueError:
                    # Fallback for non-existent sprites
                    print(f"WARNING: nonexistent sprite - {full_name}")
                    if not self.blank_sprite:
                        self.blank_sprite = pygame.Surface(
                            (self.size, self.size),
                            pygame.HWSURFACE | pygame.SRCALPHA
                        )
                    new_sprite = self.blank_sprite

                self.sprites[full_name] = new_sprite
                i += 1

    def load_all(self):
        # get the width and height of the spritesheet
        lineart = pygame.image.load('sprites/lineart.png')
        width, height = lineart.get_size()
        del lineart  # unneeded

        # if anyone changes lineart for whatever reason update this
        if isinstance(self.size, int):
            pass
        elif width / 3 == height / 7:
            self.size = width / 3
        else:
            self.size = 50  # default, what base clangen uses
            print(f"lineart.png is not 3x7, falling back to {self.size}")
            print(f"if you are a modder, please update scripts/cat/sprites.py and "
                  f"do a search for 'if width / 3 == height / 7:'")

        del width, height  # unneeded

        for x in [
            'whitepatches', 'scars', 'missingscars',
            'lineart', 'lineartdf', 'lineartdead',
            'eyes', 'eyes2', 'skin',
            'medcatherbs', 'wild',
            'collars', 'bellcollars', 'bowcollars', 'nyloncollars',
            'shadersnewwhite', 'tortiepatchesmasks', 
            'lightingnew', 'fademask',
            'fadestarclan', 'fadedarkforest',
            'symbols',

            #OHDANS
            'flower_accessories', 'plant2_accessories', 'snake_accessories', 'smallAnimal_accessories', 'deadInsect_accessories',
            'aliveInsect_accessories', 'fruit_accessories', 'crafted_accessories', 'tail2_accessories',

            #WILDS
            'wildaccs_1', 'wildaccs_2',

            #SUPERARTSI
            'superartsi',

            #coffee
            'coffee',

            'eragona',

            "crowns",

            "wooddragon",

            "springwinter",

            "raincoat",

            "poptabs",

            "fazbear",

            "bears",

            "tide",

            "chimes",

            "moipa",

            "moipa2",

            "eggs",

            "pumpkinbatharness",

            "toast",

            "stoats"

        ]:
            if 'lineart' in x and game.config['fun']['april_fools']:
                self.spritesheet(f"sprites/aprilfools{x}.png", x)
            else:
                self.spritesheet(f"sprites/{x}.png", x)

        for x in os.listdir("sprites/genemod/borders"):
            sprites.spritesheet("sprites/genemod/borders/"+x, 'genemod/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/Base Colours"):
            sprites.spritesheet("sprites/genemod/Base Colours/"+x, 'base/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/points"):
            sprites.spritesheet("sprites/genemod/points/"+x, x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/New Tabbies"):
            sprites.spritesheet("sprites/genemod/New Tabbies/"+x, 'Tabby/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/extra"):
            sprites.spritesheet("sprites/genemod/extra/"+x, 'Other/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/effects"):
            sprites.spritesheet("sprites/genemod/effects/"+x, 'Other/'+x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/somatic"):
            sprites.spritesheet("sprites/genemod/somatic/"+x, 'Somatic/'+x.replace('.png', ""))
            self.make_group('Somatic/'+x.replace('.png', ""), (0, 0), "Somatic/"+x.replace('.png', ""))
        
        
        for x in os.listdir("sprites/genemod/white"):
            sprites.spritesheet("sprites/genemod/white/"+x, 'White/'+x.replace('.png', ""))
            self.make_group('White/'+x.replace('.png', ""), (0, 0), x.replace('.png', ""))
        for x in os.listdir("sprites/genemod/break white"):
            sprites.spritesheet("sprites/genemod/break white/"+x, 'Break/'+x.replace('.png', ""))
            self.make_group('Break/'+x.replace('.png', ""), (0, 0), 'break/'+x.replace('.png', ""))

        # ...idk what to call these

        self.make_group('genemod/normal border', (0, 0), 'normbord')
        self.make_group('genemod/foldborder', (0, 0), 'foldbord')
        self.make_group('genemod/curlborder', (0, 0), 'curlbord')
        self.make_group('genemod/foldlineart', (0, 0), 'foldlines')
        self.make_group('genemod/fold_curllineart', (0, 0), 'fold_curllines')
        self.make_group('genemod/curllineart', (0, 0), 'curllines')
        self.make_group('genemod/foldlineartdf', (0, 0), 'foldlineartdf')
        self.make_group('genemod/fold_curllineartdf', (0, 0), 'fold_curllineartdf')
        self.make_group('genemod/curllineartdf', (0, 0), 'curllineartdf')
        self.make_group('genemod/foldlineartdead', (0, 0), 'foldlineartdead')
        self.make_group('genemod/fold_curllineartdead', (0, 0), 'fold_curllineartdead')
        self.make_group('genemod/curllineartdead', (0, 0), 'curllineartdead')

        self.make_group('genemod/isolateears', (0, 0), 'isolateears')
        self.make_group('genemod/noears', (0, 0), 'noears')
        
        self.make_group('genemod/rexlines', (0, 0), 'rexlineart')
        self.make_group('genemod/rexlinesdead', (0, 0), 'rexlineartdead')
        self.make_group('genemod/rexlinesdf', (0, 0), 'rexlineartdf')
        self.make_group('genemod/rexborder', (0, 0), 'rexbord')

        for a, x in enumerate(range(1, 6)):
            self.make_group('genemod/bobtails', (a, 0), f'bobtail{x}')

        # genemod base colours

        self.make_group('base/bases', (0, 0), 'basecolours', sprites_x=6, sprites_y=4)
        self.make_group('base/lightbases', (0, 0), 'lightbasecolours', sprites_x=4, sprites_y=1)

        # genemod tabby bases

        for x in ["black", "blue", "dove", "platinum",
                  "chocolate", "lilac", "champagne", "lavender",
                  "cinnamon", "fawn", "buff", "beige",
                  "red", "cream", "honey", "ivory"]:
            for a, i in enumerate(['rufousedlow', 'rufousedmedium', 'rufousedhigh', 'rufousedshaded', 'rufousedchinchilla']):
                self.make_group('Tabby/'+x, (a, 0), f'{x}{i}', sprites_x=1, sprites_y=1)
            for a, i in enumerate(['mediumlow', 'mediummedium', 'mediumhigh', 'mediumshaded', 'mediumchinchilla']):
                self.make_group('Tabby/'+x, (a, 1), f'{x}{i}', sprites_x=1, sprites_y=1)
            for a, i in enumerate(['lowlow', 'lowmedium', 'lowhigh', 'lowshaded', 'lowchinchilla']):
                self.make_group('Tabby/'+x, (a, 2), f'{x}{i}', sprites_x=1, sprites_y=1)
            for a, i in enumerate(['silverlow', 'silvermedium', 'silverhigh', 'silvershaded', 'silverchinchilla']):
                self.make_group('Tabby/'+x, (a, 3), f'{x}{i}', sprites_x=1, sprites_y=1)
        for a, x in enumerate(['low', 'medium', 'high', 'shaded', 'chinchilla']):
            self.make_group('Tabby/shading', (a, 0), f'{x}shading')
        self.make_group('Tabby/unders', (0, 0), f'Tabby_unders')

        # genemod tabby patterns

        for a, i in enumerate(['mackerel', 'brokenmack', 'spotted', 'classic', 'fullbar']):
            self.make_group('Other/tabbypatterns', (a, 0), f'{i}')
        for a, i in enumerate(['braided', 'brokenbraid', 'rosetted', 'marbled', 'redbar']):
            self.make_group('Other/tabbypatterns', (a, 1), f'{i}')
        for a, i in enumerate(['pinstripe', 'brokenpins', 'servaline', 'fullbarc', 'agouti']):
            self.make_group('Other/tabbypatterns', (a, 2), f'{i}')
        for a, i in enumerate(['pinsbraided', 'brokenpinsbraid', 'leopard', 'redbarc', 'charcoal']):
            self.make_group('Other/tabbypatterns', (a, 3), f'{i}')
        
        #genemod point markings

        self.make_group('points_spring', (0, 0), 'pointsm')
        self.make_group('points_summer', (0, 0), 'pointsl')
        self.make_group('points_winter', (0, 0), 'pointsd')
        self.make_group('mocha_spring', (0, 0), 'mocham')
        self.make_group('mocha_summer', (0, 0), 'mochal')
        self.make_group('mocha_winter', (0, 0), 'mochad')

        #genemod karpati
        for a, x in enumerate(['hetkarpatiwinter', 'hetkarpatispring', 'hetkarpatisummer']):
            self.make_group('Other/karpati', (a, 0), x)
        for a, x in enumerate(['homokarpatiwinter', 'homokarpatispring', 'homokarpatisummer']):
            self.make_group('Other/karpati', (a, 1), x)

        #genemod effects
        self.make_group('Other/bimetal', (0, 0), 'bimetal')
        self.make_group('Other/ghosting', (0, 0), 'ghost')
        self.make_group('Other/tabbyghost', (0, 0), 'tabbyghost')
        self.make_group('Other/grizzle', (0, 0), 'grizzle')
        self.make_group('Other/smoke', (0, 0), 'smoke')
        self.make_group('Other/bleach', (0, 0), 'bleach')
        self.make_group('Other/lykoi', (0, 0), 'lykoi')
        self.make_group('Other/hairless', (0, 0), 'hairless')
        self.make_group('Other/donskoy', (0, 0), 'donskoy')
        self.make_group('Other/furpoint', (0, 0), 'furpoint')
        self.make_group('Other/caramel', (0, 0), 'caramel', 1, 1)
        self.make_group('Other/satin', (0, 0), 'satin', 1, 1)
        self.make_group('Other/salmiak', (0, 0), 'salmiak')


        #genemod extra
        self.make_group('Other/ears', (0, 0), 'ears')
        # self.make_group('Other/albino_skin', (0, 0), 'albino') # in old ver, not in merge. here just in case
        self.make_group('Other/noses', (0, 0), 'nose')
        self.make_group('Other/nose_colours', (0, 0), 'nosecolours', sprites_y=5)
        self.make_group('Other/paw_pads', (0, 0), 'pads')

        #genemod eyes

        for i, x in enumerate(['left', 'right', 'sectoral1', 'sectoral2', 'sectoral3', 'sectoral4', 'sectoral5', 'sectoral6']):
            self.make_group('Other/eyebase', (i, 0), x, sprites_y=6)
        
        for b, x in enumerate(['P11', 'P10', 'P9', 'P8', 'P7', 'P6', 'P5', 'P4', 'P3', 'P2', 'P1', 'blue', 'albino']):
            for a, y in enumerate(range(1, 12)):
                self.make_group('Other/eyes_full', (a, b), f'R{y} ; {x}/', sprites_y=6)
        
        self.make_group('Other/red_pupils', (0, 0), 'redpupils')

        # Line art
        self.make_group('lineart', (0, 0), 'lines')
        self.make_group('shadersnewwhite', (0, 0), 'shaders')
        self.make_group('lightingnew', (0, 0), 'lighting')

        self.make_group('lineartdead', (0, 0), 'lineartdead')
        self.make_group('lineartdf', (0, 0), 'lineartdf')
        # Fading Fog
        for i in range(0, 3):
            self.make_group('fademask', (i, 0), f'fademask{i}')
            self.make_group('fadestarclan', (i, 0), f'fadestarclan{i}')
            self.make_group('fadedarkforest', (i, 0), f'fadedf{i}')

        
        # Define white patches
        white_patches = [
            ['FULLWHITE', 'ANY', 'TUXEDO', 'LITTLE', 'COLOURPOINT', 'VAN', 'ANYTWO', 'MOON', 'PHANTOM', 'POWDER',
             'BLEACHED', 'SAVANNAH', 'FADESPOTS', 'PEBBLESHINE'],
            ['EXTRA', 'ONEEAR', 'BROKEN', 'LIGHTTUXEDO', 'BUZZARDFANG', 'RAGDOLL', 'LIGHTSONG', 'VITILIGO', 'BLACKSTAR',
             'PIEBALD', 'CURVED', 'PETAL', 'SHIBAINU', 'OWL'],
            ['TIP', 'FANCY', 'FRECKLES', 'RINGTAIL', 'HALFFACE', 'PANTSTWO', 'GOATEE', 'VITILIGOTWO', 'PAWS', 'MITAINE',
             'BROKENBLAZE', 'SCOURGE', 'DIVA', 'BEARD'],
            ['TAIL', 'BLAZE', 'PRINCE', 'BIB', 'VEE', 'UNDERS', 'HONEY', 'FAROFA', 'DAMIEN', 'MISTER', 'BELLY',
             'TAILTIP', 'TOES', 'TOPCOVER'],
            ['APRON', 'CAPSADDLE', 'MASKMANTLE', 'SQUEAKS', 'STAR', 'TOESTAIL', 'RAVENPAW', 'PANTS', 'REVERSEPANTS',
             'SKUNK', 'KARPATI', 'HALFWHITE', 'APPALOOSA', 'DAPPLEPAW'],
            ['HEART', 'LILTWO', 'GLASS', 'MOORISH', 'SEPIAPOINT', 'MINKPOINT', 'SEALPOINT', 'MAO', 'LUNA', 'CHESTSPECK',
             'WINGS', 'PAINTED', 'HEARTTWO', 'WOODPECKER'],
            ['BOOTS', 'MISS', 'COW', 'COWTWO', 'BUB', 'BOWTIE', 'MUSTACHE', 'REVERSEHEART', 'SPARROW', 'VEST',
             'LOVEBUG', 'TRIXIE', 'SAMMY', 'SPARKLE'],
            ['RIGHTEAR', 'LEFTEAR', 'ESTRELLA', 'SHOOTINGSTAR', 'EYESPOT', 'REVERSEEYE', 'FADEBELLY', 'FRONT',
             'BLOSSOMSTEP', 'PEBBLE', 'TAILTWO', 'BUDDY', 'BACKSPOT', 'EYEBAGS'],
            ['BULLSEYE', 'FINN', 'DIGIT', 'KROPKA', 'FCTWO', 'FCONE', 'MIA', 'SCAR', 'BUSTER', 'SMOKEY', 'HAWKBLAZE',
             'CAKE', 'ROSINA', 'PRINCESS'],
            ['LOCKET', 'BLAZEMASK', 'TEARS', 'DOUGIE']
        ]

        for row, patches in enumerate(white_patches):
            for col, patch in enumerate(patches):
                self.make_group('whitepatches', (col, row), patch)
            
        # tortiepatchesmasks
        tortiepatchesmasks = [
            ['ONE', 'TWO', 'THREE', 'FOUR', 'REDTAIL', 'DELILAH', 'HALF', 'STREAK', 'MASK', 'SMOKE'],
            ['MINIMALONE', 'MINIMALTWO', 'MINIMALTHREE', 'MINIMALFOUR', 'OREO', 'SWOOP', 'CHIMERA', 'CHEST', 'ARMTAIL',
             'GRUMPYFACE'],
            ['MOTTLED', 'SIDEMASK', 'EYEDOT', 'BANDANA', 'PACMAN', 'STREAMSTRIKE', 'SMUDGED', 'DAUB', 'EMBER', 'BRIE'],
            ['ORIOLE', 'ROBIN', 'BRINDLE', 'PAIGE', 'ROSETAIL', 'SAFI', 'DAPPLENIGHT', 'BLANKET', 'BELOVED', 'BODY'],
            ['SHILOH', 'FRECKLED', 'HEARTBEAT', 'CRYPTIC']
        ]

        for row, masks in enumerate(tortiepatchesmasks):
            for col, mask in enumerate(masks):
                self.make_group('tortiepatchesmasks', (col, row), f"tortiemask{mask}")
        self.make_group('Other/blue-tipped', (0, 0), 'tortiemaskBLUE-TIPPED')

        self.load_scars()
        self.load_symbols()

    def load_scars(self):
        """
        Loads scar sprites and puts them into groups.
        """

            # ohdan's accessories
        for a, i in enumerate([
            "DAISIES", "DIANTHUS", "BLEEDING HEARTS", "FRANGIPANI", "BLUE GLORY", "CATNIP FLOWER", "BLANKET FLOWER", "ALLIUM", "LACELEAF", "PURPLE GLORY"]):
            self.make_group('flower_accessories', (a, 0), f'acc_flower{i}')
        for a, i in enumerate([
            "YELLOW PRIMROSE", "HESPERIS", "MARIGOLD", "WISTERIA"]):
            self.make_group('flower_accessories', (a, 1), f'acc_flower{i}')
        
        for a, i in enumerate([
            "SINGULARCLOVER", "STICK", "PUMPKIN", "MOSS", "IVY", "ACORN", "MOSS PELT", "REEDS", "BAMBOO"]):
            self.make_group('plant2_accessories', (a, 0), f'acc_plant2{i}')

        for a, i in enumerate([
            "GRASS SNAKE", "BLUE RACER", "WESTERN COACHWHIP", "KINGSNAKE"]):
            self.make_group('snake_accessories', (a, 0), f'acc_snake{i}')
            
        for a, i in enumerate([
            "GRAY SQUIRREL", "RED SQUIRREL", "CRAB", "WHITE RABBIT", "BLACK RABBIT", "BROWN RABBIT", "INDIAN GIANT SQUIRREL", "FAWN RABBIT", "BROWN AND WHITE RABBIT", "BLACK AND WHITE RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 0), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "WHITE AND FAWN RABBIT", "BLACK VITILIGO RABBIT", "BROWN VITILIGO RABBIT", "FAWN VITILIGO RABBIT", "BLACKBIRD", "ROBIN", "JAY", "THRUSH", "CARDINAL", "MAGPIE"]):
            self.make_group('smallAnimal_accessories', (a, 1), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "CUBAN TROGON", "TAN RABBIT", "TAN AND WHITE RABBIT", "TAN VITILIGO RABBIT", "RAT", "WHITE MOUSE", "BLACK MOUSE", "GRAY MOUSE", "BROWN MOUSE", "GRAY RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 2), f'acc_smallAnimal{i}')
        for a, i in enumerate([
            "GRAY AND WHITE RABBIT", "GRAY VITILIGO RABBIT"]):
            self.make_group('smallAnimal_accessories', (a, 3), f'acc_smallAnimal{i}')
            
        for a, i in enumerate([
            "LUNAR MOTH", "ROSY MAPLE MOTH", "MONARCH", "DAPPLED MONARCH", "POLYPHEMUS MOTH", "MINT MOTH"]):
            self.make_group('deadInsect_accessories', (a, 0), f'acc_deadInsect{i}')
            
        for a, i in enumerate([
            "BROWN SNAIL", "RED SNAIL", "WORM", "BLUE SNAIL", "ZEBRA ISOPOD", "DUCKY ISOPOD", "DAIRY COW ISOPOD", "BEETLEJUICE ISOPOD", "BEE", "RED LADYBUG"]):
            self.make_group('aliveInsect_accessories', (a, 0), f'acc_aliveInsect{i}')
        for a, i in enumerate([
            "ORANGE LADYBUG", "YELLOW LADYBUG"]):
            self.make_group('aliveInsect_accessories', (a, 1), f'acc_aliveInsect{i}')
        
        for a, i in enumerate([
            "RASPBERRY2", "BLACKBERRY", "GOLDEN RASPBERRY", "CHERRY", "YEW"]):
            self.make_group('fruit_accessories', (a, 0), f'acc_fruit{i}')
        
        for a, i in enumerate([
            "WILLOWBARK BAG", "CLAY DAISY POT", "CLAY AMANITA POT", "CLAY BROWNCAP POT", "BIRD SKULL", "LEAF BOW"]):
            self.make_group('crafted_accessories', (a, 0), f'acc_crafted{i}')
        
        for a, i in enumerate([
            "SEAWEED", "DAISY CORSAGE"]):
            self.make_group('tail2_accessories', (a, 0), f'acc_tail2{i}')


        # wilds accessories redone sheets by moipa and jay
        for a, i in enumerate([
            "LILYPAD", "LARGE DEATHBERRY", "SMALL DEATHBERRY", "ACORN2", "PINECONE", "VINE"]):
            self.make_group('wildaccs_1', (a, 0), f'acc_herbs{i}')
        
        for a, i in enumerate([
            "CHERRY2", "BLEEDING HEARTS2", "SHELL PACK", "FERNS", "GOLD FERNS"]):
            self.make_group('wildaccs_1', (a, 1), f'acc_herbs{i}')

        for a, i in enumerate([
            "WHEAT", "BLACK WHEAT"]):
            self.make_group('wildaccs_1', (a, 2), f'acc_herbs{i}')
        
        # -------------------------------------------------------------------------
        
        for a, i in enumerate([
            "BERRIES", "CLOVERS", "CLOVER2", "MOSS2", "FLOWER MOSS", "MUSHROOMS"]):
            self.make_group('wildaccs_2', (a, 0), f'acc_herbs{i}')

        for a, i in enumerate([
            "LARGE LUNA", "LARGE COMET", "SMALL LUNA", "SMALL COMET", "LADYBUG"]):
            self.make_group('wildaccs_2', (a, 1), f'acc_wild{i}')

        for a, i in enumerate([
            "MUD PAWS", "ASHY PAWS"]):
            self.make_group('wildaccs_2', (a, 2), f'acc_wild{i}')

        # superartsi's accessories

        for a, i in enumerate([
            "ORANGEBUTTERFLY", "BLUEBUTTERFLY", "BROWNPELT", "GRAYPELT", "BROWNMOSSPELT", "GRAYMOSSPELT"]):
            self.make_group('superartsi', (a, 0), f'acc_wild{i}')
        for a, i in enumerate([
            "FERN", "MOREFERN", "BLEEDINGVINES", "BLEEDINGHEART", "LILY"]):
            self.make_group('superartsi', (a, 1), f'acc_wild{i}')

        # coffee's accessories
        for a, i in enumerate([
            "PINKFLOWERCROWN", "YELLOWFLOWERCROWN", "BLUEFLOWERCROWN", "PURPLEFLOWERCROWN"]):
            self.make_group('coffee', (a, 0), f'acc_flower{i}')

        # eragona rose's accessories

        for a, i in enumerate([
            "REDHARNESS", "NAVYHARNESS", "YELLOWHARNESS", "TEALHARNESS", "ORANGEHARNESS", "GREENHARNESS"]):
            self.make_group('eragona', (a, 0), f'collars{i}')
        for a, i in enumerate([
            "MOSSHARNESS", "RAINBOWHARNESS", "BLACKHARNESS", "BEEHARNESS", "CREAMHARNESS"]):
            self.make_group('eragona', (a, 1), f'collars{i}')
        for a, i in enumerate([
            "PINKHARNESS", "MAGENTAHARNESS", "PEACHHARNESS", "VIOLETHARNESS"]):
            self.make_group('eragona', (a, 2), f'collars{i}')

        for a, i in enumerate([
            "YELLOWCROWN", "REDCROWN", "LILYPADCROWN"]):
            self.make_group('crowns', (a, 0), f'acc_wild{i}')

        for a, i in enumerate([
            "WOODDRAGON"]):
            self.make_group('wooddragon', (a, 0), f'acc_wild{i}')


        for a, i in enumerate(["CHERRYBLOSSOM","TULIPPETALS","CLOVERFLOWER","PANSIES","BELLFLOWERS","SANVITALIAFLOWERS","EGGSHELLS","BLUEEGGSHELLS","EASTEREGG","FORSYTHIA"]):
            self.make_group('springwinter', (a, 0), f'acc_wild{i}')
        for a, i in enumerate([
            "MINTLEAF","STICKS","SPRINGFEATHERS","SNAILSHELL","MUD","CHERRYPLUMLEAVES","CATKIN","HONEYCOMB","FLOWERCROWN","LILIESOFTHEVALLEY"]):
            self.make_group('springwinter', (a, 1), f'acc_wild{i}')
        for a, i in enumerate([
            "STRAWMANE","MISTLETOE","REDPOINSETTIA","WHITEPOINSETTIA","COTONEASTERWREATH","YEWS","CALLUNA","TEETHCOLLAR","DRIEDORANGE","ROESKULL"]):
            self.make_group('springwinter', (a, 2), f'acc_wild{i}')
        for a, i in enumerate([
            "WOODENOAKANTLERS","WOODENBIRCHANTLERS","DOGWOOD","GRAYWOOL","BLACKWOOL","CREAMWOOL","WHITEWOOL","FIRBRANCHES","CORALBELLS","SLIVERDUSTPLANT"]):
            self.make_group('springwinter', (a, 3), f'acc_wild{i}')

        for a, i in enumerate([
            "RAINCOAT"]):
            self.make_group('raincoat', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "POPTABS"]):
            self.make_group('poptabs', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "FAZBEAR"]):
            self.make_group('fazbear', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "WHITEBEAR", "PANDA", "BEAR", "BROWNBEAR"]):
            self.make_group('bears', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "TIDE"]):
            self.make_group('tide', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "CELESTIALCHIMES", "STARCHIMES", "LUNARCHIMES", "SILVERLUNARCHIMES"]):
            self.make_group('chimes', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "FIDDLEHEADS", "LANTERNS", "HEARTCHARMS"]):
            self.make_group('moipa', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "SPRINGFLOWERCORSAGE", "ORCHID", "SPRINGFLOWERS", "RADIO", "SWANFEATHER", "DRACULAPARROTFEATHER", "JAYFEATHER"]):
            self.make_group('moipa2', (a, 0), f'acc_flower{i}')
        
        for a, i in enumerate([
            "EAGLEFEATHER", "STARFLOWERS", "HEARTLEAVES", "YELLOWWISTERIA", "HOLLY2", "HOLLYVINES"]):
            self.make_group('moipa2', (a, 1), f'acc_wild{i}')

        for a, i in enumerate([
            "LAVENDERHEADPIECE", "LAVENDERTAILWRAP", "LAVENDERANKLET"]):
            self.make_group('moipa2', (a, 2), f'acc_wild{i}')

        for a, i in enumerate([
            "EGG"]):
            self.make_group('eggs', (a, 0), f'acc_wild{i}')

        for a, i in enumerate([
            "BATHARNESS"]):
            self.make_group('pumpkinbatharness', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "TOAST", "TOASTBERRY", "TOASTGRAPE", "TOASTNUTELLA", "TOASTPB"]):
            self.make_group('toast', (a, 0), f'acc_crafted{i}')

        for a, i in enumerate([
            "WINTERSTOAT", "BROWNSTOAT"]):
            self.make_group('stoats', (a, 0), f'acc_wild{i}')
        
        # Define scars
        scars_data = [
            ["ONE", "TWO", "THREE", "MANLEG", "BRIGHTHEART", "MANTAIL", "BRIDGE", "RIGHTBLIND", "LEFTBLIND",
             "BOTHBLIND", "BURNPAWS", "BURNTAIL"],
            ["BURNBELLY", "BEAKCHEEK", "BEAKLOWER", "BURNRUMP", "CATBITE", "RATBITE", "FROSTFACE", "FROSTTAIL",
             "FROSTMITT", "FROSTSOCK", "QUILLCHUNK", "QUILLSCRATCH"],
            ["TAILSCAR", "SNOUT", "CHEEK", "SIDE", "THROAT", "TAILBASE", "BELLY", "TOETRAP", "SNAKE", "LEGBITE",
             "NECKBITE", "FACE"],
            ["HINDLEG", "BACK", "QUILLSIDE", "SCRATCHSIDE", "TOE", "BEAKSIDE", "CATBITETWO", "SNAKETWO", "FOUR"]
        ]

        # define missing parts
        missing_parts_data = [
            ["LEFTEAR", "RIGHTEAR", "NOTAIL", "NOLEFTEAR", "NORIGHTEAR", "NOEAR", "HALFTAIL", "NOPAW", "TNR"]
        ]

        # scars 
        for row, scars in enumerate(scars_data):
            for col, scar in enumerate(scars):
                self.make_group('scars', (col, row), f'scars{scar}')

        # missing parts
        for row, missing_parts in enumerate(missing_parts_data):
            for col, missing_part in enumerate(missing_parts):
                self.make_group('missingscars', (col, row), f'scars{missing_part}')

        # accessories
        #to my beloved modders, im very sorry for reordering everything <333 -clay
        medcatherbs_data = [
            ["MAPLE LEAF", "HOLLY", "BLUE BERRIES", "FORGET ME NOTS", "RYE STALK", "CATTAIL", "POPPY", "ORANGE POPPY", "CYAN POPPY", "WHITE POPPY", "PINK POPPY"],
            ["BLUEBELLS", "LILY OF THE VALLEY", "SNAPDRAGON", "HERBS", "PETALS", "NETTLE", "HEATHER", "GORSE", "JUNIPER", "RASPBERRY", "LAVENDER"],
            ["OAK LEAVES", "CATMINT", "MAPLE SEED", "LAUREL", "BULB WHITE", "BULB YELLOW", "BULB ORANGE", "BULB PINK", "BULB BLUE", "CLOVER", "DAISY"]
        ]
        dryherbs_data = [
            ["DRY HERBS", "DRY CATMINT", "DRY NETTLES", "DRY LAURELS"]
        ]
        wild_data = [
            ["RED FEATHERS", "BLUE FEATHERS", "JAY FEATHERS", "GULL FEATHERS", "SPARROW FEATHERS", "MOTH WINGS", "ROSY MOTH WINGS", "MORPHO BUTTERFLY", "MONARCH BUTTERFLY", "CICADA WINGS", "BLACK CICADA"]
        ]

        collars_data = [
            ["CRIMSON", "BLUE", "YELLOW", "CYAN", "RED", "LIME"],
            ["GREEN", "RAINBOW", "BLACK", "SPIKES", "WHITE"],
            ["PINK", "PURPLE", "MULTI", "INDIGO"]
        ]

        bellcollars_data = [
            ["CRIMSONBELL", "BLUEBELL", "YELLOWBELL", "CYANBELL", "REDBELL", "LIMEBELL"],
            ["GREENBELL", "RAINBOWBELL", "BLACKBELL", "SPIKESBELL", "WHITEBELL"],
            ["PINKBELL", "PURPLEBELL", "MULTIBELL", "INDIGOBELL"]
        ]

        bowcollars_data = [
            ["CRIMSONBOW", "BLUEBOW", "YELLOWBOW", "CYANBOW", "REDBOW", "LIMEBOW"],
            ["GREENBOW", "RAINBOWBOW", "BLACKBOW", "SPIKESBOW", "WHITEBOW"],
            ["PINKBOW", "PURPLEBOW", "MULTIBOW", "INDIGOBOW"]
        ]

        nyloncollars_data = [
            ["CRIMSONNYLON", "BLUENYLON", "YELLOWNYLON", "CYANNYLON", "REDNYLON", "LIMENYLON"],
            ["GREENNYLON", "RAINBOWNYLON", "BLACKNYLON", "SPIKESNYLON", "WHITENYLON"],
            ["PINKNYLON", "PURPLENYLON", "MULTINYLON", "INDIGONYLON"]
        ]

        # medcatherbs
        for row, herbs in enumerate(medcatherbs_data):
            for col, herb in enumerate(herbs):
                self.make_group('medcatherbs', (col, row), f'acc_herbs{herb}')
        #dryherbs
        for row, dry in enumerate(dryherbs_data):
            for col, dryherbs in enumerate(dry):
                self.make_group('medcatherbs', (col, 3), f'acc_herbs{dryherbs}')     
        # wild
        for row, wilds in enumerate(wild_data):
            for col, wild in enumerate(wilds):
                self.make_group('wild', (col, 0), f'acc_wild{wild}')

        # collars
        for row, collars in enumerate(collars_data):
            for col, collar in enumerate(collars):
                self.make_group('collars', (col, row), f'collars{collar}')

        # bellcollars
        for row, bellcollars in enumerate(bellcollars_data):
            for col, bellcollar in enumerate(bellcollars):
                self.make_group('bellcollars', (col, row), f'collars{bellcollar}')

        # bowcollars
        for row, bowcollars in enumerate(bowcollars_data):
            for col, bowcollar in enumerate(bowcollars):
                self.make_group('bowcollars', (col, row), f'collars{bowcollar}')

        # nyloncollars
        for row, nyloncollars in enumerate(nyloncollars_data):
            for col, nyloncollar in enumerate(nyloncollars):
                self.make_group('nyloncollars', (col, row), f'collars{nyloncollar}')

    def load_symbols(self):
        """
        loads clan symbols
        """

        if os.path.exists('resources/dicts/clan_symbols.json'):
            with open('resources/dicts/clan_symbols.json') as read_file:
                self.symbol_dict = ujson.loads(read_file.read())

        # U and X omitted from letter list due to having no prefixes
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                   "V", "W", "Y", "Z"]

        # sprite names will format as "symbol{PREFIX}{INDEX}", ex. "symbolSPRING0"
        y_pos = 1
        for letter in letters:
            x_mod = 0
            for i, symbol in enumerate([symbol for symbol in self.symbol_dict if
                                        letter in symbol and self.symbol_dict[symbol]["variants"]]):
                if self.symbol_dict[symbol]["variants"] > 1 and x_mod > 0:
                    x_mod += -1
                for variant_index in range(self.symbol_dict[symbol]["variants"]):
                    x_pos = i + x_mod

                    if self.symbol_dict[symbol]["variants"] > 1:
                        x_mod += 1
                    elif x_mod > 0:
                        x_pos += - 1

                    self.clan_symbols.append(f"symbol{symbol.upper()}{variant_index}")
                    self.make_group('symbols',
                                    (x_pos, y_pos),
                                    f"symbol{symbol.upper()}{variant_index}",
                                    sprites_x=1, sprites_y=1, no_index=True)

            y_pos += 1

    def dark_mode_symbol(self, symbol):
        """Change the color of the symbol to dark mode, then return it
        :param Surface symbol: The clan symbol to convert"""
        dark_mode_symbol = copy(symbol)
        var = pygame.PixelArray(dark_mode_symbol)
        var.replace((87, 76, 45), (239, 229, 206))
        del var
        # dark mode color (239, 229, 206)
        # debug hot pink (255, 105, 180)

        return dark_mode_symbol

# CREATE INSTANCE
sprites = Sprites()

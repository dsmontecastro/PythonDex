import pyglet as p
from get_file import get_file

from . import processes
from .colors import Color


class InformationPanel:
    def __init__(
        self,
        data,
    ):
        self.data = data
        self.front = p.graphics.Batch()
        self.back = p.graphics.Batch()
        self.initialize_components()

    def initialize_components(self):
        # Load pokemon data to display
        self.index = self.data.index
        self.name = self.data.name
        self.type_1 = self.data.type1
        self.type_2 = self.data.type2

        # Load initial type 1 and 2 background images and sprites
        self.background_1_image = p.image.load(
            get_file("resources/backgrounds/{}.png".format(self.type_1))
        )

        # Check if type_2 is a string or a NaN float
        if isinstance(self.type_2, str):
            self.background_2_image = p.image.load(
                get_file("resources/backgrounds/{}.png".format(self.type_2))
            )
        else:
            self.background_2_sprite.image = p.image.load(
                get_file("resources/backgrounds/blank.png")
            )

        self.background_1_sprite = p.sprite.Sprite(
            self.background_1_image, batch=self.back
        )
        self.background_2_sprite = p.sprite.Sprite(
            self.background_2_image, batch=self.back
        )
        self.background_2_sprite.opacity = 150
        self.background_2_sprite.rotate = 180

        # Load initial pokemon image and sprite
        # Attempt to load jpg version if it exists
        # else, load png version
        try:
            self.pokemon_image = p.image.load(
                get_file("resources/pokemon/{}.jpg".format(self.name.lower()))
            )
        except FileNotFoundError:
            pass
        try:
            self.pokemon_image = p.image.load(
                get_file("resources/pokemon/{}.png".format(self.name.lower()))
            )
        except FileNotFoundError:
            raise FileNotFoundError("Invalid pokemon name.")
        self.pokemon_image.anchor_x = self.pokemon_image.width
        self.pokemon_sprite = p.sprite.Sprite(
            self.pokemon_image,
            self.background_1_sprite.width,
            self.background_1_sprite.width,
            batch=self.front,
        )

        # Load labels
        self.label_name = p.text.Label(
            "Name: {}".format(self.data.name),
            font_name="Power Clear",
            x=30,
            y=440,
            font_size=15,
            batch=self.front,
        )
        self.label_abilities = p.text.Label(
            "Abilities: {}".format(self.data.abilities),
            font_name="Power Clear",
            x=30,
            y=420,
            font_size=12,
            batch=self.front,
        )
        self.label_weight = p.text.Label(
            "WT: {} kg".format(self.data.weight),
            font_name="Power Clear",
            x=30,
            y=400,
            font_size=12,
            batch=self.front,
        )
        self.label_height = p.text.Label(
            "HT: {} m".format(self.data.height),
            font_name="Power Clear",
            x=30,
            y=380,
            font_size=12,
            batch=self.front,
        )

        self.width = self.background_1_image.width
        self.height = self.background_1_image.height

        self.hexagon_image = p.image.load(get_file("resources/tiles/stat_wheel.png"))
        self.hexagon_image.anchor_x = int(self.hexagon_image.width / 2)
        self.hexagon_image.anchor_y = int(self.hexagon_image.height / 2)
        self.hexagon_sprite = p.sprite.Sprite(
            self.hexagon_image,
            self.background_1_sprite.width / 2,
            self.hexagon_image.height / 2 + 25,
            batch=self.front,
        )

        self.stats_image = p.image.load(get_file("resources/tiles/stat_names.png"))
        self.stats_image.anchor_x = int(self.stats_image.width / 2) + 10
        self.stats_image.anchor_y = int(self.stats_image.height / 2)
        self.stats_sprite = p.sprite.Sprite(
            self.stats_image,
            self.hexagon_sprite.x,
            self.hexagon_sprite.y,
            batch=self.front,
        )

        self.stats = [
            self.data.hp,
            self.data.attack,
            self.data.defense,
            self.data.speed,
            self.data.sp_defense,
            self.data.sp_attack,
        ]
        self.current_stats = processes.vertex_create(
            self.stats, self.hexagon_sprite.x, self.hexagon_sprite.y
        )
        self.previous_stats = self.current_stats

    def update_background_sprite(self):
        # Replace type_1 sprite background image
        self.background_1_sprite.image = p.image.load(
            get_file("resources/backgrounds/{}.png".format(self.type_1))
        )

        # Check if type_2 is a string or a NaN float
        # Made as an artifact of using pandas for data loading
        if isinstance(self.type_2, str):
            self.background_2_sprite.image = p.image.load(
                get_file("resources/backgrounds/{}.png".format(self.type_2))
            )
        else:
            self.background_2_sprite.image = p.image.load(
                get_file("resources/backgrounds/blank.png")
            )

    def update_pokemon_sprite(self):
        try:
            self.pokemon_image = p.image.load(
                get_file("resources/pokemon/{}.jpg".format(self.data.name.lower()))
            )
        except FileNotFoundError:
            pass
        try:
            self.pokemon_image = p.image.load(
                get_file("resources/pokemon/{}.png".format(self.data.name.lower()))
            )
        except FileNotFoundError:
            pass
        self.pokemon_image.anchor_x = self.pokemon_image.width
        self.pokemon_sprite.image = self.pokemon_image

    def update_labels(self):
        self.label_name.text = "Name: {}".format(self.data.name)
        self.label_abilities.text = "Abilities: {}".format(self.data.abilities)
        self.label_weight.text = "WT: {} kg".format(self.data.weight)
        self.label_height.text = "HT: {} m".format(self.data.height)

    def update(self, data):
        self.data = data
        self.index = data.index
        self.name = data.name
        self.type_1 = data.type1
        self.type_2 = data.type2
        self.stats = [
            data.hp,
            data.attack,
            data.defense,
            data.speed,
            data.sp_defense,
            data.sp_attack,
        ]
        self.current_stats = processes.vertex_create(
            self.stats, self.hexagon_sprite.x, self.hexagon_sprite.y
        )

        self.update_background_sprite()
        self.update_pokemon_sprite()
        self.update_labels()

    def draw_self(self):
        self.back.draw()
        self.front.draw()
        p.graphics.draw(
            4,
            p.gl.GL_QUADS,
            (
                "v2f",
                (
                    self.background_1_sprite.width,
                    self.background_1_sprite.y,
                    self.background_1_sprite.width,
                    self.background_1_sprite.height,
                    640,
                    self.background_1_sprite.height,
                    640,
                    self.background_1_sprite.y,
                ),
            ),
            ("c3B", Color.BLACK * 4),
        )


class Browser:
    def __init__(self, database, favorites, x, y):
        self.database = database
        self.favorites = favorites
        self.back = p.graphics.Batch()
        self.front = p.graphics.Batch()

        # Preload image tiles
        self.select_active_image = p.image.load(get_file("resources/tiles/select_active.png"))
        self.select_active_image.anchor_x = self.select_active_image.width // 2
        self.select_active_image.anchor_y = self.select_active_image.height // 2
        self.select_inactive_image = p.image.load(get_file("resources/tiles/select_inactive.png"))
        self.select_inactive_image.anchor_x = self.select_inactive_image.width // 2
        self.select_inactive_image.anchor_y = self.select_inactive_image.height // 2
        self.star_active_image = p.image.load(get_file("resources/tiles/fav_active.png"))
        self.star_active_image.anchor_x = self.star_active_image.width // 2
        self.star_active_image.anchor_y = self.star_active_image.height // 2
        self.star_inactive_image = p.image.load(get_file("resources/tiles/fav_inactive.png"))
        self.star_inactive_image.anchor_x = self.star_inactive_image.width // 2
        self.star_inactive_image.anchor_y = self.star_inactive_image.height // 2

        # Set states
        if len(database) >= 10:
            self.cycle_max = 10
        else:
            self.cycle_max = len(database)
        self.index = 0
        self.top = self.index
        self.selected = self.index
        self.bottom = self.index + self.cycle_max - 1
        self.offset = 40
        self.tiles = []
        self.tile_pos = (x + 2.5 * self.offset, y, self.offset)
        self.texts = []
        self.text_pos = (x + 30, y, self.offset)
        self.stars = []
        self.star_pos = (x, y, self.offset)

        for i in range(self.cycle_max):
            self.tiles.append(
                p.sprite.Sprite(
                    self.select_inactive_image,
                    batch=self.back,
                    x=self.tile_pos[0],
                    y=self.tile_pos[1] - self.tile_pos[2] * i,
                )
            )
            self.stars.append(
                p.sprite.Sprite(
                    self.star_inactive_image,
                    batch=self.back,
                    x=self.star_pos[0],
                    y=self.star_pos[1] - self.star_pos[2] * i,
                )
            )
            self.stars[i].scale = self.tiles[i].height / self.stars[i].height
            if self.bottom < self.cycle_max - 1:
                target_fav = i
            else:
                target_fav = self.top + i
            if self.database[target_fav].index in self.favorites:
                self.stars[i].color = Color.GREY
            else:
                self.stars[i].color = Color.WHITE
            self.texts.append(
                p.text.Label(
                    "{} - {}".format(
                        processes.add0(self.database[i].index + 1), self.database[i].name
                    ),
                    batch=self.front,
                    x=self.text_pos[0],
                    font_size=15,
                    y=self.text_pos[1] - self.text_pos[2] * i,
                    anchor_y="center",
                    font_name="Power Clear",
                    color=Color.BLACK + tuple([255]),
                )
            )

        # setting the first items as the "selector"
        self.tiles[0].image = self.select_active_image
        self.texts[0].color = Color.WHITE + tuple([255])

    def update_data(self, shift):
        if shift >= self.cycle_max or shift <= -self.cycle_max:
            # Shift entire list and selector
            self.top += shift
            self.index += shift
            self.bottom += shift
        elif self.index != self.bottom and shift > 0:
            self.index += shift
            self.selected += shift
        elif self.index != self.top and shift < 0:
            self.index += shift
            self.selected += shift
        elif self.index == self.top and shift < 0:
            self.top += shift
            self.index += shift
            self.bottom += shift
        elif self.index == self.bottom and shift > 0:
            self.top += shift
            self.index += shift
            self.bottom += shift

        if self.top < 0:
            self.top = len(self.database) + self.top
        if self.top > len(self.database) - 1:
            self.top = self.top - len(self.database)
        if self.bottom > len(self.database) - 1:
            self.bottom = self.bottom - len(self.database)
        if self.bottom < 0:
            self.bottom = len(self.database) + self.bottom
        if self.selected < 0:
            self.selected = 0
        if self.selected > self.cycle_max - 1:
            self.selected = self.cycle_max - 1
        if self.index > len(self.database) - 1:
            self.index = self.index - len(self.database)
        if self.index < 0:
            self.index = len(self.database) + self.index

        target_database = []
        if self.bottom < self.top:
            target_database = target_database + self.database[self.top :]
            target_database = target_database + self.database[0 : self.bottom + 1]
        elif self.top > self.bottom and self.bottom < self.cycle_max:
            target_database = target_database + self.database[self.bottom :]
            target_database = target_database + self.database[: self.top]
        else:
            target_database = (
                target_database + self.database[self.top : self.bottom + 1]
            )

        for i in range(len(target_database)):
            self.texts[i].text = "{} - {}".format(
                processes.add0(target_database[i].index), target_database[i].name
            )

            target_fav = self.top + i
            if target_fav > len(self.database) - 1:
                target_fav = target_fav - len(self.database)
            if self.database[target_fav].index in self.favorites:
                self.stars[i].color = Color.GREY
            else:
                self.stars[i].color = Color.WHITE
            if i == self.selected:
                self.tiles[i].image = self.select_active_image
                self.texts[i].color = Color.WHITE + tuple([255])
            else:
                self.tiles[i].image = self.select_inactive_image
                self.texts[i].color = Color.BLACK + tuple([255])
            self.tiles[i].visible = True
            self.stars[i].visible = True

        return self.index

    def clear_browser(self):
        for text in self.texts:
            text.text = ""
        for sprite in self.tiles:
            sprite.visible = False
        for star in self.stars:
            star.visible = False

    def update_favs(self):
        if self.index in self.favorites:
            self.favorites.remove(self.index)
            self.stars[self.selected].color = Color.WHITE
        else:
            self.favorites.append(self.index)
            self.stars[self.selected].color = Color.GREY

    def update_database(self, database):
        self.database = database

        if len(database) >= 10:
            self.cycle_max = 10
        else:
            self.cycle_max = len(self.database)
        self.index = 0
        self.top = self.index
        self.selected = self.index
        self.bottom = self.index + self.cycle_max - 1
        self.clear_browser()
        self.update_data(0)

    def draw_self(self):
        self.back.draw()
        self.front.draw()


class SearchPanel:
    def __init__(self, database, x, y):
        self.front = p.graphics.Batch()
        self.back = p.graphics.Batch()
        self.database = database
        self.search_string = ""
        self.label = p.text.Label(
            text="Search...",
            font_name="Power Clear",
            font_size=14,
            x=380,
            y=440,
            batch=self.front,
            color=Color.BLACK + tuple([255]),
            anchor_x="left",
            anchor_y="center",
        )

        self.field_image = p.image.load(get_file("resources/tiles/select_inactive.png"))
        self.field_image.anchor_x = self.field_image.width // 2
        self.field_image.anchor_y = self.field_image.height // 2
        self.field = p.sprite.Sprite(
            self.field_image,
            batch=self.back,
            x=450,
            y=440,
        )

    def draw_self(self):
        self.back.draw()
        self.front.draw()

    def handle_backspace(self):
        self.search_string = self.search_string[:-1]
        self.label.text = self.search_string

    def handle_char(self, key):
        if len(self.search_string) < 15:
            self.search_string += key.lower()
            self.search_string = self.search_string.capitalize()
            self.label.text = self.search_string

    def handle_enter(self):
        stats = ["hp", "attack", "defense", "speed", "sp_defense", "sp_attack"]
        types = [
            "bug",
            "dark",
            "dragon",
            "electric",
            "fairy",
            "fight",
            "fire",
            "flying",
            "ghost",
            "grass",
            "ground",
            "ice",
            "normal",
            "poison",
            "psychic",
            "rock",
            "steel",
            "water",
        ]
    
        if self.search_string == "": return self.database

        strings = self.search_string.split(" ")
        mode = strings[0].lower()

        if mode == "legendary":
            self.query = self.database.filter_by_legendary(True)
        elif mode == "common":
            self.query = self.database.filter_by_legendary(False)
    
        elif mode in types:
            type_1, type_2 = mode, "none"
            if len(strings) > 1: type_2 = strings[-1].lower()
            self.query = self.database.filter_by_type(type_1, type_2)
    
        elif mode in stats:
            stat, value = mode, 0
            if len(strings) > 1: value = int(strings[-1])
            self.query = self.database.filter_by_stat(mode, value)
        
        else: self.query = self.database.filter_by_name(self.search_string)


        if self.query != None and not self.query.isempty():
            return self.query
        else:
            self.label.text = "No results..."
            return self.database


class ScrollBar:
    def __init__(self, database, up=0, down=0, left=0, right=0):
        self.square = (right, up, right, down, left, down, left, up)
        self.width = right - left
        self.height = up - down
        self.maximum = up
        self.minimum = down
        self.ratio = len(database) / self.height
        self.bar_img = p.image.load(get_file("resources/tiles/scroll_bar.png"))
        self.bar_img.anchor_x = int(self.bar_img.width / 2)
        self.bar_img.anchor_y = int(self.bar_img.height / 2)
        self.bar = p.sprite.Sprite(self.bar_img, x=right - self.width / 2, y=up)

    def update_from_scroll(self, dy):
        self.bar.y += dy
        if self.bar.y > self.maximum:
            self.bar.y = self.minimum
        elif self.bar.y < self.minimum:
            self.bar.y = self.maximum

    def update_from_key(self, top):
        self.bar.y = int(self.maximum - ((top + 5) / self.ratio))

    def update_database(self, database):
        self.ratio = len(database) / self.height

    def draw_self(self):
        p.graphics.draw(4, p.gl.GL_QUADS, ("v2f", self.square), ("c3B", Color.GREY * 4))
        self.bar.draw()

import pyglet as p
from pyglet.window import key
from interface.processes import vertex_change

from get_file import get_file
from database.fav import Favorites
from database.database import Database

from interface.colors import Color
from interface.panels import InformationPanel, Browser, SearchPanel, ScrollBar

# Get resources
width = 640
height = 480
current_pokemon = 0
database = Database()
favorites = Favorites()
p.font.add_file(get_file("resources/fonts/pkmndp.ttf"))

# Initialize windows
config = p.gl.Config(sample_buffers=1, samples=8, double_buffer=True)
window = p.window.Window(caption='PythonDex', width=width, height=height, config=config)

# Set blending modes
p.gl.glEnable(p.gl.GL_BLEND)
p.gl.glBlendFunc(p.gl.GL_SRC_ALPHA, p.gl.GL_ONE_MINUS_SRC_ALPHA)

information = InformationPanel(database.index(current_pokemon))
browser = Browser(database, favorites, x=information.width+30, y=window.height-90)
search_panel = SearchPanel(database, x=information.width+30, y=window.height+15)
scroll_bar = ScrollBar(database, window.height-80, 30, window.width-30, window.width-20)

previous_stats = information.current_stats
scroll_state   = False

def update_hexagon(dt):
    global previous_stats
    previous_stats = vertex_change(previous_stats, information.current_stats)

def update_information_panel(dt):
    information.update(database[0])

def update_scroll(dt):
    global current_pokemon
    if (dt != 0):
        prev = current_pokemon
        current_pokemon = browser.update_data(dt)
        if (current_pokemon != prev):
            information.update(database.index(current_pokemon))

key_shifts = {key.DOWN: 1, key.UP: -1, key.RIGHT: 10, key.LEFT: -10, key.PAGEDOWN: 50, key.PAGEUP: -50}

@window.event
def on_key_press(symbol, mod):
    global database, browser, previous_stat
    if symbol in key_shifts:
        scroll_bar.update_from_key(browser.top)
        update_scroll(key_shifts[symbol])
    elif symbol == key.TAB:
        browser.update_favs()
    elif symbol == key.BACKSPACE:
        search_panel.handle_backspace()
    elif symbol == key.ENTER:
        database = search_panel.handle_enter()
        current_pokemon = database.first().index
        information.update(database.first())
        browser.update_database(database)
    elif symbol == key.SPACE:
        search_panel.handle_char(" ")

    else:
        char = chr(symbol)
        if str.isalnum(char):
            search_panel.handle_char(char)

@window.event
def on_mouse_scroll(x, y, dx, dy):
    scroll_bar.update_from_key(browser.top)
    update_scroll(int(-dy))

@window.event
def on_mouse_drag(x, y, dx, dy, button, modifier):
    global scroll_state
    if scroll_bar.bar.x - scroll_bar.bar.width/2 <= x <= scroll_bar.bar.x + scroll_bar.bar.width/2:
        if scroll_bar.bar.y - scroll_bar.bar.height/2 <= y <= scroll_bar.bar.y + scroll_bar.bar.height/2:
            scroll_state = True
    if scroll_state:
        check = int(scroll_bar.bar.y + dy)
        if  scroll_bar.minimum < check < scroll_bar.maximum:
            scroll_bar.update_from_scroll(dy)
            shift = int(len(database)-(dy*scroll_bar.ratio))
            update_scroll(shift)

@window.event
def on_mouse_release(x, y, button, modifier):
    global scroll_state
    if scroll_state: scroll_state = False

@window.event
def on_draw():
    window.clear()
    information.draw_self()
    browser.draw_self()
    search_panel.draw_self()
    scroll_bar.draw_self()
    vertices = [information.hexagon_sprite.x, information.hexagon_sprite.y] + previous_stats
    p.graphics.draw_indexed(7, p.gl.GL_TRIANGLES,
                            [0, 6, 1, 0, 1, 2, 0, 2, 3, 0, 3, 4, 0, 4, 5, 0, 5, 6],
                            ('v2f', tuple(vertices)), ('c4B', (Color.WHITE + tuple([150])) * 7))
    p.graphics.draw(6, p.gl.GL_LINE_LOOP, ('v2f', previous_stats), ('c3B', (Color.BLACK* 6)))

if __name__ == "__main__":
    p.clock.schedule_interval(update_hexagon, 1/120.0)
    p.app.run()

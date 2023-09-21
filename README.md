# PythonDex (Prototype)

![Screenshot](https://dsmontecastro.github.io/Portfolio/pythondex.png)

## Description
__Made in conjunction with fellow groupmates Jose Salinas and Matthew Menorca, A.Y. 2018.__
A Pokedex application, serving as our 2nd machine project for our 1st Semester. My main role in this task was to create the logic for the GUI, connecting both the assets and database elements made by my teammates.

The app was developed through _Python_, making use of _Pyglet_ for its GUI. It loads resources from CSV files, with Pandas as an intermediary. This was a prototype design made in the span of around 1 month,
and serves as a basis for one of my personal projects.


#### <ins>UPDATE (2023) </ins>

The app works with the latest versions of most packages in the _requirements_ file as of Aug. 2023. However, this excludes _Pyglet_, as it has deprecated some functions and features from the application's version (1.5).

## Installation
Install the necessary dependencies in _requirements.txt_. Afterwards, the app can be opened through running __main.py__ via the standard python run command, e.g. `py main.py`.

A simple executable made with _PyInstaller_ is also available.

## Controls
The scrollbar can be controlled by via the mousewheel, directional inputs, and the page up & down keys.

Press `TAB` to mark the currently selected Pokemon as a __favorite__.

Type in any alphanumeric character to fill in the searchbar above.
`BACKSPACE` will erase the last character, and `ENTER` to initiate the __search__. Aside from the Pokemon's __name__, users can also type in the followin search keys:

* __Common__ - lists the known non-legendary pokemon.
* __Legendary__ - lists the known legendary pokemon.
* _Types_ - input any type or pair of to search for matching Pokemon.
* _Stats_ - input any stat plus an optional number (default 0) to search for a descending list of Pokemon with at least that base-stat value.
  > Note: The __special__ stats are _sp\_attack_ or _sp\_defense_.

Use `ESCAPE` or close the window to quit the program.
from kivy.core.text import LabelBase
import os

FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'MaokenAssortedSans.ttf')

LabelBase.register(name='Maoken', fn_regular=FONT_PATH)

FONT = {
    "family": "Maoken",
    "size": 18
}

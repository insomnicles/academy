from beautifiers.html.easy import EasyBeautifier
from beautifiers.tex.simple import SimpleBeautifier

class BeautifierFactory():
    def create(self, theme):
        if theme == 'easy':
            return EasyBeautifier()
        elif theme == 'simple':
            return SimpleBeautifier()
        else:
            raise Exception("Extractor for theme " + theme + " not found.")
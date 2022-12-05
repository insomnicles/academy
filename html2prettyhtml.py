from src.converters.beautify import Beautifier
from src.converters.extractors import Extractor
from src.converters.extractors import GuttenbergDialogueExtractor
from src.converters.extractors import GuttenbergPoemExtractor

import os
import sys
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import urlparse
from urlextract import URLExtract
from pprint import pprint

class Html2PrettyHtml:
    src_file, src_filename, src_dir, src_url, output_dir = "", "", "", "", ""

    src_file = ""
    src_dir = ""
    src_filename = ""
    src_url = ""
    src_html = ""
    output_dir = ""

    structured_doc = None

    def convert(self, source, source_type, source_work, theme, output_dir):
        print("\n------------------\nProcessing " + source_work)

        try:
            self.set_source_info(source_work)
            self.get_source_html()
            print("Source set successfully")
        except HTTPError as http_error:
            print("Error: could not convert url: HTTPError")
            return
        except URLError as url_error:
            print("Error: could not convert url: URL Error: Server Not Found")
            return
        except OSError as e:
            print("Error: could not convert file/url: file/url not found or not readable\n")
            return
        except Exception:
            print("Error: could not Convert File" + str(e.code) + "\n")
            return

        try:
            #ext = Extractor(source, source_type)
            if (source == "guttenberg" and source_type == "dialogue"):
                ext = GuttenbergDialogueExtractor()
            elif (source == "guttenberg" and source_type == "poem"):
                ext = GuttenbergPoemExtractor()
            else:
                raise Exception("could not find a suitable extractor")

            ext.set_html(self.src_html)
            self.structured_doc = ext.extract()
            print(self.structured_doc)
            print("Extracted File Successfully\n")
        except Exception as e:
            print("Error: could not extract data from source file/url\n")
            # pprint(vars(bc))
            return

        print(self.structured_doc)
        #pprint(vars(bc))
        #print(structured_doc)
        try:
            if (theme == "velvet"):
                crt = Beautifier(source_type)
            elif (theme == "sunny"):
                crt = Beautifier(source_type)
            else:
                raise Exception("Theme " + theme + " was not recognized.")

            crt.create(self.structured_doc)
            print(output_dir + self.src_filename)
            crt.save(output_dir + "/" + self.src_filename)
        except Exception:
            print("Error: could not beautify document data")
            print(sys.exc_info())
            return

        self.reset()

    def set_source_info(self, source_work):

        urls = URLExtract().find_urls(source_work)
        if urls:
            self.src_url = urls[0]
            self.src_filename = urls[0].split("/")[-1]
        else:
            self.src_file = source_work.strip()
            self.src_dir = os.path.dirname(source_work) + "/"
            self.src_filename = os.path.basename(source_work)

    def get_source_html(self):
        html = ""
        if self.src_url != "":
            f = urlopen(self.src_url)
        else:
            f = open(self.src_file, "rb")
        if not f:
            raise Exception("Html not found")
        html = f.read()
        f.close()
        self.src_html = html

    def reset(self):
        self.src_file, self.src_filename, self.src_dir, self.src_url, self.output_dir = "", "", "", "", ""
        self.src_html = ""
        self.structured_doc = None

source_plato= "./src/books/guttenberg/plato"
source_aristotle="./src/books/guttenberg/aristotle"
source_sophocles="./src/books/guttenberg/sophocles"

plato_files = {
    # Plato
    # "alcibiadesI":  source_plato + "/plato-alcibiadesI-tr-jowett-guttenberg-modified.html",     # **Using Modified Gutenberg Source: original missing toc markup
    # "alcibiadesII": source_plato + "/plato-alcibiadesII-tr-jowett-guttenberg.html",             # MINOR: no marcel.tr tag
    # "apology":      source_plato + "/plato-apology-tr-jowett-guttenberg.html",                  #
    # "charmides":    source_plato + "/plato-charmides-tr-jowett-guttenberg.html",                #
    # "cratylus":     source_plato + "/plato-cratylus-tr-jowett-guttenberg.html",                 # Minor: translator in par; descriptions not parsed; add footnotes
    # "crito":        source_plato + "/plato-crito-tr-jowett-guttenberg-modified.html",                    # ERROR: original missing toc markup
    # "critias":      source_plato + "/plato-critias-tr-jowett-guttenberg.html",                  #
    # "euthydemus":   source_plato + "/plato-euthydemus-tr-jowett-guttenberg.html",               #
    # "euthyphro":    source_plato + "/plato-euthyphro-tr-jowett-guttenberg.html",                #
    # "eryxias":      source_plato + "/plato-eryxias-tr-jowett-guttenberg.html",                  #
    # "gorgias":      source_plato + "/plato-gorgias-tr-jowett-guttenberg.html",                  #
    # "ion":          source_plato + "/plato-ion-tr-jowett-guttenberg.html",                      #
    # "laches":       source_plato + "/plato-laches-tr-jowett-guttenberg.html",                   # Minor: PERSONS in TOC
    # "laws":         source_plato + "/plato-laws-tr-jowett-guttenberg.html",                     #
    # "lesser-hippias": source_plato + "/plato-lesser-hippias-tr-jowett-guttenberg-modified.html",# ERROR: original missing toc markup
    # "lysis":        source_plato + "/plato-lysis-tr-jowett-guttenberg.html",                    # Minor: PERSONS toc entry
    # "menexenus":    source_plato + "/plato-menexenus-tr-jowett-guttenberg.html",                # Minor: PERSONS toc entry
    "meno":           source_plato + "/plato-meno-tr-jowett-guttenberg.html",                     #
    "notplato":       source_plato + "/notplato.html",                     #
    # "parmenides":   source_plato + "/plato-parmenides-tr-jowett-guttenberg.html",               #
    # "phaedo":       source_plato + "/plato-phaedo-tr-jowett-guttenberg.html",                   # Minor: PERSONS OF THE DIALOGUE in dialogue para
    # "phaedrus":     source_plato + "/plato-phaedrus-tr-jowett-guttenberg.html",                 #
    # "philebus":     source_plato + "/plato-philebus-tr-jowett-guttenberg.html",                 #
    # "protagoras":   source_plato + "/plato-protagoras-tr-jowett-guttenberg.html",               #
    # "republic":     source_plato + "/plato-republic-tr-jowett-guttenberg.html",                 # Minor: PERSONS in toc
    # "sophist":      source_plato + "/plato-sophist-tr-jowett-guttenberg.html",                  #
    # "statesman":    source_plato + "/plato-statesman-tr-jowett.html",                           #
    # "symposium":    source_plato + "/plato-symposium-tr-jowett-guttenberg.html",                #
    # "timaeus":      source_plato + "/plato-timaeus-tr-jowett-guttenberg.html",                  #
    # "theaetetus":   source_plato + "/plato-theaetetus-tr-jowett-guttenberg.html",               #
}

plato_urls = {
    # Plato
    # "alcibiadesI":  source_plato + "/plato-alcibiadesI-tr-jowett-guttenberg-modified.html",     # **Using Modified Gutenberg Source: original missing toc markup
    # "alcibiadesII": source_plato + "/plato-alcibiadesII-tr-jowett-guttenberg.html",             # MINOR: no marcel.tr tag
    # "apology":      source_plato + "/plato-apology-tr-jowett-guttenberg.html",                  #
    # "charmides":    source_plato + "/plato-charmides-tr-jowett-guttenberg.html",                #
    # "cratylus":     source_plato + "/plato-cratylus-tr-jowett-guttenberg.html",                 # Minor: translator in par; descriptions not parsed; add footnotes
    # "crito":        source_plato + "/plato-crito-tr-jowett-guttenberg-modified.html",                    # ERROR: original missing toc markup
    # "critias":      source_plato + "/plato-critias-tr-jowett-guttenberg.html",                  #
    # "euthydemus":   source_plato + "/plato-euthydemus-tr-jowett-guttenberg.html",               #
    # "euthyphro":    source_plato + "/plato-euthyphro-tr-jowett-guttenberg.html",                #
    # "eryxias":      source_plato + "/plato-eryxias-tr-jowett-guttenberg.html",                  #
    # "gorgias":      source_plato + "/plato-gorgias-tr-jowett-guttenberg.html",                  #
    "ion":          "https://www.gutenberg.org/cache/epub/1635/pg1635-images.html",                      #
    # "laches":       source_plato + "/plato-laches-tr-jowett-guttenberg.html",                   # Minor: PERSONS in TOC
    # "laws":         source_plato + "/plato-laws-tr-jowett-guttenberg.html",                     #
    # "lesser-hippias": source_plato + "/plato-lesser-hippias-tr-jowett-guttenberg-modified.html",# ERROR: original missing toc markup
    # "lysis":        source_plato + "/plato-lysis-tr-jowett-guttenberg.html",                    # Minor: PERSONS toc entry
    # "menexenus":    source_plato + "/plato-menexenus-tr-jowett-guttenberg.html",                # Minor: PERSONS toc entry
    #"meno":         "https://www.gutenberg.org/cache/epub/1643/pg1643-images.html",                     #
    "notplato":         "https://www.asdflasdfasdf.com/1.html",                     #
    # "parmenides":   source_plato + "/plato-parmenides-tr-jowett-guttenberg.html",               #
    # "phaedo":       source_plato + "/plato-phaedo-tr-jowett-guttenberg.html",                   # Minor: PERSONS OF THE DIALOGUE in dialogue para
    # "phaedrus":     source_plato + "/plato-phaedrus-tr-jowett-guttenberg.html",                 #
    # "philebus":     source_plato + "/plato-philebus-tr-jowett-guttenberg.html",                 #
    # "protagoras":   source_plato + "/plato-protagoras-tr-jowett-guttenberg.html",               #
    # "republic":     source_plato + "/plato-republic-tr-jowett-guttenberg.html",                 # Minor: PERSONS in toc
    # "sophist":      source_plato + "/plato-sophist-tr-jowett-guttenberg.html",                  #
    # "statesman":    source_plato + "/plato-statesman-tr-jowett.html",                           #
    # "symposium":    source_plato + "/plato-symposium-tr-jowett-guttenberg.html",                #
    # "timaeus":      source_plato + "/plato-timaeus-tr-jowett-guttenberg.html",                  #
    # "theaetetus":   source_plato + "/plato-theaetetus-tr-jowett-guttenberg.html",               #
}


aristotle = {
    # Aristotle
    "athenian-constitution":source_aristotle + "/aristotle-the-athenian-constitution-tr-kenyon-guttenberg.html",       #
    "categories":           source_aristotle + "/aristotle-the-categories-tr-edghill-guttenberg.html",                 #
    "nico-ethics":          source_aristotle + "/aristotle-the-nicomachean-ethics-tr-smith-ja-guttenberg.html",        #
    "poetics-bywater":      source_aristotle + "/aristotle-on-the-art-of-poetry-tr-bywater-guttenberg.html",           #
    "poetics-butcher":      source_aristotle + "/aristotle-the-poetics-tr-butcher-guttenberg.html",                    #
    "treatise-on-government":source_aristotle + "/aristotle-treatise-on-government-tr-ellis-guttenberg.html",          #
}

sophocles = {
    "sophocles": source_sophocles + "/sophocles-seven-plays.html"
}

bc = Html2PrettyHtml()
for dialogue in plato_files:
    bc.convert("guttenberg", "dialogue", plato_files[dialogue], "velvet" "output/guttenberg/plato")
    #pprint(vars(bc))
for url in plato_urls:
    bc.convert("guttenberg", "dialogue", plato_urls[url], "summer", "output/guttenberg/plato")
    #pprint(vars(bc))

# for book in aristotle:
#    bc.convert("guttenberg", "book", book, "output/guttenberg/aristotle")

# for poem in sophocles:
#    bc.convert("guttenberg", "poem", poem, "output/guttenberg/sophocles")

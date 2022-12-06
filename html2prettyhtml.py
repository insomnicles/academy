from prettifier import EasyPrettifier
from extractors import GutenbergExtractor

from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen
from urllib.parse import urlparse
import time
import os
class Html2PrettyHtml:
    DEBUG = False

    source, source_work, theme, output_dir = "", "", "", ""
    structured_doc = None

    def convert(self, source, source_work, theme, output_dir):
        print("\n------------------\nProcessing " + source_work)
        self.source = source
        self.source_work = source_work
        self.theme = theme
        self.output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"

        try:
            if (source == "gutenberg"):
                ext = GutenbergExtractor(source_work, self.output_dir)
            else:
                raise Exception("Could not find a suitable extractor")
            self.structured_doc = ext.extract()
            del ext
            print("Extracted File Successfully\n") if self.DEBUG else True
        except HTTPError as http_error:
            print("Error: could not convert url: " + source_work + " HTTPError")
            self.reset()
            return
        except URLError as url_error:
            print("Error: could not convert url:" + source_work + " URL Error: Server Not Found")
            self.reset()
            return
        except OSError as e:
            print("Error: could not convert file/url: " + source_work + ": file/url not found or not readable\n")
            self.reset()
            return
        except Exception as e:
            print("Error: could not extract data from source file/url\n")
            print(e)
            self.reset()
            return

        try:
            if (theme == "easy"):
                crt = EasyPrettifier()
            else:
                raise Exception("Theme " + theme + " was not recognized.")

            crt.create(self.structured_doc)
            filename = self.structured_doc['metadata']['dc.title'] + ".html" if self.structured_doc['metadata']['dc.title'] != "" else self.structured_doc['src']['filename']
            crt.save(output_dir, filename)
            del crt
            print("Converted File Successfully: " + filename)
        except Exception as e:
            print("Error: could not beautify document data")
            print(e)
            self.reset()
            return

        self.reset()

    def reset(self):
        self.source, self.source_work, self.theme, self.output_dir = "", "", "", ""
        self.structured_doc = None

plato_urls = {
    #"alcibiadesI":  "https://www.gutenberg.org/cache/epub/1676/pg1676-images.html",     # ERROR: original missing toc markup
    "alcibiadesI":  "https://www.gutenberg.org/files/1676/1676-h/1676-h.htm",
    "alcibiadesII": "https://www.gutenberg.org/cache/epub/1677/pg1677-images.html",     # MINOR: no marcel.tr tag
    "apology":      "https://www.gutenberg.org/cache/epub/1656/pg1656-images.html",
    "charmides":    "https://www.gutenberg.org/cache/epub/1580/pg1580-images.html",
    "cratylus":     "https://www.gutenberg.org/cache/epub/1616/pg1616-images.html",     # Minor: translator in par; descriptions not parsed; add footnotes
    #"crito":        "https://www.gutenberg.org/cache/epub/1657/pg1657-images.html",     # ERROR: original missing toc markup
    "critias":      "https://www.gutenberg.org/cache/epub/1571/pg1571-images.html",
    "euthydemus":   "https://www.gutenberg.org/cache/epub/1598/pg1598-images.html",
    "euthyphro":    "https://www.gutenberg.org/cache/epub/1642/pg1642-images.html",
    "eryxias":      "https://www.gutenberg.org/cache/epub/1681/pg1681-images.html",
    "gorgias":      "https://www.gutenberg.org/cache/epub/1672/pg1672-images.html",
    "ion":          "https://www.gutenberg.org/cache/epub/1635/pg1635-images.html",
    "laches":       "https://www.gutenberg.org/cache/epub/1584/pg1584-images.html",     # Minor: PERSONS in TOC
    "laws":         "https://www.gutenberg.org/cache/epub/1750/pg1750-images.html",
    "lesser-hippias": "https://www.gutenberg.org/cache/epub/1673/pg1673-images.html",   # ERROR: original missing toc markup
    "lysis":        "https://www.gutenberg.org/cache/epub/1579/pg1579-images.html",     # Minor: PERSONS toc entry
    "menexenus":    "https://www.gutenberg.org/cache/epub/1682/pg1682-images.html",     # Minor: PERSONS toc entry
    "meno":         "https://www.gutenberg.org/cache/epub/1643/pg1643-images.html",
    "parmenides":   "https://www.gutenberg.org/cache/epub/1687/pg1687-images.html",
    "phaedo":       "https://www.gutenberg.org/cache/epub/1658/pg1658-images.html",     # Minor: PERSONS OF THE DIALOGUE in dialogue para
    "phaedrus":     "https://www.gutenberg.org/cache/epub/1636/pg1636-images.html",
    "philebus":     "https://www.gutenberg.org/cache/epub/1744/pg1744-images.html",
    "protagoras":   "https://www.gutenberg.org/cache/epub/1591/pg1591-images.html",
    # "republic2":     "https://www.gutenberg.org/cache/epub/55201/pg55201-images.html",
    "republic":     "https://www.gutenberg.org/cache/epub/1497/pg1497-images.html",
    "sophist":      "https://www.gutenberg.org/cache/epub/1735/pg1735-images.html",
    "statesman":    "https://www.gutenberg.org/cache/epub/1738/pg1738-images.html",
    "symposium":    "https://www.gutenberg.org/cache/epub/1600/pg1600-images.html",
    "timaeus":      "https://www.gutenberg.org/cache/epub/1572/pg1572-images.html",
    "theaetetus":   "https://www.gutenberg.org/cache/epub/1726/pg1726-images.html",
    "notplato":     "https://www.asdflasdfasdf.com/1.html",
}


bc = Html2PrettyHtml()

# URLs
# for url in plato_urls:
#     bc.convert("gutenberg", plato_urls[url], "easy", "output/gutenberg/urls")

#FILE
#bc.convert("gutenberg", "src/books/gutenberg/plato/plato-republic-2-tr-jowett-guttenberg.html", "easy", "output/gutenberg/plato")

# FILES
#src_directory = "src/books/gutenberg/"
src_directory = "src/books/gutenberg/plato/"
# src_directory = "src/books/gutenberg/aristotle/"
# src_directory = "src/books/gutenberg/sophocles"

for path, subdirs, files in os.walk(src_directory):
    for name in files:
        if name.endswith(".html"):
            bc.convert("gutenberg", os.path.join(path, name), "easy", "output/gutenberg/plato")
            time.sleep(1)

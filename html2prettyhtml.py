from prettifier import EasyPrettifier
from extractors import GutenbergExtractor

from urllib.request import urlopen
from urllib.parse import urlparse
import time
import os
import click
import logging

@click.command()
@click.argument('id', default="1643")
@click.argument('outputdir', default="output/test")
@click.option('--theme', default="easy", help="Theme. Default is the easy theme.")
@click.option('--fromlocaldir', help='Process book with **id** from a local directory instead of retrieving from url.')
@click.option('--all', is_flag=True, help='Process all files in a local directory. Id argument will be ignored.')
@click.option('--verbose', is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug', is_flag=True, help='Turn on debugging messages.')

def html2prettyhtml(id, outputdir, theme, fromlocaldir, all, verbose, debug):
    """ html2prettyhtml converts a Project Gutenberg book in html into pretty html reader.
    The reader is stylized by theme, the default being the "easy" theme.
    The books are retrieved from Project Guternberg directly or from a local source directory.
    """

    if verbose:
        logging.basicConfig(filename='html2prettyhtml.log', filemode="w", level=logging.INFO)

    if debug:
        logging.basicConfig(filename='html2prettyhtml.log', filemode="w", level=logging.DEBUG)

    themes = [ "easy" ]
    if theme not in themes:
        print("Error: theme not recognized. Valid themes: " + ", ".join(themes))
        return

    if all and not fromlocaldir:
        print("Error: --fromlocaldir option must be set to use --all\n E.g. python html2prettyhtml.py --fromlocaldir=/src/gutenberg --all")
        return

    bc = Html2PrettyHtml()

    if all and fromlocaldir:
        local_dir = fromlocaldir if fromlocaldir[-1] == "/" else fromlocaldir + "/"
        for path, subdirs, files in os.walk(local_dir):
            for name in files:
                if name.endswith(".html"):
                    bc.convert("gutenberg", os.path.join(path, name), outputdir, theme)
                    time.sleep(0.25)
            return

    if fromlocaldir:
        local_dir = fromlocaldir if fromlocaldir[-1] == "/" else fromlocaldir + "/"
        file_source = local_dir + "pg" + str(id) + "-images.html"
        bc.convert("gutenberg", file_source, outputdir, theme)
        return

    url_source = "https://www.gutenberg.org/cache/epub/" + str(id) + "/" + "pg" + str(id) + "-images.html"
    bc.convert("gutenberg", url_source, outputdir, theme)


class Html2PrettyHtml:
    source, source_work, theme, output_dir = "", "", "", ""
    structured_doc = None

    def convert(self, source, source_work, output_dir, theme):
        print('Started conversion from file %s.' % source_work)
        logging.info('Started converting %s.' % source_work)

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

            if (theme == "easy"):
                crt = EasyPrettifier()
            else:
                raise Exception("Theme " + theme + " was not recognized.")

            crt.create(self.structured_doc)
            #filename = self.structured_doc['metadata']['dc.title'] + ".html" if self.structured_doc['metadata']['dc.title'] != "" else self.structured_doc['src']['filename']
            filename = self.structured_doc['src']['filename']
            crt.save(output_dir, filename)

            del crt
            print("Converted File Successfully to " + self.output_dir + filename)
            logging.info('Converted File Successfully to %s.' % self.output_dir + filename)
            self.reset()
        except Exception as e:
            print(e)
            self.reset()
            return


    def reset(self):
        self.source, self.source_work, self.theme, self.output_dir = "", "", "", ""
        self.structured_doc = None

if __name__ == '__main__':
    html2prettyhtml()

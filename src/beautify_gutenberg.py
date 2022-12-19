from beautifiers.html.easy import EasyBeautifier
from beautifiers.tex.simple import SimpleBeautifier
from extractors.gutenberg.gutenberg import GutenbergExtractor

import os
import click
import logging

@click.command()
@click.argument('id')
@click.argument('dir')
@click.argument('theme')
@click.option('--fromlocaldir', is_flag=False,help='Process book with **id** from a local directory instead of retrieving from url.')
@click.option('--all',          is_flag=True, help='Process all files in a local directory. Id argument will be ignored.')
@click.option('--save',         is_flag=True, help='Saves Project Gutenberg source file to the output directory.')
@click.option('--json',         is_flag=True, help='Saves extraction into json file to the output directory.')
@click.option('--verbose',      is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug',        is_flag=True, help='Turn on debugging messages.')

def beautify_gutenberg(id, dir, theme, fromlocaldir, all, save, json, verbose, debug):
    """ Converts a Project Gutenberg book with [ID] into a HTML or TEX format with [THEME] into directory [DIR].
    THEME: \n
    html reader: easy, green\n
    tex document: simple\n
    See website for examples of type and theme.
    """

    #Valid input
    themes = {  "html": [ "easy" ],
                "tex" : [ "simple" ]}

    if theme not in themes["html"] and theme not in themes["tex"]:
        print("Input Error: theme not recognized. Valid themes: \n HTML: " + ", ".join(themes['html']) + "\n TEX: " + ", ".join(themes['tex']))
        exit(5)

    if all and not fromlocaldir:
        print("Input Error: --fromlocaldir option must be set to use --all\n E.g. python beautify_gutenberg.py --fromlocaldir=/src/gutenberg --all")
        exit(5)

    # Setup logging
    if verbose:
        logging.basicConfig(filename='./../logs/beautify.log', filemode="a", level=logging.INFO)

    if debug:
        logging.basicConfig(filename='./../logs/beautify.log', filemode="a", level=logging.DEBUG)

    # Run
    # beautify an entire directory
    bg = BeautifyGutenberg()
    if all and fromlocaldir:
        local_dir = fromlocaldir if fromlocaldir[-1] == "/" else fromlocaldir + "/"
        for path, subdirs, files in os.walk(local_dir):
            for name in files:
                if name.endswith(".html"):
                    bg.convert("gutenberg", os.path.join(path, name), dir, theme, json, save)
    # beautify one local file
    elif fromlocaldir:
        local_dir = fromlocaldir if fromlocaldir[-1] == "/" else fromlocaldir + "/"
        file_source = local_dir + "pg" + str(id) + "-images.html"
        bg.convert("gutenberg", file_source, dir, theme, json, save)
    # beautify one from URL
    else:
        url_source = "https://www.gutenberg.org/cache/epub/" + str(id) + "/" + "pg" + str(id) + "-images.html"
        bg.convert("gutenberg", url_source, dir, theme, json, save)
    del bg
    exit(0)


class BeautifyGutenberg:

    def convert(self, source, source_work, output_dir, theme, save_json = False, save_src = False):
        print('Started conversion of %s.' % source_work)
        logging.info('Started converting %s.' % source_work)

        # Validate source
        if source != "gutenberg":
            print("Error: Unrecognized source: %s.\n Could not convert %s " % source, source_work)
            logging.info('Input Error: unrecognized source %s .' % source_work)
            self.reset()
            return

        # Validate theme
        themes = {  "html": [ "easy" ],
                    "tex" : [ "simple" ]}
        if theme not in themes["html"] and theme not in themes["tex"]:
            print("Input Error: theme not recognized. Valid themes: \n HTML: " + ", ".join(themes['html']) + "\n TEX: " + ", ".join(themes['tex']))
            exit(5)

        # Initialize
        structured_doc = None
        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"

        try:
            # Extract Structured Document
            if source == "gutenberg":
                ext = GutenbergExtractor(source_work, output_dir, save_json, save_src)

            structured_doc = ext.extract()

            # Beautify Structured Document
            if theme == "easy":
                crt = EasyBeautifier()
            elif theme == "simple":
                crt = SimpleBeautifier()

            crt.create(structured_doc)
            crt.save(output_dir)

            print("Conversion Successful to %s" % output_dir)
            logging.info('Conversion Successful to %s.\n' % output_dir)
        except Exception as e:
            print("Error: Conversion could not be completed.")
            logging.debug("Exception occurred", exc_info=True)
            exit(1)

if __name__ == '__main__':
    beautify_gutenberg()

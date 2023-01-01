from extractors.extractor_factory import ExtractorFactory
from beautifiers.beautifier_factory import BeautifierFactory

import os
import click
import logging

import urllib.error
#from urlextract import URLExtract
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen


@click.command()
@click.argument('id')
@click.argument('outputdir')
@click.argument('theme')
@click.option('--fromlocaldir', is_flag=False,help='Process book with **id** from a local directory instead of retrieving from url.')
@click.option('--all',          is_flag=True, help='Process all files in a local directory. Id argument will be ignored.')
@click.option('--savesrc',      is_flag=True, help='Saves Project Gutenberg source file to the output directory.')
@click.option('--savejson',     is_flag=True, help='Saves extraction into json file to the output directory.')
@click.option('--verbose',      is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug',        is_flag=True, help='Turn on debugging messages.')

def convert_gutenberg(id, outputdir, theme, fromlocaldir, all, savesrc, savejson, verbose, debug, source = 'gutenberg'):
    """ Converts a Project Gutenberg book with [ID] into a HTML or TEX format with [THEME] into output directory [OUTPUTDIR].
    THEME: \n
    html reader: easy\n
    tex document: simple\n
    See website for examples of type and theme.
    """

    # Setup logging
    if verbose:
        logging.basicConfig(filename='./../logs/beautify.log', filemode="a", level=logging.INFO)

    if debug:
        logging.basicConfig(filename='./../logs/beautify.log', filemode="a", level=logging.DEBUG)

    #Validate input
    themes = {  "html": [ "easy" ],
                "tex" : [ "simple" ]}

    if source != "gutenberg":
        print("Error: Unrecognized source: %s." % source)
        logging.info("Input Error: unrecognized source %s." % source)
        exit(5)

    if theme not in themes["html"] and theme not in themes["tex"]:
        print("Input Error: theme not recognized. Run --help")
        logging.info("Input Error: theme not recognized %s." % theme)
        exit(5)

    if all and not fromlocaldir:
        print("Input Error: --fromlocaldir option must be set to use --all")
        logging.info("Input Error: --all used without --fromlocaldir.")
        exit(5)

    # Run
    if source == 'gutenberg':
        converter = BeautifyGutenberg()
    
    if all and fromlocaldir:
        ofile = converter.convertAllLocal(fromlocaldir, outputdir, theme, savesrc, savejson)
    elif fromlocaldir:
        ofile = converter.convertFromLocal(id, fromlocaldir, outputdir, theme, savesrc, savejson)
    else:
        ofile = converter.convertFromUrl(id, outputdir, theme, savesrc, savejson)
        print(ofile)
    exit(0)

class BeautifyGutenberg():

    save_src, save_json = False, False

    def convertAllLocal(self, src_dir, output_dir, theme, save_src = False, save_json = False):
        src_dir = src_dir if src_dir[-1] == "/" else src_dir + "/"
        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
    
        for path, subdirs, files in os.walk(src_dir):
            for name in files:
                if "epub" in name:
                    self.convert(os.path.join(path, name), output_dir, theme, save_src, save_json)
                if name.endswith(".html"):
                    self.convert(os.path.join(path, name), output_dir, theme, save_src, save_json)
        return

    def convertFromLocal(self, src_id, src_dir, output_dir, theme,  save_src = False, save_json = False):
        src_dir = os.path.abspath(src_dir) + "/"

        processable_types = [ 'epub', 'html' ]
        for type in processable_types:
            file_source = src_dir + "pg" + str(src_id) + "-images." + type
            if os.path.exists(file_source):
                break
        self.convert(file_source, output_dir, theme, save_src, save_json)
        return

    def convertFromUrl(self, id, output_dir, theme, save_src = False, save_json = False):
        url_source = "https://www.gutenberg.org/cache/epub/" + str(id) + "/" + "pg" + str(id) + "-images.html"

        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
        filename = "pg" + str(id) + "-images.html"
        src_file = output_dir + filename
   
        print('Started conversion of %s.' % url_source)
        try:
            f = urlopen(url_source)
            if not os.path.exists(output_dir):
               os.makedirs(output_dir)
            
            fout = open(src_file, "wb")
            fout.write(f.read())
            fout.close()

            return self.convert(src_file, output_dir, theme, save_src, save_json)


        except urllib.error.HTTPError as e:
            print("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            logging.info("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            exit(1)
        except URLError as url_error:
            print("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            logging.info("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            exit(1)

    def convert(self, src_file, output_dir, theme, save_src = False, save_json = False) -> str:
        logging.info('Started converting %s.' % src_file)

        try:
            ext = ExtractorFactory().create('gutenberg', src_file, output_dir, save_src, save_json)
            structured_doc = ext.extract()

            beau = BeautifierFactory().create(theme)
            beau.create(structured_doc)
            output_file = beau.save(output_dir)

            print("Conversion Successful to %s" % output_file)
            logging.info("Conversion Successful to %s.\n" % output_file)
            return output_file
            

        except Exception as e:
            print("Error: Conversion could not be completed.")
            logging.debug(e)
            exit(1)

if __name__ == '__main__':
    convert_gutenberg()

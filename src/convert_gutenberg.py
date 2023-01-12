from extractors.extractor_factory import ExtractorFactory
from beautifiers.beautifier_factory import BeautifierFactory

import os
import click
import logging

import urllib.error
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen


@click.command()
@click.argument('id')
@click.argument('srctype')
@click.argument('outputdir')
@click.argument('theme')
@click.option('--fromlocaldir', is_flag=False,help='Process book with **id** from a local directory instead of retrieving from url.')
@click.option('--all',          is_flag=True, help='Process all files in a local directory. Id argument will be ignored.')
@click.option('--savesrc',      is_flag=True, help='Saves Project Gutenberg source file to the output directory.')
@click.option('--savejson',     is_flag=True, help='Saves extraction into json file to the output directory.')
@click.option('--verbose',      is_flag=True, help='Get extra information about what\'s happening behind the scenes.')
@click.option('--debug',        is_flag=True, help='Turn on debugging messages.')

def convert_gutenberg(id, srctype, outputdir, theme, fromlocaldir, all, savesrc, savejson, verbose, debug, source = 'gutenberg'):
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

    # Validate input
    valid_src_type = {  "epub", "html" }
    valid_themes = {    "html": [ "easy" ],
                        "tex" : [ "simple" ]}

    if srctype not in valid_src_type:
        print("Error: Unrecognized source type: %s." % source)
        logging.info("Input Error: unrecognized source type %s." % source)
        exit(5)

    if source != "gutenberg":
        print("Error: Unrecognized source: %s." % source)
        logging.info("Input Error: unrecognized source %s." % source)
        exit(5)

    if theme not in valid_themes["html"] and theme not in valid_themes["tex"]:
        print("Input Error: theme not recognized. Run --help")
        logging.info("Input Error: theme not recognized %s." % theme)
        exit(5)

    if all and not fromlocaldir:
        print("Input Error: --fromlocaldir option must be set to use --all")
        logging.info("Input Error: --all used without --fromlocaldir.")
        exit(5)

    # Run
    if source == 'gutenberg':
        converter = BeautifyGutenberg(srctype, theme, savesrc, savejson)
    
        if all and fromlocaldir:
            ofile = converter.convertAllLocal(fromlocaldir, outputdir)
        elif fromlocaldir:
            ofile = converter.convertFromLocal(id, fromlocaldir, outputdir)
        else:
            ofile = converter.convertFromUrl(id, outputdir)
    exit(0)

class BeautifyGutenberg():

    """
        The converter for converting gutenberg books into html or latex
    """

    src_type = ""
    theme = ""
    save_src, save_json = False, False

    def __init__(self, src_type, theme, save_src, save_json) -> None:
        self.src_type = src_type
        self.save_src = save_src
        self.save_json = save_json
        self.theme = theme
        

    def convertAllLocal(self, src_dir, output_dir) -> list:
        src_dir = src_dir if src_dir[-1] == "/" else src_dir + "/"
        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
    
        converted_files = []

        for path, subdirs, files in os.walk(src_dir):
            for name in files:
                if name.endswith("." + self.src_type):
                    print("Started converstion of %s." % os.path.join(path, name))
                    outputfile =self.convert(os.path.join(path, name), output_dir)
                    converted_files.append(outputfile)
        return converted_files

    def convertFromLocal(self, src_id, src_dir, output_dir) -> str:
        src_dir = os.path.abspath(src_dir) + "/"

        if self.src_type == "epub":
            epub_file = src_dir + "pg" + str(src_id) + ".epub"
        elif self.src_type == "html":
            html_file = src_dir + "pg" + str(src_id) + "-images.html"

        if self.src_type == "epub" and os.path.exists(epub_file):
            src_file_path = epub_file
        elif self.src_type == "html" and os.path.exists(html_file):
            src_file_path = html_file
        else:
            raise Exception("Gutenberg file of type " + self.src_type + " with id" + str(src_id) + " not found in " + src_dir)
        
        print("Started converstion of %s." % src_file_path)
        return self.convert(src_file_path, output_dir)

    def convertFromUrl(self, id, output_dir) -> str:
        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"

        if self.src_type == "html":
            url_source = "https://www.gutenberg.org/cache/epub/" + str(id) + "/" + "pg" + str(id) + "-images.html"
            filename = "pg" + str(id) + "-images.html"
        elif self.src_type == "epub":
            url_source = "https://www.gutenberg.org/cache/epub/" + str(id) + "/" + "pg" + str(id) + ".epub"
            filename = "pg" + str(id) + ".epub"
        else:
            raise Exception("src type" + self.src_type + " not recognized")
        src_file = output_dir + filename
   
        print('Started conversion of %s.' % url_source)
        try:
            f = urlopen(url_source)
            if not os.path.exists(output_dir):
               os.makedirs(output_dir)
            
            fout = open(src_file, "wb")
            fout.write(f.read())
            fout.close()

            return self.convert(src_file, output_dir)

        except urllib.error.HTTPError as e:
            print("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            logging.info("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            logging.debug(e)
            exit(1)
        except URLError as e:
            print("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            logging.info("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            logging.debug(e)
            exit(1)
        except Exception as e:
            print(e)
            exit(1)

    def convert(self, src_file, output_dir) -> str:
        logging.info('Started converting %s.' % src_file)

        try:
            ext = ExtractorFactory().create('gutenberg', self.src_type, src_file, output_dir, self.save_src, self.save_json)
            structured_doc = ext.extract()

            beau = BeautifierFactory().create(self.theme)
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

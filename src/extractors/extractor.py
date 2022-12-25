from bs4 import BeautifulSoup
import json
import os
import logging
import urllib.error
from urlextract import URLExtract
from urllib.error import URLError
from urllib.error import HTTPError
from urllib.request import urlopen

class Extractor:
    extractor = None
    soup = None
    src_html = ""

    src, metadata, toc, sections, body, section_urls, section_files, sections_html = {}, {}, {}, {}, {}, {}, {}, {}
    structured_doc = {}
    license = ""

    output_dir, src_file, src_dir, src_url = "", "", "", ""
    save_json, save_src = False, False

    def __init__(self, source_work, output_dir):
        logging.basicConfig(filename='../logs/html2prettyhtml.log', filemode="a", level=logging.DEBUG)
        logging.info('Created Extractor')

        self.output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
        urls = URLExtract().find_urls(source_work)

        if urls:
            self.src_url = urls[0]
            self.src_filename = urls[0].split("/")[-1]
        else:
            self.src_file = source_work.strip()
            self.src_dir = os.path.dirname(source_work) + "/"
            self.src_filename = os.path.basename(source_work)

        try:
            if self.src_url != "":
                f = urlopen(self.src_url)
            else:
                f = open(self.src_file, "rb")
            html = f.read()
            f.close()
        except urllib.error.HTTPError as e:
            print("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            logging.info("Error: could not convert url: " + self.src_url + " HTTPError: " + format(e.code))
            exit(1)
        except URLError as url_error:
            print("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            logging.info("Error: could not open :" + self.src_url + " URL Error: Server Not Found")
            exit(1)
        except OSError as e:
            print("Error: could not open url: " + self.src_url + ": file/url not found or not readable")
            logging.info("Error: could not open url: " + self.src_url + ": file/url not found or not readable")
            exit(1)
        except Exception as e:
            print("Error: could not extract html from url/file")
            logging.info("Error: could not extract html from url/file")
            return

        self.src_html = html
        self.soup = BeautifulSoup(html, 'html5lib')

    def extract(self):

        self.extract_metadata()
        self.extract_src()
        self.extract_toc()
        self.extract_sections()
        self.extract_body()

        self.construct_structured_doc()

        if self.save_json: self.save_json_file()
        if self.save_src: self.save_src_file()

        self.reset()

        logging.info("Extraction Complete")
        return self.structured_doc

    def construct_structured_doc(self):
        self.structured_doc['src'] = self.src
        logging.info(self.structured_doc['src'])
        self.structured_doc['metadata'] = self.metadata
        logging.info(self.structured_doc['metadata'])
        self.structured_doc['toc'] = self.toc
        logging.info(self.structured_doc['toc'])
        self.structured_doc['sections'] = self.sections
        logging.info(self.sections.keys())
        self.structured_doc['body'] = self.body
        

    def save_src_file(self):
        src_filename = self.output_dir + "src/" + self.src_filename

        try:
            os.makedirs(self.output_dir + "src/", exist_ok=True)
            f = open(src_filename, "wb")
            f.write(self.src_html)
            f.close()
            logging.info("Source file saved to " + src_filename)
        except Exception as e:
            print("Error: could not save source file %s" % src_filename)
            logging.info("Error: could not save source file %s" % src_filename)
            logging.debug(e)
            exit(1)

    def save_json_file(self):
        source = self.src_file if (self.src_file) else self.src_url
        json_filename = self.output_dir + "json/" + source.split("/")[-1].split(".")[0] + ".json"

        try:
            os.makedirs(self.output_dir + "json/", exist_ok=True)
            with open(json_filename, "w") as outfile:
                json.dump(self.structured_doc, outfile)
            outfile.close()
            logging.info("JSON file saved to " + json_filename)
        except Exception as e:
            print("Error: could not save json file %s" % json_filename)
            logging.info("Error: could not save json file %s" % json_filename)
            logging.debug(e)
            exit(1)

    def reset(self):
        self.extractor = None
        self.src_html = ""
        self.soup = None
        self.metadata, self.toc, self.sections, self.body, self.section_urls, self.section_files, self.sections_html = {}, {}, {}, {}, {}, {}, {}
        self.output_dir, self.src_file, self.src_url = "", "", ""
        self.save_json, self.save_src = False, False

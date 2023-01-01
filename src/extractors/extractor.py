from bs4 import BeautifulSoup
import json
import os
import logging

class Extractor:
    extractor = None
    soup = None
    src_html = ""

    src, metadata, toc, sections, body, section_urls, section_files, sections_html = {}, {}, {}, {}, {}, {}, {}, {}
    structured_doc = {}
    license = ""

    output_dir, src_file, src_dir, src_url = "", "", "", ""
    save_json, save_src = False, False
    logging_level = logging.DEBUG

    def __init__(self, src_file, output_dir, save_src = False, save_json = False):

        logging.info('Created Extractor')

        self.output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"

        self.src_file = src_file.strip()
        self.src_dir = os.path.dirname(src_file) + "/"
        self.src_filename = os.path.basename(src_file)
        self.save_src = save_src
        self.save_json = save_json

        try:
            f = open(self.src_file, "rb")
            html = f.read()
            f.close()

            self.src_html = html
            self.soup = BeautifulSoup(html, 'html5lib')
        except OSError as e:
            print("Error: could not open file: " + self.src_file + ": file not found or not readable")
            logging.info("Error: could not open url: " + self.src_file + ": file not found or not readable")
            exit(1)
        except Exception as e:
            print("Error: could not extract html from file " + self.src_file)
            logging.info("Error: could not extract html from file" + self.src_file)
            return

       

    def extract(self):

        self.extract_metadata()
        self.extract_src()
        self.extract_toc()
        self.extract_sections()
        self.extract_body()

        self.structured_doc['src'] = self.src
        self.structured_doc['metadata'] = self.metadata
        self.structured_doc['toc'] = self.toc
        self.structured_doc['sections'] = self.sections
        self.structured_doc['body'] = self.body

        logging.info(self.structured_doc['src'])
        logging.info(self.structured_doc['metadata'])
        logging.info(self.structured_doc['toc'])
        logging.info(self.sections.keys())

        if self.save_json: self.save_json_file()
        if self.save_src: self.save_src_file()

        self.reset()

        logging.info("Extraction Complete")
        return self.structured_doc

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

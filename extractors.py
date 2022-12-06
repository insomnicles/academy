from bs4 import BeautifulSoup
import re
import nltk
import json
import os
from urlextract import URLExtract

from urllib.request import urlopen

class Extractor:
    DEBUG = False
    extractor = None
    soup = None
    src_html = ""

    metadata, toc, sections, body, section_urls, section_files, sections_html = {}, {}, {}, {}, {}, {}, {}
    structured_doc = {}
    license = ""

    output_dir, src_file, src_dir, src_url = "", "", "", ""

    def __init__(self, source_work, output_dir):
        print("Created Extractor") if self.DEBUG else True
        self.output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
        urls = URLExtract().find_urls(source_work)

        if urls:
            self.src_url = urls[0]
            self.src_filename = urls[0].split("/")[-1]
        else:
            self.src_file = source_work.strip()
            self.src_dir = os.path.dirname(source_work) + "/"
            self.src_filename = os.path.basename(source_work)

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
        self.soup = BeautifulSoup(html, 'html5lib')

    def extract(self):
        self.extract_metadata()
        self.extract_toc()
        self.extract_sections()
        self.extract_body()
        self.construct_structured_doc()
        self.save()
        return self.structured_doc

    def construct_structured_doc(self):
        self.structured_doc['src'] = {
            "source": "gutenberg",
            "file": self.src_file,
            "dir": self.src_dir,
            "filename": self.src_filename,
            "url": self.src_url,
        }
        self.structured_doc['metadata'] = self.metadata
        self.structured_doc['toc'] = self.toc
        self.structured_doc['sections'] = self.sections
        self.structured_doc['body'] = self.body

    def save(self):
        if (self.src_file):
            json_filename = self.output_dir + "json/" + self.src_file.split("/")[-1].split(".")[0] + ".json"
        elif (self.src_url):
            json_filename = self.output_dir + "json/" + self.src_url.split("/")[-1].split(".")[0] + ".json"
        else:
            print("Could not save JSON file")
            return

        os.makedirs(self.output_dir + "json/", exist_ok=True)
        with open(json_filename, "w") as outfile:
            json.dump(self.structured_doc, outfile)
        outfile.close()

    def reset(self):
        self.extractor = None
        self.src_html = ""
        self.soup = None
        self.metadata, self.toc, self.sections, self.body, self.section_urls, self.section_files, self.sections_html = {}, {}, {}, {}, {}, {}, {}
        self.structured_doc = {}
        self.output_dir, self.src_file, self.src_url = "", "", ""


class GutenbergExtractor(Extractor):
    gutenberg_license = "http://gutenberg.org/license"

    def __init__(self, source_work, output_dir):
        print("Created Gutenberg Dialogue Extractor") if self.DEBUG else True
        super().__init__(source_work, output_dir)
        self.license = self.gutenberg_license

    def extract_metadata(self):
        metadata, subjects = {}, []
        self.metadata = {}

        # Initialize the following required metadata
        metadata['dc.title'] = ""
        metadata['dc.creator'] = ""
        metadata['marcrel.trl'] = ""

        for tag in self.soup.find_all('meta'):
            name = tag.get('name')
            content = tag.get('content')
            if name is not None and content is not None:
                if name == 'dc.subject':
                    subjects.append(content)
                else:
                    metadata[tag.get('name')] = tag.get('content')
            # property = tag.get('property')
            # if property is not None and content is not None:
            #     metadata[property] = content

        if 'subjects' in metadata.keys():
            metadata['subjects'] = subjects

        # for tag in self.soup.find_all('link'):
        #     rel = tag.get('rel')
        #     href = tag.get('href')
        #     if rel and href:
        #         metadata[rel[0]]=href

        metadata['source_url'] = self.src_url
        metadata['source_licence_url'] = self.license
        self.metadata = metadata
        print(self.metadata)  if self.DEBUG else True

    def extract_toc(self):
        self.toc = {}
        entries, toc = [], {}

        soup = BeautifulSoup(self.src_html, 'html5lib')
        for tag in soup.body.find_all():
            if (tag.name == "a"):

                # Skip Footnotes
                href=tag.get('href')
                id=tag.get('id')
                #if tag.get('href') is not None and ("#f" in tag.get('href') or "#r" in tag.get('href') or "fn" in tag.get('href') or "#Footnote" in tag.get('href') or "Page_"):
                if href is not None and ("#f" in href or "#r" in href or "fn" in href or "#Footnote" in href):
                    continue
                #if tag.get('id') is not None and ("fn" in tag.get('id') or "Footnote" in tag.get('id') ):
                if id is not None and ("fn" in id or "Footnote" in id or "FNanchor" in id):
                    continue

                # entry
                if tag.get('id') is not None:
                    entries.append(tag['id'])

                # toc entry
                if tag.get('href') is None:
                    continue
                if "#link2H" in tag.get('href'):
                    toc[tag.get("href")[1:]] = tag.text.strip()
                if "#chap" in tag.get('href'):
                    toc[tag.get("href")[1:]] = tag.text.strip()
                if "#pref" in tag.get('href'):
                    toc[tag.get("href")[1:]] = tag.text.strip()
                if "#intro" in tag.get('href'):
                    toc[tag.get("href")[1:]] = tag.text.strip()
                if "#Book" in tag.get('href'):
                    toc[tag.get("href")[1:]] = tag.text.strip()
                # if "#Pg" in tag.get('href'):
                #     toc[tag.get("href")[1:]] = tag.text.strip()
                # if "#part" in tag.get('href'):
                #     toc[tag.get("href")[1:]] = tag.text.strip()
            # if (tag.name == "h2"):
            #     id=tag.get('id')
            #     if (id is not None and "BOOK_" in id):
            #         toc[id] = tag.text.strip()

        if len(entries) != len(toc):
            print("WARNING: TOC entries do not match document entries")
            return None
        self.toc = toc

    def extract_sections(self):
        self.sections = {}
        current_section, sections = '', {}

        for tag in self.soup.body.find_all():
            if tag.name == "a" and tag.get('id') is not None and "fn" not in tag.get('id'):
                current_section = tag.get('id')
                sections[current_section] = ''
            if (tag.name == "p" and tag.text != "" and current_section != '' ):
                section_html = sections[current_section] + str(tag)
                sections[current_section] = section_html

        self.sections = sections
        #return self.sections

    def extract_body(self):
        dialogue_descriptors = [ 'PERSONS OF THE DIALOGUE', 'SCENE', 'PLACE OF THE NARRATION' ];

        speakers = ['ALCIBIADES', 'ANYTUS', 'APOLLODORUS', 'ATHENIAN', 'ATHENIAN STRANGER','BOY',
                    'CALLICLES', 'CHAEREPHON', 'CLEINIAS', 'COMPANION', 'CLEITOPHON', 'CRATYLUS', 'CRITIAS', 'CRITO', 'ECHECRATES',
                    'ERASISTRATUS', 'ERYXIAS', 'EUCLID', 'EUDICUS', 'EUTHYPHRO', 'GORGIAS', 'HERMOCRATES', 'HERMOGENES',
                    'HIPPIAS', 'ION', 'LACHES', 'LYSIMACHUS', 'MEGILLUS', 'MELESIAS', 'MENEXENUS', 'MENO', 'NICIAS',
                    'PHAEDO', 'PHAEDRUS', 'PHILEBUS', 'POLUS', 'PROTARCHUS', 'SOCRATES', 'SON', 'STRANGER', 'TERPSION',
                    'THEAETETUS', 'THEODORUS', 'TIMAEUS', 'YOUNG SOCRATES' ]

        par_num, converted_html = 0, ""
        descriptors = {}
        self.body = {}
        par_num = 0

        for section_id in self.sections:
            pars = {}
            soup = BeautifulSoup(self.sections[section_id],"html5lib")
            for ptag in soup.find_all('p'):

                speaker, speech, sentences_html = "", "", ""

                clean_text = re.sub(" ", "", re.sub("\n", "", ptag.text)).strip()
                if not clean_text:
                    continue

                clean_text = ptag.text.replace("\n", " ").replace("\t"," ")
                clean_text = re.sub(" +", " ", clean_text).strip()

                if not clean_text:
                    continue

                split = clean_text.split(':')
                first = split[0].strip()

                # Stephanus Annotation Tags
                children= ptag.findChild()
                if children is not None:
                    for child in children:
                        if (child.name == 'span' and child.get('class') == "stpagenum"):
                            print('STEPHANUS SPAN FOUND')
                        #print("CHILD:" + child.text + "ZZZ")

                # Dialogue description
                if first in dialogue_descriptors:
                    #print("Descriptor Found" + first)
                    descriptor = first
                    description = ': '.join(split[1:])

                    descriptors[descriptor] = description

                    converted_html = f"""
                                        {converted_html}
                                        <div class="description">
                                            <div class="book_description">{descriptor}:</div>{description}
                                        </div>"""

                # Dialogue paragraph w/ speaker
                elif first in speakers:
                    speaker = first

                    speaker_html = "<div class=\"speaker\">" + speaker + "</div>"
                    par_num +=1
                    par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"

                    speech = ': '.join(split[1:])

                    par_sentences = nltk.sent_tokenize(speech)
                    for sentence in par_sentences:
                        sentences_html = sentences_html + "<div class=\"sentence\"> " + sentence + "</div>"

                    converted_html = converted_html + "<div class=\"speech\">" + par_num_html + speaker_html + sentences_html + "</div>\n"
                    pars[par_num] = { "type": "speech",
                                      "speaker": speaker,
                                      "sentences": par_sentences,
                                      "images": {},
                                      "footnotes": {}
                                    }
                # Regular Text Paragraph (w/o speaker or dialogue description)
                else:
                    par_num +=1
                    par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"

                    par_sentences = nltk.sent_tokenize(clean_text)
                    for sentence in par_sentences:
                        sentences_html = sentences_html + "<div class=\"sentence\"> " + sentence + "</div>"

                    converted_html = converted_html + f"""<div class="speech">{par_num_html} {sentences_html}</div>\n"""

                    pars[par_num] = { "type": "text",
                                      "sentences": par_sentences,
                                      "images": {},
                                      "footnotes": {}
                                    }

                sentences_html, speaker_html = "", ""
            self.body[section_id] = pars
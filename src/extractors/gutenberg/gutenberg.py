from ..extractor import Extractor
from bs4 import BeautifulSoup
import re
import nltk
import logging

class GutenbergExtractor(Extractor):
    gutenberg_license = "http://gutenberg.org/license"

    def __init__(self, source_work, output_dir, save_json, save_src):
        logging.info("Created Gutenberg Dialogue Extractor")
        super().__init__(source_work, output_dir)
        self.license = self.gutenberg_license
        self.save_json = save_json
        self.save_src = save_src

    def extract_src(self):
        gutenberg_id = ""
        if (self.metadata['dcterms.source']):
            gutenberg_id = int(self.metadata['dcterms.source'].split("files/")[1].split("/")[0])

        self.src = {
            "source": "gutenberg",
            "id": gutenberg_id,
            "file": self.src_file,
            "dir": self.src_dir,
            "filename": self.src_filename,
            "url": self.src_url,
        }

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

        if 'subjects' in metadata.keys():
            metadata['subjects'] = subjects

        metadata['source_url'] = self.src_url
        metadata['source_licence_url'] = self.license
        self.metadata = metadata

    def extract_toc(self):
        toc_indicators = [ "#link2H", "#toc", "#ch", "#chap", "#Chapter", "#CHAPTER", "#pref", "#intro", "#Book", "#RULE", "#Bk", "#vol", "#biblio", "#I", "#V", "#X", "#para", "#part"]

        self.toc = {}
        toc = {'toc': {}}
        soup = BeautifulSoup(self.src_html, 'html5lib')
        for tag in soup.body.find_all('a'):
            if (tag.get('href') is not None):
                href = tag.get('href')
                for indicator in toc_indicators:
                    if (indicator.upper() in href.upper()):
                        toc['toc'][href[1:]] = tag.text.strip()
        if not toc['toc']:
            toc['toc'][0] = ""

        tables = soup.find_all('table')
        toc['table_html'] = str(tables[0]) if tables else ""
        self.toc = toc

    def extract_sections(self):
        self.sections = {}
        current_section, sections = '', {}
        toc_keys = self.toc['toc'].keys()

        # remove gutenberg section header and footer
        excluded_section_tag = [ "section" ]
        for tag in self.soup.body.find_all():
            if (tag.name is not None and tag.name in excluded_section_tag):
                tag.decompose()
                continue

        # books without table of contents have a 0 section
        if 0 in toc_keys and self.toc['toc'][0] == "":
            current_section = 0
            sections[0] = ""
            section_html = ""
            included_section_tag = [ "h1", "h2", "h3", "h4", "p", "pre" ]

            for tag in self.soup.body.find_all():
                if tag.name in included_section_tag and tag.text != "":
                    section_html += str(tag)
            sections[0] = section_html
        # books with extracted toc
        else:
            for tag in self.soup.body.find_all():
                if tag.get('id') is not None and tag.get('id') in toc_keys:
                    current_section = tag.get('id')
                    sections[current_section] = ''
                if current_section != '':
                    section_html = sections[current_section] + str(tag)
                    sections[current_section] = section_html
        self.sections = sections

    def isLinePoem(self, tag) -> bool:
        poem_indicator = [ "poem" ]
        if tag.get('class') is None:
            return False

        for css_class in tag.get('class'):
            if css_class in poem_indicator:
                return True
        return False

    def isPre(self, tag) -> bool:
        return tag.name is not None and tag.name == "pre"

    def isHeading(self, tag) -> bool:
        heading_indicator = [ "h1", "h2", "h3", "h4", "h5"]
        return tag.name is not None and tag.name in heading_indicator

    def isDialogueDescriptor(self, tag) -> bool:
        dialogue_descriptors = [ 'PERSONS OF THE DIALOGUE', 'SCENE', 'PLACE OF THE NARRATION' ];
        if tag.text is None:
            return False

        for descriptor in dialogue_descriptors:
            if descriptor in tag.text:
                return True
        return False

    def isSpeech(self, tag) -> bool:
        speakers = ['ALCIBIADES', 'ANYTUS', 'APOLLODORUS', 'ATHENIAN', 'ATHENIAN STRANGER','BOY',
                    'CALLICLES', 'CHAEREPHON', 'CLEINIAS', 'COMPANION', 'CLEITOPHON', 'CRATYLUS', 'CRITIAS', 'CRITO', 'ECHECRATES',
                    'ERASISTRATUS', 'ERYXIAS', 'EUCLID', 'EUDICUS', 'EUTHYPHRO', 'GORGIAS', 'HERMOCRATES', 'HERMOGENES',
                    'HIPPIAS', 'ION', 'LACHES', 'LYSIMACHUS', 'MEGILLUS', 'MELESIAS', 'MENEXENUS', 'MENO', 'NICIAS',
                    'PHAEDO', 'PHAEDRUS', 'PHILEBUS', 'POLUS', 'PROTARCHUS', 'SOCRATES', 'SON', 'STRANGER', 'TERPSION',
                    'THEAETETUS', 'THEODORUS', 'TIMAEUS', 'YOUNG SOCRATES' ]

        upper_case_words = re.findall(r'\b[A-Z]+(?:\s+[A-Z]+)*\b', tag.text)
        firstColon = tag.text.split(':')[0].strip()

        # for word in upper_case_words:
        #     spacy_parser = self.english_nlp(word)
        #     for entity in spacy_parser:
        #         print(f'Found: {entity.text} of type: {entity.label_}')

        # for entity in spacy_parser.ents:
        #     print(entity)
        #     if entity.label_ == "PERSON":
        #         logging.info(f'Found: {entity.text} of type: {entity.label_}')
        #         print(f'Found: {entity.text} of type: {entity.label_}')

        return firstColon.isupper() and firstColon in speakers

    def isImage(self, tag) -> bool:
        return tag.name == "img" and tag.get('src') != ""

    def isFootnote(self, tag) -> bool:
        footnote_indicators = [ "#Footnote", "#FN", "#linknote", "#f", "#r", "#Footnote", "Page_" ]
        return tag.name is not None and tag.get('href') is not None and tag.name == "a" and tag.get('href') in footnote_indicators and "pginternal" in tag.get('class')

    def isSidenote(self, tag) -> bool:
        sidenote_indicators = [ "#sidenote" ]
        return False

    def isEndnote(self, tag) -> bool:
        endnote_indicators = [ "#endnote" ]
        return False

    def isPageNum(self, tag) -> bool:
        pagenum_indicators = [ "page" ]
        return False

    def isScholarPage(self, tag) -> bool:
        scholar_pagenum_indicators = [ "stpagenum" ]
        # elif child.name == 'span' and child.get('class') in pagenum_indicators:
        return False

    def isRegularParagraph(self, tag) -> bool:
        return tag.name == "p" and not self.isLinePoem(tag)     # and is not ...

    def isParagraphSkippableTag(self, tag) -> bool:
        skippable = [ "html", "head", "body", "i", "br" ]
        return tag.name is not None and tag.name in skippable

    def extract_children(self, tag):
        children = tag.findChildren()
        if children is None:
            return ( [], [], [])

        book_id = self.src['id']

        structured_par_text = ""
        images, footnotes, annotations = [],[], []

        # Converting Paragraph Html to Paragraph with Markup for Footnotes, Endnotes, etc. + Image collection
        for child in children:
            if child.name is None:
                logging.info("CHILD HAS NO NAME")
            elif child.name == 'img':
                src = child.get('src') if child.get('src') is not None else ""
                images.append({
                    "id": child.get('id') or "",
                    "alt": child.get('alt') or "",
                    "src": "https://www.gutenberg.org/files/" + str(book_id) + "/" + str(book_id) + "-h/" + src or "",
                    "height": child.get('height') or "",
                    "width": child.get('width') or "",
                    "caption": ""
                })
                logging.info("IMAGE FOUND: " + src)
            elif self.isFootnote(child):
                logging.info("Footnote FOUND: ")
                pass
            elif self.isPageNum(child):
                #logging.info("Found Page Number")
                pass
            elif self.isScholarPage(child):
                #logging.info('SCHOLARLY ANNOTATION FOUND')
                pass
            elif child.name == "i":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "em":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "br":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "hr":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "a":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "p":
                # logging.info("CHILD <I>")
                pass
            elif child.name == "span":
                # logging.info("CHILD SPAN NOT RECOGNIZED: ")
                # logging.info(child.attrs.values())
                pass
            else:
                logging.info("CHILD NAME NOT RECOGNIZED: " + child.name)
                logging.info(child.attrs.values())
        return ( images, footnotes, annotations)

    def extract_body(self):
        self.body = {}
        tag_num = 0
        elem_num = 0

        for section_id in self.sections:
            elems = {}
            soup = BeautifulSoup(self.sections[section_id],"html5lib")
            sec_elem_num = 0

            for tag in soup.find_all():
                speaker, speech = "", ""
                images, footnotes, annotations = [], [], []

                if self.isParagraphSkippableTag(tag):
                    continue

                # todo: heading levels
                if self.isHeading(tag):
                    ( images, footnotes, annotations ) = self.extract_children(tag)
                    elems[elem_num] = {"elem_num": elem_num,
                                      "sec_par_num": sec_elem_num,
                                      "type": "heading",
                                      "level": 2,
                                      "heading": tag.text,
                                      "images": images,
                                      "footnotes": footnotes,
                                      "annotations": annotations}
                elif tag.name == "a":
                    pass
                elif self.isPre(tag):
                    ( images, footnotes, annotations ) = self.extract_children(tag)
                    elems[elem_num] = {"elem_num": elem_num,
                                      "sec_par_num": sec_elem_num,
                                      "type": "pre",
                                      "sentences": { 0: tag.text },
                                      "images": images,
                                      "footnotes": footnotes,
                                      "annotations": annotations }
                # todo: children for images, etc.
                elif self.isLinePoem(tag):
                    lines = []
                    for line in tag.text.split("\n"):
                        if line != "":
                            lines.append(line.strip())
                    ( images, footnotes, annotations ) = self.extract_children(tag)
                    elems[elem_num] = {"elem_num": elem_num,
                                      "sec_par_num": sec_elem_num,
                                      "type": "poem",
                                      "lines": lines,
                                      "images": images,
                                      "footnotes": footnotes,
                                      "annotations": annotations}
                elif self.isDialogueDescriptor(tag):
                    descriptor = tag.text.split(":")[0]
                    description = ' '.join(tag.text.split(":")[1:])
                    elems[elem_num] = {
                        "type": "descriptor",
                        "descriptor": descriptor,
                        "description": description }
                elif self.isSpeech(tag):
                    # Use regex to get the first set of capital letters? [ending in :,., ...; KING ARTHUR, SOCRATES, but not Some day...
                    clean_text = re.sub(" +", " ", tag.text.replace("\n", " ").replace("\t"," ")).strip()
                    speaker = clean_text.split(':')[0]
                    speech = ': '.join(clean_text.split(':')[1:])
                    par_sentences = nltk.sent_tokenize(speech)

                    ( images, footnotes, annotations ) = self.extract_children(tag)
                    elems[elem_num] = {  "elem_num": elem_num,
                                        "sec_par_num": sec_elem_num,
                                        "type": "speech",
                                        "speaker": speaker,
                                        "sentences": par_sentences,
                                        "images": images,
                                        "footnotes": footnotes,
                                        "annotations": annotations }
                # todo: separate paragraph: text only, and ii) text with <a> removed, but with html style tags <i>, <strong>, <sup>, etc.
                elif self.isRegularParagraph(tag):
                    # logging.info("Regular PAR")
                    clean_text = re.sub(" +", " ", tag.text.replace("\n", " ").replace("\t"," ")).strip()

                    ( images, footnotes, annotations ) = self.extract_children(tag)
                    par_sentences = nltk.sent_tokenize(clean_text)
                    elems[elem_num] = {  "elem_num": elem_num,
                                        "sec_par_num": sec_elem_num,
                                        "type": "text",
                                        "sentences": par_sentences,
                                        "images": images,
                                        "footnotes": footnotes,
                                        "annotations": annotations }
                elif (tag.name is not None):
                    #logging.info("TAG NOT RECOGNIZED:" + tag.name)
                    continue
                elif (tag.name is None and tag.text != ""):
                    #logging.info("TAG WITH TEXT BUT NO NAME: ")
                    continue
                else:
                    logging.info("TAG WITH NO NAME OR TEXT:")
                elem_num += 1
                sec_elem_num += 1
            self.body[section_id] = elems
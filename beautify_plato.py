import re
import nltk
import sys
import shutil
from bs4 import BeautifulSoup
import os
import os.path

def get_meta_tags(parsed_html):

    metaInfo, subjects = [], []

    for tag in parsed_html.find_all('meta'):
        name = tag.get('name')
        content = tag.get('content')
        if name is not None and content is not None:
            if name == 'dc.subject':
                subjects = ''
            else:
                metaInfo.append({ tag.get('name'): tag.get('content') })
    metaInfo.append({'subjects': subjects})

    return metaInfo

def get_toc(parsed_html):

    entries, toc = [], {}

    # toc: id =
    # entry tags href=['chap', 'link2H']
    # footnote_tags ['fn',]

    for tag in parsed_html.body.find_all():
        if (tag.name == "a"):

            # Skip Footnotes
            if tag.get('href') is not None and ("#f" in tag.get('href') or "#r" in tag.get('href') or "fn" in tag.get('href') or "#Footnote" in tag.get('href')):
                continue
            if tag.get('id') is not None and ("fn" in tag.get('id') or "Footnote" in tag.get('id') ):
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
            if "#Pg" in tag.get('href'):
                toc[tag.get("href")[1:]] = tag.text.strip()
            if "#part" in tag.get('href'):
                toc[tag.get("href")[1:]] = tag.text.strip()

    if len(entries) != len(toc):
        print("TOC entries do not match document entries")
        print(toc)
        print(entries)
        return None

    return toc

# def get_dialogue_descriptions(parsed_html, dialogue_descriptors):
#     descriptions = {}
#     for tag in parsed_html.body.find_all():
#         split = tag.text.split(':')
#         first = split[0].strip()
#         if first in dialogue_descriptors:
#             description = split[1:][0]
#             description = description.replace("\n", "").replace("\t","")
#             description = re.sub(" +", " ", description)
#             descriptions[first] = description.strip()
#     return descriptions


def get_sections(parsed_html):

    current_section, sections = '', {}

    # for section in sections
    for tag in parsed_html.body.find_all():
        if tag.name == "a" and tag.get('id') is not None and "fn" not in tag.get('id'):
            current_section = tag.get('id')
            sections[current_section] = ''
        if (tag.name == "p" and tag.text != "" and current_section != '' ):
            section_html = sections[current_section] + str(tag)
            sections[current_section] = section_html

    return sections

def convert_header_html(title, css_file, output_dir):

    title = title.upper()
    author = "Plato"
    css_file = os.path.basename(css_file)

    converted_html = f"""<head>
                            <meta http-equiv="content-type" content="text/html; charset="UTF-8">
                            <title> {title} | {author} </title>
                            <link href="{css_file}" rel="stylesheet">
                            <script type="text/javascript" src="academy.js"></script>
                        </head>"""

    return converted_html

def convert_section_paragraphs(section_html, speakers, dialogue_descriptors):

    par_num, converted_html = 0, ""

    for ptag in section_html.body.find_all('p'):

        speaker, speech, sentences_html = "", "", ""

        if ptag.text.strip() == '':
            continue

        split = ptag.text.split(':')
        first = split[0].strip()

        # Dialogue paragraph with Dialogue description
        if first in dialogue_descriptors:
            descriptor = first
            description = split[1:][0]
            description = description.replace("\n", "").replace("\t","")
            description = re.sub(" +", " ", description)
            description.strip()
            converted_html = converted_html + "<div class=\"description\">" + "<div class=\"descriptor\">" + descriptor + "</div>" + description + "</div>"

        # Dialogue paragraph w/ speaker
        elif first in speakers:
            speaker = first
            speaker_html = "<h2 class=\"speaker\">" + speaker + "</h2>"
            par_num +=1
            par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"

            speech = split[1:][0]
            clean_speech_text = speech.replace("\n", "").replace("\t","")
            clean_speech_text = re.sub(" +", " ", clean_speech_text)
            clean_speech_text.strip()

            par_sentences = nltk.sent_tokenize(clean_speech_text)
            for sentence in par_sentences:
                sentences_html = sentences_html + "<div class=\"sentence\"> " + sentence + "</div>"

            converted_html = converted_html + "<div class=\"speech\">" + par_num_html + speaker_html + sentences_html + "</div>\n"

        # Dialogue paragraph w/o speaker or dialogue description
        else:
            par_num +=1
            par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"
            par_text = ptag.text.replace("\n", "").replace("\t","")
            par_text = re.sub(" +", " ", par_text)
            par_text.strip()

            par_sentences = nltk.sent_tokenize(par_text)
            for sentence in par_sentences:
                sentences_html = sentences_html + "<div class=\"sentence\"> " + sentence + "</div>"

            converted_html = converted_html + "<div class=\"speech\">" + par_num_html + sentences_html + "</div>\n"

        sentences_html, speaker_html = "", ""

    return converted_html

def convert_toc_html(toc):

    toc_html = ''

    for tocEntry in toc:
        toc_html = toc_html + "<h3 class=\"dialogueTranslator\" lang=\"en\"><a href=\"#\" onclick='return showDiv("+ tocEntry + ")' >" + toc[tocEntry] + "</a></h3>"

    return toc_html

def convert_section_title_html(title, toc):

    return "<h2>" + toc[title] + "</h2>"

def convert_book_headings_html(file, meta_data):

    title = file.upper()
    author = "Plato"

    if (file == 'cleitophon'):
        translator = "W.R.M. Lamb"
        source = "Plato in Twelve Volumes, Vol. 9 translated by W.R.M. Lamb. Cambridge, MA, Harvard University Press; London, William Heinemann Ltd. 1925."
        copyright= "Persius Project: <a href=\"https://creativecommons.org/licenses/by-sa/3.0\">Creative Commons Attribution-ShareAlike 3.0 United States</a>"
    else:
        translator = "Translation by Jowett, Benjamin (1817-1893)"
        source = ''
        copyright = "<a href=\"https://www.gutenberg.org/cache/epub/1643/pg1643-images.html\">Guttenberg source file</a>&nbsp;and&nbsp;<a href=\"https://www.gutenberg.org/license\">©License</a>"

    headings_html = f"""<h1 class="dialogueTitle" lang="en">{title}</h1>
                        <h2 class="dialogueAuthor" lang="en"><a href="https://en.wikipedia.org/wiki/Plato">{author}</a></h2>
                        <h3 class="dialogueTranslator" lang="en">{translator}</h3>
                        <p style="padding:0px" class="dialogueCopyright"><small>{source}</small></p>
                        <p class="dialogueCopyright"><small>{copyright}</small></p>
                        """

    return headings_html

def process_file_html(dialogue, css_file, output_dir, parsed_html, dialogue_descriptors, speakers):

    meta_data = get_meta_tags(parsed_html)
    toc = get_toc(parsed_html)
    if toc is None:
        print("Entries and TOC are not the same. Skipping dialogue")
        return ""

    sections = get_sections(parsed_html)
    #print(toc)
    #print(sections.keys())

    header_html = convert_header_html(dialogue, css_file, output_dir)
    toc_html = convert_toc_html(toc)
    book_headings_html = convert_book_headings_html(dialogue, meta_data)

    converted_section_html = {}
    sections_html = ''

    for section in sections:
        original_section_html = BeautifulSoup(sections[section], 'html5lib')

        converted_section_html[section] = convert_section_paragraphs(original_section_html, speakers, dialogue_descriptors)
        section_title_html = convert_section_title_html(section, toc)
        sections_html = sections_html + f"""<div id="{section}" class="book_section">
                                                {section_title_html}
                                                {converted_section_html[section]}
                                            </div>"""

    converted_html = f"""<html>
                            {header_html}
                            <body class="default">
                                <div class="container">
                                    {book_headings_html}
                                    {toc_html}
                                    {sections_html}
                                </div>
                            </body>
                        </html>"""
    return converted_html


# TOC marker, Entry Marker; Description Marker;
dialogues = {
    # Plato
    "alcibiadesI":"./sources/plato/plato-alcibiadesI-tr-jowett-guttenberg-modified.html",# no toc, no entries
    "alcibiadesII":"./sources/plato/plato-alcibiadesII-tr-jowett-guttenberg.html",      # 
    "apology": "./sources/plato/plato-apology-tr-jowett-guttenberg.html",               # 
    "charmides":"./sources/plato/plato-charmides-tr-jowett-guttenberg.html",            # 
    "cleitophon":"./sources/plato/plato-cleitophon-tr-lamb.html",                       # 
    "cratylus":"./sources/plato/plato-cratylus-tr-jowett-guttenberg.html",              # Minor: translator in par; descriptions not parsed; add footnotes
    #"crito":"./sources/plato/plato-crito-tr-jowett-guttenberg.html",                   # MAJOR: No structure in HTML
    "crito":"./sources/plato/modified/plato-crito-tr-jowett-guttenberg-modified.html",  # 
    "critias":"./sources/plato/plato-critias-tr-jowett-guttenberg.html",                # 
    "euthydemus":"./sources/plato/plato-euthydemus-tr-jowett-guttenberg.html",          # 
    "euthyphro":"./sources/plato/plato-euthyphro-tr-jowett-guttenberg.html",            # 
    "eryxias":"./sources/plato/plato-eryxias-tr-jowett-guttenberg.html",                # 
    "gorgias":"./sources/plato/plato-gorgias-tr-jowett-guttenberg.html",                # 
    "ion":"./sources/plato/plato-ion-tr-jowett-guttenberg.html",                        # 
    "laches":"./sources/plato/plato-laches-tr-jowett-guttenberg.html",                  # Minor: PERSONS in TOC
    "laws": "./sources/plato/plato-laws-tr-jowett-guttenberg.html",                     # 
    #"lesser-hyppias":"./sources/plato/plato-lesser-hypias-tr-jowett-guttenberg.html",   # MAJOR: extra entries in TOC; entries in incorrected places in HTML
    "lesser-hyppias":"./sources/plato/modified/plato-lesser-hypias-tr-jowett-guttenberg-modified.html",   # 
    "lysis":"./sources/plato/plato-lysis-tr-jowett-guttenberg.html",                    # Minor: PERSONS toc entry
    "menexenus":"./sources/plato/plato-menexenus-tr-jowett-guttenberg.html",            # Minor: PERSONS toc entry
    "meno":  "./sources/plato/plato-meno-tr-jowett-guttenberg.html",                    # 
    "parmenides":"./sources/plato/plato-parmenides-tr-jowett-guttenberg.html",          # 
    "phaedo":"./sources/plato/plato-phaedo-tr-jowett-guttenberg.html",                  # Minor: PERSONS OF THE DIALOGUE in dialogue para
    "phaedrus":"./sources/plato/plato-phaedrus-tr-jowett-guttenberg.html",              # 
    "philebus":"./sources/plato/plato-philebus-tr-jowett-guttenberg.html",              # 
    "protagoras":"./sources/plato/plato-protagoras-tr-jowett-guttenberg.html",          # 
    "republic":"./sources/plato/plato-republic-tr-jowett-guttenberg.html",              # Minor: PERSONS in toc
    "sophist":"./sources/plato/plato-sophist-tr-jowett-guttenberg.html",                # 
    "statesman":"./sources/plato/plato-statesman-tr-jowett.html",                       # 
    "symposium":"./sources/plato/plato-symposium-tr-jowett-guttenberg.html",            # 
    "timaeus":"./sources/plato/plato-timaeus-tr-jowett-guttenberg.html",                # 
    "theaetetus": "./sources/plato/plato-theaetetus-tr-jowett-guttenberg.html",         # 
    "7thletter": "./sources/plato/plato-7thLetter-tr-bury.html",                        #

    # Aristotle
    "athenian-constitution": "./sources/aristotle/aristotle-the-athenian-constitution-tr-kenyon-guttenberg.html",   # 
    "categories": "./sources/aristotle/aristotle-the-categories-tr-edghill-guttenberg.html",                        # 
    "history-of-animals": "./sources/aristotle/aristotle-history-of-animals-tr-cresswell-guttenberg.html",          # MAJOR: inconsistent structure; index and toc anchors are same
    "nico-ethics": "./sources/aristotle/aristotle-the-nicomachean-ethics-tr-smith-ja-guttenberg.html",              # 
    "poetics-bywater": "./sources/aristotle/aristotle-on-the-art-of-poetry-tr-bywater-guttenberg.html",             # 
    "poetics-butcher": "./sources/aristotle/aristotle-the-poetics-tr-butcher-guttenberg.html",                      # 
    "treatise-on-government": "./sources/aristotle/aristotle-treatise-on-government-tr-ellis-guttenberg.html",      # 

    # Xenophon
    "memorabilia": "./sources/xenophon/xenophon-memorabilia-tr-dakyns-guttenberg.html"
}

dialogue_descriptors = [ 'PERSONS OF THE DIALOGUE', 'SCENE', 'PLACE OF THE NARRATION' ];

speakers = ['ALCIBIADES', 'ANYTUS', 'APOLLODORUS', 'ATHENIAN', 'ATHENIAN STRANGER','BOY',
            'CALLICLES', 'CHAEREPHON', 'CLEINIAS', 'COMPANION', 'CLEITOPHON', 'CRATYLUS', 'CRITIAS', 'CRITO', 'ECHECRATES',
            'ERASISTRATUS', 'ERYXIAS', 'EUCLID', 'EUDICUS', 'EUTHYPHRO', 'GORGIAS', 'HERMOCRATES', 'HERMOGENES',
            'HIPPIAS', 'ION', 'LACHES', 'LYSIMACHUS', 'MEGILLUS', 'MELESIAS', 'MENEXENUS', 'MENO', 'NICIAS',
            'PHAEDO', 'PHAEDRUS', 'PHILEBUS', 'POLUS', 'PROTARCHUS', 'SOCRATES', 'SON', 'STRANGER', 'TERPSION',
            'THEAETETUS', 'THEODORUS', 'TIMAEUS', 'YOUNG SOCRATES' ]

num_args = len(sys.argv)
if (num_args != 4 and num_args != 1):
    print("Usage Error: \n All dialogues: python beautify_plato.py all css_file output_dir \n One dialogue: python beautify_plato.py meno css_file output_dir")
    exit(1)

if (num_args == 4):
    # Check if dialogue arg valid
    if sys.argv[1] in dialogues:
        dialogues = {sys.argv[1]: dialogues[sys.argv[1]]}
    elif sys.argv[1] == 'all':
        dialogues = dialogues
    else:
        print("Usage Error: dialogue not found: use valid dialogue name or 'all' for all dialogues")
        exit(1)

    # Check css file exists
    css_file = sys.argv[2]
    #if not os.access("./" + css_file, os.R_OK):
    if not os.path.exists(css_file):
        print("Error: CSS file " + css_file + " not found or not readable")
        exit(1)

    # # Check output dir exists
    output_dir = sys.argv[3]
    if not os.path.exists(output_dir):
        print("Error: output directory " + output_dir + " not found")
        exit(1)

if (num_args == 1):
    dialogues = dialogues
    css_file = "src/plato-jowett-default.css"
    js_file = "src/academy.js"
    output_dir = "output"

for dialogue in dialogues:

    print("Processing " + dialogue + ":")
    if dialogue == 'lesser-hypias' or dialogue == 'history-of-animals':
        print("Skipping " + dialogue + ": error in original html: persons of dialogue is a toc entry")
        # print("Using modified guttenberg source:")
        continue

    f = open(dialogues[dialogue], "rb")
    parsed_html = BeautifulSoup(f, 'html5lib')
    f.close()

    converted_html = process_file_html(dialogue, css_file, output_dir, parsed_html, dialogue_descriptors, speakers)
    fout = open("output/" + dialogue + ".html", "w")
    fout.write(converted_html)
    fout.close()

shutil.copy(css_file, output_dir)
shutil.copy("src/academy.js", output_dir)

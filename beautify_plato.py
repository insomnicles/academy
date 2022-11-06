import time
import re
import nltk
#nltk.download('punkt')

try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

def getMetaTags(dialogue, metaHtmlTags):
    metaInfo = []

    for tag in metaHtmlTags:
        if tag.get('name') is not None and tag.get('content') is not None:
            metaInfo.append({ tag.get('name'): tag.get('content') })
    return metaInfo

def getToc(tocHtml):
    entries = []
    sections = {}
    toc = {}
    for tag in parsed_html.body.find_all():
        if (tag.name == "a"):
            # TOC Entry
            if tag.get('class') is not None and 'pginternal' in tag.get('class'):
                link=tag.get("href")[1:]
                toc[link] = tag.text.strip()
                sections[link] = ''
            # Section Link
            elif tag.get('id') is not None:
                entries.append(tag['id'])
    print(toc)
    print(entries)
    print(sections)
    return toc

files = {
    "alcibiadesI":"./sources/plato/plato-alcibiadesI-tr-jowett-guttenberg.html",        # no toc, no entries
    "alcibiadesII":"./sources/plato/plato-alcibiadesII-tr-jowett-guttenberg.html",      # 
    "apology": "./sources/plato/plato-apology-tr-jowett-guttenberg.html",               # 
    "charmides":"./sources/plato/plato-charmides-tr-jowett-guttenberg.html",            # 
    "cratylus":"./sources/plato/plato-cratylus-tr-jowett-guttenberg.html",              # footnotes
    "crito":"./sources/plato/plato-crito-tr-jowett-guttenberg.html",                    # id=footer
    "critias":"./sources/plato/plato-critias-tr-jowett-guttenberg.html",                # 
    "euthydemus":"./sources/plato/plato-euthydemus-tr-jowett-guttenberg.html",          # 
    "euthyphro":"./sources/plato/plato-euthyphro-tr-jowett-guttenberg.html",            # 
    "eryxias":"./sources/plato/plato-eryxias-tr-jowett-guttenberg.html",                # 
    "gorgias":"./sources/plato/plato-gorgias-tr-jowett-guttenberg.html",                # entries id (chap01) only
    "ion":"./sources/plato/plato-ion-tr-jowett-guttenberg.html",                        # 
    "laches":"./sources/plato/plato-laches-tr-jowett-guttenberg.html",                  # 
    "laws": "./sources/plato/plato-laws-tr-jowett-guttenberg.html",                     # 
    "lesser":"./sources/plato/plato-lesser-hypias-tr-jowett-guttenberg.html",           # 
    "lysis":"./sources/plato/plato-lysis-tr-jowett-guttenberg.html",                    # 
    "menexenus":"./sources/plato/plato-menexenus-tr-jowett-guttenberg.html",            # PERSONS toc entry
    "meno":  "./sources/plato/plato-meno-tr-jowett-guttenberg.html",                    # 
    "parmenides":"./sources/plato/plato-parmenides-tr-jowett-guttenberg.html",          # 
    "phaedo":"./sources/plato/plato-phaedo-tr-jowett-guttenberg.html",                  # 
    "phaedrus":"./sources/plato/plato-phaedrus-tr-jowett-guttenberg.html",              # 
    "philebus":"./sources/plato/plato-philebus-tr-jowett-guttenberg.html",              # 
    "protagoras":"./sources/plato/plato-protagoras-tr-jowett-guttenberg.html",          # 
    "republic":"./sources/plato/plato-republic-tr-jowett-guttenberg.html",              # 
    "sophist":"./sources/plato/plato-sophist-tr-jowett-guttenberg.html",                # 
    "statesman":"./sources/plato/plato-statesman-tr-jowett.html",                       # 
    "symposium":"./sources/plato/plato-symposium-tr-jowett-guttenberg.html",            # 
    "timaeus":"./sources/plato/plato-timaeus-tr-jowett-guttenberg.html",                # 
    "theaetetus": "./sources/plato/plato-theaetetus-tr-jowett-guttenberg.html"          # 
}

dialogueDescriptors = [ 'PERSONS OF THE DIALOGUE', 'SCENE', 'PLACE OF THE NARRATION' ];

characters = [
        'ALCIBIADES', 'ANYTUS', 'APOLLODORUS', 'ATHENIAN', 'ATHENIAN STRANGER','BOY',
        'CALLICLES', 'CHAEREPHON', 'CLEINIAS', 'COMPANION', 'CRATYLUS', 'CRITIAS', 'CRITO', 'ECHECRATES',
        'ERASISTRATUS', 'ERYXIAS', 'EUCLID', 'EUDICUS', 'EUTHYPHRO', 'GORGIAS', 'HERMOCRATES', 'HERMOGENES',
        'HIPPIAS', 'ION', 'LACHES', 'LYSIMACHUS', 'MEGILLUS', 'MELESIAS', 'MENEXENUS', 'MENO', 'NICIAS',
        'PHAEDO', 'PHAEDRUS', 'PHILEBUS', 'POLUS', 'PROTARCHUS', 'SOCRATES', 'SON', 'STRANGER', 'TERPSION',
        'THEAETETUS', 'THEODORUS', 'TIMAEUS', 'YOUNG SOCRATES' ]


# def getSections(toc, docHtml):
#     sections = []

#     #for tocEntry in toc:
#     #    sectionHtml = docHtml.
#     sections = toc
#     print(sections)
#     print(toc)
#     exit(1)
#     body = docHtml.descendants #find_all("body")
#     for tag in body:
#         if tag.name == "p":
#             print(tag.name)
#         elif tag.name == "a" & tag.get('id') == toc['a']:
#             print(tag.get('href'))
#             print(tag.get('id'))
#         else:
#             continue

#     exit(1)
#     tocEntry = toc[0]
#     for toc in tocEntry:
#         print (tocEntry)
#         print (toc)
#         print ("-\n")

#         toc_siblings = docHtml.find(attrs={"href":toc}).next_siblings
#         for tag in toc_siblings:
#             print(tag.name)
#             print(tag.string)
#     #for tag in docHtml.find("toc").next_siblings:
#     #if tag.name == "h1":
#     #    break
#     #else:
#     #    html += unicode(tag)
#     return sections

file = "meno"

#for file in files:
#print("\n\nProcessing " + file + "\n")

f = open(files[file], "r")
parsed_html = BeautifulSoup(f,'html5lib')

metaData = getMetaTags('meno',parsed_html.find_all('meta'))
toc = getToc(parsed_html)
#sections = getSections(toc, parsed_html)


entries = []
sections = {}
currentSection = ''

# Dialogue descriptions
#print(metaData)
#print(toc)
#print(entries)
#print(sections)

for tag in parsed_html.body.find_all():
    split = tag.text.split(':')
    first = split[0].strip()
    if first in dialogueDescriptors:
        print("descriptor:" + first)
        speech = split[1:][0]
        clean_speech = speech.replace("\n", "").replace("\t","")
        clean_speech = re.sub(" +", " ", clean_speech)
        clean_speech.strip()
        #converted_html = converted_html + "<div class=\"description\">" + "<div class=\"descriptor\">" + first + "</div>" + clean_speech + "</div>"

#id = tag.get('id') if tag.get('id') is not None else ''
        #print("id:" + id + " - " + tag.text)
        #print("entry:" + tag['id'])
        #print(tag.attrs.keys())
        #print(tag.attrs.values())
        #print(tag.text)
exit(1)
# Sections
# for section in sections
for tag in parsed_html.body.find_all():
    if tag.name == "a" and tag.get('id') is not None:
        currentSection = tag.get('id')
    if (tag.name == "p" and tag.text != "" and currentSection != '' ):
        section_html = sections[currentSection] + str(tag)
        sections[currentSection] = section_html #.update({ currentSection: section_html })


section_html = BeautifulSoup(sections["link2H_4_0003"],'html5lib')
# Convert to Formatted HTML

par_num = 0
title = "Meno"
author = "Plato"
source_url = "http://"
dialogue_url = "http://"
css_file = "output/plato-jowett-default.css"
# $metaTagsHtml
converted_html = "<html> \
                    <head>\
                        <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"> \
                        <title>" + title + " | " + author + "</title> \
                        <meta charset=\"utf-8\"> \
                        <link href=\"output/plato-jowett-default.css\" rel=\"stylesheet\"> \
                    </head> \
                <body class=\"default\"> \
                <div class=\"container\">";

for ptag in section_html.body.find_all('p'):
    speaker = ""
    speech = ""
    sentences_html = ""

#    if ptag.text == '':
#        continue

    split = ptag.text.split(':')
    first = split[0].strip()

    # Dialogue paragraph with Dialogue description
    if first in dialogueDescriptors:
        speech = split[1:][0]
        #print(speech)
        #exit(1)
        clean_speech = speech.replace("\n", "").replace("\t","")
        clean_speech = re.sub(" +", " ", clean_speech)
        clean_speech.strip()
        converted_html = converted_html + "<div class=\"description\">" + "<div class=\"descriptor\">" + first + "</div>" + clean_speech + "</div>"

    # Dialogue paragraph w/ speaker
    elif (first in characters):
        speaker_html = "<h2 class=\"speaker\">" + first + "</h2>"
        par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"

        #paragraph text i.e. text of speaker
        speech = split[1:][0]
        clean_speech_text = speech.replace("\n", "").replace("\t","")
        clean_speech_text = re.sub(" +", " ", clean_speech_text)
        clean_speech_text.strip()

        par_sentences = nltk.sent_tokenize(clean_speech_text)
        for sentence in par_sentences:
            sentences_html = sentences_html + "<div class=\"sentence\"> " + sentence + "</div>"

        #converted_speech_html = "<p class=\"speech\">" + clean_speech + "</p>"
        #speech.join(split[1:])
        converted_html = converted_html + "<div class=\"speech\">" + par_num_html + speaker_html + sentences_html + "</div>\n"
        par_num +=1

    # Dialogue paragraph w/o speaker or dialogue description
    else:
        par_num_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"
        clean_speech_text = ptag.text.replace("\n", "").replace("\t","")
        clean_speech_text = re.sub(" +", " ", clean_speech_text)
        clean_speech_text.strip()

        par_sentences = nltk.sent_tokenize(clean_speech_text)
        for sentence in par_sentences:
            sentences_html = sentences_html + "<div class=\"sentence\">" + sentence + "</div>"

        converted_html = converted_html + "<div class=\"speech\">" + par_num_html + sentences_html + "</div>\n"
        par_num += 1

    sentences_html = ''
    speaker_html = ''

converted_html = converted_html + '</div></body></html>'

f = open("test.html", "w")
f.write(converted_html)
f.close()

#print(converted_html)
#print(ptag)
#time.sleep(1)
#print(parsed_html.body.find('div', attrs={'class':'container'}).text)
#print(f.read())
#css_filename = "./css/greek-learner-text.css"
#output_filename = "./output/plato-meno-py-formatted.html"
#$parNumFormatted = str_pad($paragraphNum, 3, '0', STR_PAD_LEFT);
#$speakerH2 = ($speaker != "") ? "<h2 class=\"speaker\">" . $speaker . "</h2>" : '';
#$parHtml = '';
#foreach ($parSentences as $sentence)
#   $parHtml .= "<div class=\"sentence\">" . $sentence . "&nbsp;</div>";
#   $parDiv = "<div class=\"speech\">
#       <span class=\"ref\">" . $parNumFormatted . "</span>" .
#       $speakerH2 .
#       $parHtml .
#       "</div>";
# return $parDiv;
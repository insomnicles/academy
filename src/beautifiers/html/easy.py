from ..beautifier import Beautifier
import shutil
import logging
import os

class EasyBeautifier (Beautifier):
    src_css_file = "css/easy.css"
    src_js_file = "js/reader.js"
    src_icons_dir = "images/icons/"
    output_css_dir = "css/"
    output_js_dir = "js/"

    def __init__(self) -> None:
        logging.info("Created Easy Beautifier")

    def create_doc(self) -> None:
        header_html = self.create_header_html()
        nav_html = self.create_nav_html()
        explanation_html = self.create_explanation_html()
        headings_html = self.create_headings_html()
        toc_html = self.create_toc_html()
        sections_html = self.create_sections_html()

        self.created_doc = f"""<html>
                                    {header_html}
                                    <body>
                                        <div id="book_reader_container" >
                                            {nav_html}
                                            <div class="book_reader">
                                                {explanation_html}
                                                <div class="book_container">
                                                    {headings_html}
                                                    {toc_html}
                                                    {sections_html}
                                                </div>
                                            </div>
                                        </div>
                                    </body>
                                </html>"""

    def create_header_html(self) -> str:
        if not self.metadata:
            raise ValueError('No metadata found: cannot create header')

        title = self.metadata['dc.title']
        author = self.metadata['dc.creator'] #.split(',')[0]
        meta_tags = ""

        output_css_file = self.output_css_dir + os.path.basename(self.src_css_file)
        output_js_file = self.output_js_dir + os.path.basename(self.src_js_file)

        for meta_tag_key in self.metadata:
            meta_tags += f"""<meta name="{meta_tag_key}" content="{self.metadata[meta_tag_key]}">\n"""

        return f""" <head>
                        <meta http-equiv="content-type" content="text/html; charset="UTF-8">
                        {meta_tags}
                        <title> {title} | {author} </title>
                        <link href="{output_css_file}" rel="stylesheet">
                        <script type="text/javascript" src="{output_js_file}"></script>
                    </head>
                """

    def create_nav_html(self) -> str:
        return f""" <div id="book_reader_nav" onload="navSetup()">
                        <a href="/">Aquarium</a>
                        <a href="#" onclick="return showToc()" ><img class="nav_img filter-nav" src="images/icons/toc.svg" /></a>
                        <a href="#" onclick="return firstSection()" ><img class="nav_img filter-nav" src="images/icons/navigate_skip_previous.svg" /></a>
                        <a href="#" onclick="return previousSection()" ><img class="nav_img filter-nav" src="images/icons/navigate_previous.svg" /></a>
                        <a href="#" onclick="return nextSection()" ><img class="nav_img filter-nav" src="images/icons/navigate_next.svg" /></a>
                        <a href="#" onclick="return lastSection()" ><img class="nav_img filter-nav" src="images/icons/navigate_skip_next.svg" /></a>
                        <a href="#" onclick="return showExplanations()" ><img class="nav_img filter-nav" src="images/icons/quick_ref.svg" /></a>
                        <a href="#" onclick="return hideRefs()" ><img class="nav_img filter-nav" src="images/icons/info.svg" /></a>
                        <a href="#" onclick="return formatSize()" ><img class="nav_img filter-nav" src="images/icons/format_size.svg" /></a>
                        <a href="#" onclick="return darklightMode('dark')" ><img id="link_dark_mode" class="nav_img filter-nav" src="images/icons/dark_mode.svg" /></a>
                        <a href="#" onclick="return darklightMode('light')" ><img id="link_light_mode" class="nav_img filter-nav" style="display:none;" src="images/icons/light_mode.svg" /></a>
                    </div>
                """

    def create_headings_html(self) -> str:
        if not self.metadata:
            raise ValueError('No metadata found: cannot create headings')

        title_html, author_html, translator_html, source_html, license_html = "", "", "", "", ""

        title = self.metadata['dc.title'] or ""
        author = self.metadata['dc.creator'] or ""
        translator = self.metadata['marcrel.trl'] or ""
        source = self.metadata['dcterms.source'] or ""
        license = self.metadata['source_licence_url'] or ""

        if title != "": title_html = f"""<h1 class="book_title" lang="en">{title}</h1>"""
        if author != "": author_html = f"""<h2 class="book_author" lang="en"><a href="#">{author}</a></h2>"""
        if translator != "": translator_html = f"""<h3 class="book_translator" lang="en">Translated by {translator}</h3>"""
        if source != "": source_html = f"""<small><a href="{source}">Source</a></small>"""
        if license != "": license_html = f"""<a href="{license}"><small>© License</a></small>"""

        return f""" {title_html}
                    {author_html}
                    {translator_html}
                    <p class="book_source_and_license" >{source_html}&nbsp;and&nbsp;{license_html}</p>
                """

    def create_toc_html(self) -> str:
        if not self.toc:
            return '<div class="book_toc"></div>'

        toc_html = f"""<div class="book_toc">"""
        if self.toc['table_html'] != "":
            toc_html += f"""<h3 class="book_toc_entry" lang="en">
                                <a href="#" onclick="return showSection('toc')" >Table of Contents</a>
                            </h3> """
        for toc_entry in self.toc['toc']:
            toc_html += f"""<h3 class="book_toc_entry" lang="en">
                                <a href="#" onclick="return showSection('{toc_entry}')" >{self.toc['toc'][toc_entry]}</a>
                            </h3>"""
        toc_html += "</div>"
        # toc_html += self.toc['table_html']
        return toc_html

    def create_explanation_html(self) -> str:
        return f""" <div class="explanation_container">
                        <div class="explanation">
                            <div class="definiendum">Alcibiades</div>
                            <div class="definiens">
                                <a href="https://en.wikipedia.org/wiki/Alcibiades">Wiki</a>a prominent Athenian statesman, orator, and general. He was the last of the Alcmaeonidae, which fell
                                from prominence after the Peloponnesian War. He played a major role in the second half of that conflict as a strategic advisor, military commander, and politician.
                            </div>
                        </div>
                    </div>
                """

    def create_heading_html(self, section_id, par_id) -> str:
        heading = self.body[section_id][par_id]['heading']

        return f"""<h2>{heading}</h2>\n"""

    def create_description_html(self, section_id, par_id) -> str:
        descriptor = self.body[section_id][par_id]["descriptor"]
        description = self.body[section_id][par_id]["description"]

        return f""" <div class="book_description">
                        <strong>{descriptor}</strong>:{description}
                    </div>
                """

    def create_ref_html(self, par_num) -> str:
        ref_num = str(par_num).zfill(3)
        return f""" <span class="ref"> {ref_num} </span>"""

    def create_pre_html(self, section_id, par_id, par_num) -> str:
        sentences = self.body[section_id][par_id]['sentences'][0]
        ref_html = self.create_ref_html(par_num)
        return f""" <div class="pre">
                        {ref_html}
                        <pre> {sentences} </pre>
                    </div>
                """

    def create_poem_html(self, section_id, par_id, par_num) -> str:
        lines_html = ""

        ref_html = self.create_ref_html(par_num)
        for line in self.body[section_id][par_id]["lines"]:
            lines_html += line + "<br>"

        return f""" <div class="poem">
                        {ref_html}
                        {lines_html}
                    </div>
                """

    def create_speech_html(self, section_id, par_id, par_num) -> str:
        sentences_html = ""

        ref_html = self.create_ref_html(par_num)
        speaker = self.body[section_id][par_id]['speaker']
        sentences = self.body[section_id][par_id]['sentences']

        for sentence in sentences:
            sentences_html += f"""<div class="sentence">{sentence}</div>"""

        return f""" <div class="speech">
                        {ref_html}
                        <div class="speaker">{speaker}</div>
                        <div class="speech_text">
                            {sentences_html}
                        </div>
                    </div>
                """

    def create_text_par_html(self, section_id, par_id, par_num) -> str:
        sentences_html = ""
        ref_html = self.create_ref_html(par_num)
        sentences = self.body[section_id][par_id]['sentences']
        for sentence in sentences:
            sentences_html += f"""<div class="sentence"> {sentence}</div>"""

        return f""" <div class="text">
                        {ref_html}
                        {sentences_html}
                    </div>
                """

    def create_images_html(self, section_id, par_id) -> str:
        images_html = ""

        images = self.body[section_id][par_id]['images']
        if not images:
            return ""

        for image in images:
            figcaption_html = ""
            img = images[image]
            id = img['id'] or 0
            src = img['src'] or ""
            alt = img['alt'] or ""
            caption = img['caption'] or ""
            height = img['height'] or 400
            width = img['width'] or 400

            images_html += f""" <img class="book_image" id="{id}" src="{src}" alt="{alt}" width="{width}" height="{height}">"""
            if caption != "":
                images_html += f""" <figcaption class="image_caption">{caption}</figcaption>"""


        return f""" <div class="image_container">
                        {images_html}
                    </div>
                """

    def create_footnotes_html(self, section_id, par_id) -> str:
        footnotes = self.body[section_id][par_id]['footnotes']
        if not footnotes:
            return ""
        return f""""""

    def par_has(self, type, section_id, par_id) -> bool:
        return type in self.body[section_id][par_id]

    def create_sections_html(self) -> str:
        par_num = 0
        sections_html = ""

        if self.toc['table_html'] != "":
            sections_html += f"""   <div id="toc" class="book_section">
                                        {self.toc['table_html']}
                                    </div>
                                """

        for section_id in self.body:
            sec_html = ""
            for par_id in self.body[section_id]:
                type = self.body[section_id][par_id]['type']

                if (type == "heading"):
                    sec_html += self.create_heading_html(section_id, par_id)
                elif (type == "descriptor"):
                    sec_html += self.create_description_html(section_id, par_id)
                elif (type == "pre"):
                    sec_html += self.create_pre_html(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "poem"):
                    sec_html += self.create_poem_html(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "text"):
                    sec_html += self.create_text_par_html(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "speech"):
                    sec_html += self.create_speech_html(section_id, par_id, par_num)
                    par_num +=1
                else:
                    raise Exception("type not found:" + type)

                # Add Images, Footnotes
                if self.par_has('images', section_id, par_id):
                    sec_html += self.create_images_html(section_id, par_id)
                if self.par_has('footnotes', section_id, par_id):
                    sec_html += self.create_footnotes_html(section_id, par_id)
            sections_html += f"""<div id="{section_id}" class="book_section">
                                    {sec_html}
                                </div>"""
        return sections_html

    def save(self, output_dir, filename = ""):
        if not self.created_doc:
            raise Exception("Error nothing to save: no html was created")

        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
        output_images_dir = output_dir + "images"
        output_icon_dir = output_dir + "images/icons"
        css_dir = output_dir + "css"
        js_dir = output_dir + "js"

        output_file = output_dir + self.src['filename'] if filename == "" else output_dir + filename

        os.makedirs(output_dir, exist_ok=True)
        os.makedirs(css_dir, exist_ok=True)
        os.makedirs(js_dir, exist_ok=True)
        os.makedirs(output_images_dir, exist_ok=True)
        os.makedirs(output_icon_dir, exist_ok=True)

        try:
            fout = open(output_file, "w")
            fout.write(self.created_doc)
            fout.close()
            self.reset()

            c_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
            src_icons_dir = c_dir + "icons/"
            shutil.copy(c_dir + self.src_css_file, css_dir);
            shutil.copy(c_dir + self.src_js_file, js_dir);
            if os.path.exists(src_icons_dir):
                shutil.copytree(src_icons_dir, output_icon_dir, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
            logging.info("Easy Beautification Complete.")
        except FileNotFoundError as e:
            print("Error: File not found.")
            print(e)
            logging.debug(e)
            exit(1)
        except Exception as e:
            print("Error: could not write file.")
            print(e)
            logging.debug(e)
            exit(1)

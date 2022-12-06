import shutil
import os

class Prettifier:
    created_header_html, created_headings_html, created_toc_html, created_sections_html, created_page_html = "", "", "", "", ""
    src, metadata, toc, body = {}, {}, {}, {}
    DEBUG = False

    def __init__(self):
        print("Created creator") if self.DEBUG else True
        pass

    def create(self, structured_doc):
        self.src = structured_doc['src']
        self.metadata = structured_doc['metadata']
        self.toc = structured_doc['toc']
        self.body = structured_doc['body']

        self.create_header_html()
        self.create_headings_html()
        self.create_toc_html()
        self.create_sections_html()
        self.create_page_html()

    def save(self, output_dir, filename = ""):
        if not self.created_page_html:
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
            fout.write(self.created_page_html)
            fout.close()
            self.reset()
        except FileNotFoundError as e:
            print("FIle not found error")
            print(e)
        except Exception as e:
            print("Error: could not write html file")
            print(e)
            return

        try:
            shutil.copy(self.src_css_file, css_dir);
            shutil.copy(self.src_js_file, js_dir);
            shutil.copy(self.src_icons_dir + "toc.svg",         output_icon_dir);
            shutil.copy(self.src_icons_dir + "format_size.svg", output_icon_dir);
        except FileNotFoundError as e:
            print("File not found")
        except Exception as e:
            print("Could not copy file")
            print(e)
            return
        return True

    def reset(self):
        self.created_header_html, self.created_headings_html, self.created_toc_html, self.created_sections_html, self.created_page_html = "", "", "", "", ""
        self.src, self.metadata, self.toc, self.body = {}, {}, {}, {}

class EasyPrettifier (Prettifier):
    src_css_file = "src/css/easy.css"
    src_js_file = "src/js/reader.js"
    src_icons_dir = "src/images/icons/"
    output_css_dir = "css/"
    output_js_dir = "js/"

    def __init__(self) -> None:
        print("Created EasyPrettifier") if self.DEBUG else True

    def create_page_html(self) -> str:
            navigator = f"""
                <div id="book_reader_nav">
                    <a class="site_name" href="/">Site.com</a>
                    <a href="#" onclick="return formatSize()"><img class="nav_img filter-nav" src="./images/icons/format_size.svg" /></a>
                    <a href="#" onclick="return showToc()"><img class="nav_img filter-nav" src="./images/icons/toc.svg" /></a>
                </div>"""
            explanation_container = f"""
                <div class="explanation_container">
                    <div class="explanation">
                        <div class="definiendum">Alcibiades</div>
                        <div class="definiens">
                            <a href="https://en.wikipedia.org/wiki/Alcibiades">Wiki</a>a prominent Athenian statesman, orator, and general. He was the last of the Alcmaeonidae, which fell
                            from prominence after the Peloponnesian War. He played a major role in the second half of that conflict as a strategic advisor, military commander, and politician.
                        </div>
                    </div>
                </div>"""
            self.created_page_html = f"""<html>
                                            {self.created_header_html}
                                            <body>
                                                <div id="book_reader_container" >
                                                    {navigator}
                                                    <div class="book_reader">
                                                        {explanation_container}
                                                        <div class="book_container">
                                                            {self.created_headings_html}
                                                            {self.created_toc_html}
                                                            {self.created_sections_html}
                                                        </div>
                                                    </div>
                                                </div>
                                            </body>
                                        </html>"""

    def create_header_html(self) -> str:
        if not self.metadata:
            raise ValueError('No metadata found: cannot create header')

        title = self.metadata['dc.title']
        author = self.metadata['dc.creator'].split(',')[0]
        meta_tags = ""

        output_css_file = self.output_css_dir + os.path.basename(self.src_css_file)
        output_js_file = self.output_js_dir + os.path.basename(self.src_js_file)

        for meta_tag_key in self.metadata:
            meta_tags += f"""<meta name="{meta_tag_key}" content="{self.metadata[meta_tag_key]}">\n"""

        self.created_header_html =f"""<head>
                                        <meta http-equiv="content-type" content="text/html; charset="UTF-8">
                                        {meta_tags}
                                        <title> {title} | {author} </title>
                                        <link href="{output_css_file}" rel="stylesheet">
                                        <script type="text/javascript" src="{output_js_file}"></script>
                                    </head>"""

    def create_headings_html(self) -> str:
        if not self.metadata:
            raise ValueError('No metadata found: cannot create headings')

        title = self.metadata['dc.title']
        author = self.metadata['dc.creator'].split(',')[0]
        translator = self.metadata['marcrel.trl']
        source = self.metadata['source_url']
        copyright = self.metadata['source_licence_url']
        self.created_headings_html = f"""<h1 class="book_title" lang="en">{title}</h1>
                                         <h2 class="book_author" lang="en"><a href="https://en.wikipedia.org/wiki/{author}">{author}</a></h2>
                                         <h3 class="book_translator" lang="en">{translator}</h3>
                                         <p class="book_source_and_license" ><small><a href="{source}">Source</a>&nbsp;and&nbsp;<a href="{copyright}">©License</a></small></p>"""

    def create_toc_html(self) -> str:
        if not self.toc:
            return '<div class="book_toc"></div>'

        toc_html = "<div class=\"book_toc\">"
        for toc_entry in self.toc:
            toc_html += f"""<h3 class="book_toc_entry" lang="en">
                                <a href="#" onclick="return showDiv('{toc_entry}')" >{self.toc[toc_entry]}</a>
                            </h3>"""
        toc_html += "</div>"
        self.created_toc_html = toc_html

    def create_sections_html(self) -> str:
        par_num = 0
        section_num = 0
        section_html = ""

        for section_id in self.body:
            par_html = ""
            section_html += "<div id=\"" + section_id + "\" class=\"book_section\">"
            section_html += "<h2>" + self.toc[section_id] + "</h2>"

            for par_id in self.body[section_id]:
                par_html,sentences_html, ref_html, speaker = "", "", "", ""

                type = self.body[section_id][par_id]['type']
                par_num +=1
                ref_html = "<span class=\"ref\">" + str(par_num).zfill(3) + "</span>"

                sentences = self.body[section_id][par_id]['sentences']
                for sentence in sentences:
                    sentences_html += "<div class=\"sentence\">" + sentence + "</div>"

                if (type == "text"):
                    par_html += "<div class=\"text\">" + ref_html + sentences_html + "</div>"
                elif (type == "speech"):
                    speaker = self.body[section_id][par_id]["speaker"]
                    par_html += "<div class=\"speech\">" + ref_html + "<div class=\"speaker\">" + speaker + "</div>"
                    par_html += "<div class=\"speech_text\">" + sentences_html + "</div>"
                    par_html += "</div>"
                else:
                    raise Exception("type not found:" + type)
                section_html += par_html + "\n"
            section_html += "</div>\n"
        self.created_sections_html = section_html

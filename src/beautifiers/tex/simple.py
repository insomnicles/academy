from ..beautifier import Beautifier
import shutil
import os
import logging

class SimpleBeautifier(Beautifier):
    src_icons_dir = "images/icons/"
    created_tex = ""

    def __init__(self) -> None:
        logging.info("Created Latex Beautifier")

    def create_doc(self) -> None:
        header = self.create_header()
        title_page = self.create_title_page()
        toc = self.create_toc()
        sections = self.create_sections()

        self.created_tex = f"""
\\documentclass[11pt,letter]{{article}}
{header}
{title_page}
{toc}
{sections}
\end{{document}}"""
        logging.info("Beautification Complete")

#\\usepackage{{fontawesome,url}}
# \\usepackage{{tocloft}}
# \\usepackage[stable]{{footmisc}}
# \\usepackage{{color}}
# \\usepackage{{hyperref}}
# \\hypersetup{{colorlinks=true, linktoc=all, linkcolor=black }}
# \\setlength\\cftparskip{{-2pt}}
# \\setlength\\cftbeforechapskip{{-1pt}}
# \\setcounter{{chapter}}{{1}}
# \\setcounter{{section}}{{1}}
# \\setcounter{{secnumdepth}}{{0}}
# \\setlength{{\parskip}}{{5pt}}
# \\setlength{{\parindent}}{{0pt}}
# \\setlength{{\columnsep}}{{30pt}}
# \\usepackage{{blindtext}}

    def create_header(self) -> str:
        temp = f"""

\\begin{{document}}"""
        return temp

    def create_title_page(self) -> str:
        if not self.metadata:
            raise ValueError('No metadata found: cannot create headings')

        title = self.metadata['dc.title'] or ""
        author = self.metadata['dc.creator'] or ""
        translator = self.metadata['marcrel.trl'] or ""
        source = self.metadata['dcterms.source'] or ""
        license = self.metadata['source_licence_url'] or ""
        return f"""
\\title{{{title}\\thanks{{Source: {source}. License: {license} ds}}}}
\\date{{\\today}}
\\author{{{author}\\\\ Translated by {translator}}}
\\maketitle
"""

    def create_toc(self) -> str:
        return r"""\setcounter{tocdepth}{1}
\tableofcontents
\renewcommand{\baselinestretch}{1.0}
\normalsize
\newpage
"""

    def create_heading(self, section_id, par_id) -> str:
        heading = self.body[section_id][par_id]['heading']
        return f"""\\section{{{heading}}}"""

    def create_description(self, section_id, par_id) -> str:
        descriptor = self.body[section_id][par_id]["descriptor"]
        description = self.body[section_id][par_id]["description"]

        return f""" """

    def create_ref(self, par_num) -> str:
        ref_num = str(par_num).zfill(3)
        return f""" """

    def create_pre(self, section_id, par_id, par_num) -> str:
        sentences = self.body[section_id][par_id]['sentences'][0]
        ref = self.create_ref(par_num)
        return f""" """

    def create_poem(self, section_id, par_id, par_num) -> str:
        lines = ""

        ref = self.create_ref(par_num)
        for line in self.body[section_id][par_id]["lines"]:
            lines += line + "<br>"

        return f""" """

    def create_speech(self, section_id, par_id, par_num) -> str:
        sentences_tex = ""

        #  ref = self.create_ref(par_num)
        speaker = self.body[section_id][par_id]["speaker"]
        sentences = self.body[section_id][par_id]['sentences']

        for sentence in sentences:
            sentences_tex += " " + sentence

        return f"""
\\par \\textbf{{{speaker}}}
\\par {sentences_tex}
"""

    def create_text_par(self, section_id, par_id, par_num) -> str:
        sentences_tex = ""
        # ref = self.create_ref(par_num)
        sentences = self.body[section_id][par_id]['sentences']
        for sentence in sentences:
            sentences_tex += " " + sentence

        return f"""
\\par {sentences_tex}
"""

    def create_images(self, section_id, par_id) -> str:
        images_tex = ""

        images = self.body[section_id][par_id]['images']
        if not images:
            return ""

        for image in images:
            figcaption = ""
            img = images[image]
            id = img['id'] or 0
            src = img['src'] or ""
            alt = img['alt'] or ""
            caption = img['caption'] or ""
            height = img['height'] or 400
            width = img['width'] or 400

            images_tex += f""""""
            if caption != "":
                images_tex += f""""""

        return f""" """

    def create_footnotes(self, section_id, par_id) -> str:
        footnotes = self.body[section_id][par_id]['footnotes']
        if not footnotes:
            return ""
        return f""""""

    def par_has(self, type, section_id, par_id) -> bool:
        return type in self.body[section_id][par_id]

    def create_sections(self) -> str:
        par_num = 0
        sections_tex = ""

        # if self.toc['table_html'] != "":
        #     sections_tex += f""" {self.toc['table_html']}"""

        for section_id in self.body:
            sec_tex = ""
            for par_id in self.body[section_id]:
                type = self.body[section_id][par_id]['type']

                if (type == "heading"):
                    sec_tex += self.create_heading(section_id, par_id)
                elif (type == "descriptor"):
                    sec_tex += self.create_description(section_id, par_id)
                elif (type == "pre"):
                    sec_tex += self.create_pre(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "poem"):
                    sec_tex += self.create_poem(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "text"):
                    sec_tex += self.create_text_par(section_id, par_id, par_num)
                    par_num +=1
                elif (type == "speech"):
                    sec_tex += self.create_speech(section_id, par_id, par_num)
                    par_num +=1
                else:
                    raise Exception("type not found:" + type)

                # Annotation: images, footnotes
                if self.par_has('images', section_id, par_id):
                    sec_tex += self.create_images(section_id, par_id)
                if self.par_has('footnotes', section_id, par_id):
                    sec_tex += self.create_footnotes(section_id, par_id)
            sections_tex += sec_tex
        return sections_tex

    def save(self, output_dir, filename = ""):
        if not self.created_tex:
            raise Exception("Error nothing to save: no tex was created")

        curr_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
        src_images_dir = curr_dir + "images/"

        output_dir = output_dir if output_dir[-1] == "/" else output_dir + "/"
        output_images_dir = output_dir + "images"
        if filename == "":
            filename = self.src['filename'].split(".")[0]
            filename_tex = filename + '.tex'
        output_file = output_dir + filename_tex

        try:
            os.makedirs(output_dir, exist_ok=True)
            fout = open(output_file, "w")
            fout.write(self.created_tex)
            fout.close()

            pdfshellcmd = "pdflatex -synctex=1 -interaction=nonstopmode -output-directory " + output_dir + " " + output_file
            print(pdfshellcmd)

            os.system(pdfshellcmd)
            os.system(pdfshellcmd)

            output_filename = output_dir + filename
            shellcmd = "rm " + output_filename + '.log && rm ' + output_filename + '.aux && rm ' + output_filename + '.toc && rm ' + output_filename + '.synctex.gz'
            os.system(shellcmd)
            self.reset()
        except FileNotFoundError as e:
            print("Beautifier Error: " + output_file + " not found.")
            logging.debug(e)
            exit(1)
        except Exception as e:
            print("Beautifier Error: could not write to " + output_file)
            logging.debug(e)
            exit(1)

        try:
            os.makedirs(output_images_dir, exist_ok=True)
            shutil.copytree(src_images_dir, output_images_dir, symlinks=False, ignore=None, ignore_dangling_symlinks=False, dirs_exist_ok=True)
        except FileNotFoundError as e:
            logging.info("Beautifier could not copy images from  " + src_images_dir)
            return
        except Exception as e:
            print("Beautifier Error: could not write to " + output_file)
            logging.debug(e)
            exit(1)

        logging.info("Tex file saved")

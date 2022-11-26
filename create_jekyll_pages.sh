#!/bin/bash

##################################################
#
# Creates Jekyll Pages from Book Reader Html Files
#
##################################################

SOURCE_HTML_FILES=output
SOURCE_CSS=output/css
SOURCE_JS=output/js
SOURCE_IMG=output/images/icons
OUTPUT_DIR=jekyll-pages
TARGET_JEKYLL_HOME=../insomnicles.github.io
JEKYLL_LAYOUT="book"

mkdir ${OUTPUT_DIR}

html_files=`ls ./${SOURCE_HTML_FILES}/*.html | cut -d / -f 3 | cut -d . -f 1`

for filename in $html_files
do
    if [ "$filename" == "nico-ethics" -o "$filename" == "treatise-on-government" -o "${filename}" == "poetics-butcher" -o "${filename}" == "poetics-bywater" -o "${filename}" == "athenian-constitution" -o "${filename}" == "history-of-animals" ]; then
        author="aristotle"
    elif [ ${filename} == "memorabilia" ]
    then
        author="xenophon"
    else
        author="plato"
    fi
    echo "---
layout: ${JEKYLL_LAYOUT}
permalink: /${author}/${filename}
---
" > "${OUTPUT_DIR}/"$filename".md"
    awk '/book_reader_container/,/\/body/' ${SOURCE_HTML_FILES}/"$filename".html | head -n -1 | sed 's/.\/images\/icons/{{ site.url }}\/images\/icons/g' | sed 's/^[ \t]*//' >> "${OUTPUT_DIR}/"$filename".md"

    echo "Copying ${OUTPUT_DIR}/${filename}.md to ${TARGET_JEKYLL_HOME}/pages/${author}"
    cp "${OUTPUT_DIR}/${filename}.md" "${TARGET_JEKYLL_HOME}/pages/${author}"
done

cp ${SOURCE_CSS}/academy.css ${TARGET_JEKYLL_HOME}/public/css
cp ${SOURCE_JS}/academy.js ${TARGET_JEKYLL_HOME}/public/js
cp ${SOURCE_IMG}/*.svg ${TARGET_JEKYLL_HOME}/images/icons

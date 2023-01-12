#!/bin/bash

##################################################
#
# Creates Jekyll Pages from Book Reader Html Files
#
##################################################

SOURCE_HTML_FILES=output/insomnicles
SOURCE_CSS=output/insomnicles/css/easy.css
SOURCE_JS=output/insomnicles/js/reader.js
SOURCE_IMG=output/insomnicles/images/icons/*
OUTPUT_DIR=output/jekyll-pages
TARGET_JEKYLL_HOME=../../insomnicles.github.io
JEKYLL_LAYOUT="book"

mkdir ${OUTPUT_DIR}

html_files=`ls -l ./${SOURCE_HTML_FILES}/*.html | cut -d / -f 4 | cut -d . -f 1`

for filename in $html_files
do
    printf ${filename}
    if [ "$filename" == "nico-ethics" -o "$filename" == "treatise-on-government" -o "${filename}" == "poetics-butcher" -o "${filename}" == "poetics-bywater" -o "${filename}" == "athenian-constitution" -o "${filename}" == "history-of-animals" ]; then
        author="aristotle"
    else
        author="plato"
    fi
    echo "---
layout: ${JEKYLL_LAYOUT}
permalink: /academy/${author}/${filename}
---
" > "${OUTPUT_DIR}/"$filename".md"
    awk '/book_reader_container/,/\/body/' ${SOURCE_HTML_FILES}/"$filename".html | head -n -1 | sed 's/images\/icons/{{ site.url }}\/images\/icons/g' | sed 's/^[ \t]*//' >> "${OUTPUT_DIR}/"$filename".md"


    echo "Copying ${OUTPUT_DIR}/${filename}.md to ${TARGET_JEKYLL_HOME}/pages/academy/${author}"
    cp "${OUTPUT_DIR}/${filename}.md" "${TARGET_JEKYLL_HOME}/pages/academy/${author}"
done

cp ${SOURCE_CSS} ${TARGET_JEKYLL_HOME}/public/css
cp ${SOURCE_JS} ${TARGET_JEKYLL_HOME}/public/js
cp ${SOURCE_IMG} ${TARGET_JEKYLL_HOME}/images/icons

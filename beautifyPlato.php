<?php

/**
 * beautifyPlato
 *
 * Beautifies Plato's Works, translated by Benjamin Jowett, from Guttenberg Project
 *
 * The function takes the location of the html file and a css file and creates a beautiful html file
 *
 * @param  string   $file       location of dialogue html file: must be a Guttenberg Plato book, Jowett translation only
 * @param  string   $cssFile    location of the css file
 * @param  string   $outputFile location and name of output file
 * @return void
 * @todo 1. Fix: Dialogues that contain errors
 *              Menexius:   introduction prepended; "Person of Dialogue" appears in TOC, which screws things up
 *              Laches:     introduction prepended; "Person of Dialogue" appears in TOC, which screws things up
 *              Lysis:      introduction prepended; "Person of Dialogue" appears in TOC, which screws things up
 *              Cratylus:   first line -- Translated by Benjamin Jowett -- should not be there; rest is good
 *              Apology:    no text at all
 *              Crito:      first 8 lines are from the introduction
 *              Republic:   introduction prepended; books not separated;
 *              Critias:    missing last line: "* The rest of the Dialogue of Critias has been lost."               [hardcode]
 *              Laws:       books not separated;
 *       2. Fix: concate content if more than one in meta tags, for example subject tag
 *       3. Add persons, place, narrrative at start of dialogue
 *       4. PHP Warning: undefined array
 *       5. PHP Warning: tag section invalid in DomDocument
 *       6. add class names in CSS file for title, author, translator, etc.
 *       Note: DomNode->nodeValue = textContent
 */

function beautifyPlato(string $file, string $cssFile, string $outputFile)
{
    $dom = new DomDocument();
    $htmlDoc = file_get_contents($file);
    $dom->loadHTML($htmlDoc);
    $xpath = new DOMXPath($dom);
    $headerNodes = $xpath->query('/html/head/*');

    $title = $author = $translator = '';
    $metaTagNames = [
        'dc.title',
        'dc.language',
        'dcterms.source',
        'dcterms.modified',
        'dc.rights',
        'dc.creator',
        'marcrel.trl',
        'dc.subject',
        'dcterms.created',
        'generator'
    ];
    $metaData = [];
    foreach ($headerNodes as $meta) {
        $name = $meta->getAttribute('name');
        $content = $meta->getAttribute('content');
        if (in_array($name, $metaTagNames))
            $metaData[$name] = $content;
    }

    $nodes = $xpath->query('/html/body//*');

    // Variable initialization
    $dialogueStart = $dialogueEnd = false;
    $persons = $scene = $place = $placeOfNarration = '';
    $speaker = $speech = '';
    $speechNo = 1;
    $textInHtml = '';
    $speakers = [
        'ANYTUS',
        'APOLLODORUS',
        'ATHENIAN',
        'ATHENIAN STRANGER',
        'BOY',
        'CALLICLES',
        'CHAEREPHON',
        'CLEINIAS',
        'COMPANION',
        'CRATYLUS',
        'CRITIAS',
        'CRITO',
        'ECHECRATES',
        'ERASISTRATUS',
        'ERYXIAS',
        'EUCLID',
        'EUDICUS',
        'EUTHYPHRO',
        'GORGIAS',
        'HERMOCRATES',
        'HERMOGENES',
        'HIPPIAS',
        'ION',
        'LACHES',
        'LYSIMACHUS',
        'MEGILLUS',
        'MELESIAS',
        'MENEXENUS',
        'MENO',
        'NICIAS',
        'PHAEDO',
        'PHAEDRUS',
        'PHILEBUS',
        'POLUS',
        'PROTARCHUS',
        'SOCRATES',
        'SON',
        'STRANGER',
        'TERPSION',
        'THEAETETUS',
        'THEODORUS',
        'TIMAEUS',
        'YOUNG SOCRATES'
    ];

    foreach ($nodes as $node) {

        // Dialogue end: Guttenberg License Section reached
        if ($node->nodeName == 'section' && $dialogueStart) {
            $dialogueEnd = true;
            break;
        }

        // Dialogue starts: First Node (<p>, <h3>, ...) with PERSONS OF DIALOGUE
        if (str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE')) {            // OR Setting, OR ....
            $utterance = explode(":", trim($node->nodeValue));
            $persons = $utterance[1];
            $dialogueStart = true;
            continue;
        }

        // Set Scene
        if (str_contains($node->nodeValue, 'SCENE')) {
            $utterance = explode(":", trim($node->nodeValue));
            $setting = $utterance[1];
            $dialogueStart = true;
            continue;
        }

        // Set Place of Narration
        if (str_contains($node->nodeValue, 'PLACE OF THE NARRATION')) {
            $utterance = explode(":", trim($node->nodeValue));
            $placeOfNarration = $utterance[1];
            $dialogueStart = true;

            continue;
        }

        if ($dialogueStart && $node->nodeName == 'p' && trim($node->nodeValue) != '') {

            $utterance = explode(":", trim($node->nodeValue));

            // speech w/o semi colons
            if (empty($utterance))
                $speech = $node->nodeValue;
            // speech with semi colons with an initial Speech Character
            elseif (in_array($utterance[0], $speakers)) {
                $speaker = trim($utterance[0]);
                for ($i = 1; $i < sizeof($utterance); $i++)
                    $speech = $speech . $utterance[$i];
            }
            // speech with semi colons but w/o speech character
            else {
                for ($i = 0; $i < sizeof($utterance); $i++)
                    $speech = $speech . $utterance[$i];
            }

            $speechNum = str_pad($speechNo, 3, '0', STR_PAD_LEFT);
            $speakerH2 = ($speaker != "") ? "<h2 class=\"speaker\">$speaker</h2>" : '';
            $speechDiv = "\n<div class=\"speech\">\n<span class=\"ref\">" . $speechNum . "</span>\n"
                . $speakerH2 .
                "\n<div class=\"sentence\">$speech</div>\n</div>";

            // set and reset variables
            $speechNo++;
            $textInHtml .= $speechDiv;
            $speech = '';
            $speaker = '';
        }
    }

    // Output Header
    $title = $metaData['dc.title'];
    $author = $metaData['dc.creator'];
    $translator = $metaData['marcrel.trl'];
    $cssFileParts = pathinfo($cssFile);
    $head = "<head>
                <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">
                <title>" . $title . " | " . $author . "</title>
                <meta charset=\"utf-8\">
                <link href=\"" . $cssFileParts['basename'] . "\" rel=\"stylesheet\">
            </head>";

    // Dialogue Headings: Author, Title, Translator
    $headings = "
            <nav><a href=\"https://en.wikipedia.org/wiki/Plato\">" . $author . "</a></nav>
            <h1 lang=\"en\">" . $title . "</h1>
            <h3 lang=\"en\">Translation by " . $translator . "</h3>
            <!-- <h4 lang=\"en\">Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></h4> -->
            <p class=\"copyright\"><small>© Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></small></p>
            ";

    // Body of Dialogue
    $beautifiedFile =
        "<html>" . $head . "
                <body class=\"default\">
                    <div class=\"container\">" .
        $headings .
        $textInHtml .
        "</div>
                </body>
            </html>";

    // Output Beautified File
    file_put_contents($outputFile, $beautifiedFile);

    // Copy Css from source to output location
    if (!copy($cssFile, 'output/' . $cssFileParts['basename']))
        die("Error: failed to copy $cssFile...");
}


$sourceFiles = scandir('sources');
foreach ($sourceFiles as $filename) {
    $pathParts = pathinfo($filename);
    if ($pathParts['extension'] != 'html')
        continue;

    beautifyPlato("./sources/" . $pathParts['basename'], "./css/greek-learner-text.css", "output/" . $pathParts['filename'] . "-beautified.html");
}

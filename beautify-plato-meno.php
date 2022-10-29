<?php

/**
 * Beautifies Plato's, Meno (tr. Jowett) from Guttenberg Project
 *
 * The function takes the location of the html file stripped
 * of everything except the core text i.e. Jowett's introductions, license, etc.
 * The function creates a beautiful html file from the input file and a css file.
 *
 * @param  string   $file       location of dialogue text only html file
 * @param  string   $cssFile    location of the css file
 * @param  string   $outputFile location and name of outputfile
 * @return void
 * @todo Fix: Dialogue Start Marker Incomptible: Apology, Lesser Hypias, Lysis, Republic and Timease (nested divs or atypical Scene, Persons setting)
 *       Note: DomNode->nodeValue = textContent
 */

function beautifyMeno(string $file, string $cssFile, string $outputFile)
{

    $dom = new DomDocument();
    $htmlDoc = file_get_contents($file);

    $dom->loadHTML($htmlDoc);
    $xpath = new DOMXPath($dom);
    //$nodes = $xpath->query('/html/body//*[@style]');
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

    $title = 'Meno';
    $author = 'Plato';
    $translator = 'Jowett';

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

            //printf('Element %s: %s %s', $node->nodeName, $node->textContent, PHP_EOL);
            $utterance = explode(":", trim($node->nodeValue));

            if (empty($utterance))
                $speech = $node->nodeValue;
            elseif (in_array($utterance[0], $speakers)) {
                $speaker = trim($utterance[0]);
                $speech = $speech . $utterance[1];
                // itterate over rest of utterance from explode (may contain more than one semicolon)
                for ($i = 1; $i < sizeof($utterance); $i++)
                    $speech = $speech . $utterance[$i];
            } else    // p text not a dialogue entry with speaker but does contain semi-colon
                $speech = $node->nodeValue;

            $speechNum = str_pad($speechNo, 3, '0', STR_PAD_LEFT);
            $speakerH2 = ($speaker != "") ? "<h2 class=\"speaker\">$speaker</h2>" : '';
            echo "\n";
            $speechDiv = "\n<div class=\"speech\">\n<span class=\"ref\">" . $speechNum . "</span>\n"
                . $speakerH2 .
                "\n<div class=\"sentence\">$speech</div>\n</div>";
            echo $speechDiv;
            // sleep(1);
            $speechNo++;
            $textInHtml .= $speechDiv;
            $speech = '';
            $speaker = '';
            // speaker stays the same
        }
    }

    $head = "<head>
                <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">
                <title>" . $title . " | " . $author . "</title>
                <meta charset=\"utf-8\">
                <link href=\"" . $cssFile . "\" rel=\"stylesheet\">
            </head>";

    $headings = "
            <nav><a href=\"https://en.wikipedia.org/wiki/Plato\">" . $author . "</a></nav>
            <h1 lang=\"en\">" . $title . "</h1>
            <h3 lang=\"en\">Translation by " . $translator . "</h3>
            <!-- <h4 lang=\"en\">Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></h4> -->
            <p class=\"copyright\"><small>© Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></small></p>
            ";

    $beautifiedFile =
        "<html>" . $head . "
                <body class=\"default\">
                    <div class=\"container\">" .
        $headings .
        $textInHtml .
        "</div>
                </body>
            </html>";

    file_put_contents($outputFile, $beautifiedFile);
    if (!copy("css/" . $cssFile, 'output/' . $cssFile)) {
        echo "failed to copy $cssFile...\n";
    }
}

beautifyMeno("./sources/plato-meno-tr-jowett-guttenberg.html", "greek-learner-text.css", "output/plato-meno-beautified-new.html");

<?php

/**
 * beautifyPlato
 *
 * Beautifies Plato's Works, translated by Benjamin Jowett, from Guttenberg Project
 *
 * The function takes the location of the html file and a css file and creates a beautiful html file
 * Note: DomElement->nodeValue = <DomElement->
 *
 * @param  string   $cssFile    location of the css file
 * @param  string   $outputDir          location and name of output file
 * @param  string   $requestedDialogue  all or single dialogue title
 * @return void
 * @todo 1. fix: Dialogues that contain errors
 *              Republic:   introduction prepended; books not separated;
 *              Laws:       books not separated;
 *              Laches:     Dialogue description not recorded propertly
 *              Lysis:      Dialogue description not recorded propertly
 *              Phaedo:     person of dialogue missing
 *       2. fix: sentence tokenizer (spreg) does not identify sentences ending with "?!", or "..."
 *       3. fix: add footnotes
 *       4. add Jowett introductions
 *       5. Add Non-Jowett dialogues
 */
function beautifyPlato(string $cssFile, string $outputDir, string $requestedDialogue)
{
    // Basic guard for css file and output file
    if (!file_exists($cssFile))
        die("Css file " . $cssFile . " could not be found");

    $outputDirParts = pathinfo($outputDir);
    if (!is_dir($outputDirParts['dirname']))
        die("Output directory not found");

    // Variable initialization
    // Speakers from all Platonic dialogues
    $dialogues = [
        "alcibiadesI"   => "https://www.gutenberg.org/cache/epub/1676/pg1676-images.html",  // "https://www.gutenberg.org/files/1676/1676-h/1676-h.htm"
        "alcibiadesII"   => "https://www.gutenberg.org/cache/epub/1677/pg1677-images.html", // "https://www.gutenberg.org/files/1677/1677-h/1677-h.htm"
        "apology"   => "https://www.gutenberg.org/cache/epub/1580/pg1580-images.html",      // "https://www.gutenberg.org/files/1656/1656-h/1656-h.htm",
        "charmides" => "https://www.gutenberg.org/cache/epub/1580/pg1580-images.html",      // "https://www.gutenberg.org/files/1580/1580-h/1580-h.htm",
        "cratylus"  => "https://www.gutenberg.org/cache/epub/1616/pg1616-images.html",      // "https://www.gutenberg.org/files/1616/1616-h/1616-h.htm",
        "critias"   => "https://www.gutenberg.org/cache/epub/1571/pg1571-images.html",      // "https://www.gutenberg.org/files/1571/1571-h/1571-h.htm",
        "crito"     => "https://www.gutenberg.org/cache/epub/1657/pg1657-images.html",      // "https://www.gutenberg.org/files/1657/1657-h/1657-h.htm",
        "eryxias"   => "https://www.gutenberg.org/cache/epub/1681/pg1681-images.html",      // "https://www.gutenberg.org/files/1681/1681-h/1681-h.htm",
        "euthydemus" => "https://www.gutenberg.org/cache/epub/1598/pg1598-images.html",     // "https://www.gutenberg.org/files/1598/1598-h/1598-h.htm",
        "euthyphro" => "https://www.gutenberg.org/cache/epub/1642/pg1642-images.html",      // "https://www.gutenberg.org/files/1642/1642-h/1642-h.htm",
        "gorgias"   => "https://www.gutenberg.org/cache/epub/1672/pg1672-images.html",      // "https://www.gutenberg.org/files/1672/1672-h/1672-h.htm",
        "ion"       => "https://www.gutenberg.org/cache/epub/1635/pg1635-images.html",      // "https://www.gutenberg.org/files/1635/1635-h/1635-h.htm",
        "laches"    => "https://www.gutenberg.org/cache/epub/1584/pg1584-images.html",      // "https://www.gutenberg.org/files/1584/1584-h/1584-h.htm",
        "laws"      => "https://www.gutenberg.org/cache/epub/1750/pg1750-images.html",      // "https://www.gutenberg.org/files/1750/1750-h/1750-h.htm",
        "lesser-hypias" => "https://www.gutenberg.org/cache/epub/1673/pg1673-images.html",  // "https://www.gutenberg.org/files/1673/1673-h/1673-h.htm",
        "lysis"     => "https://www.gutenberg.org/cache/epub/1579/pg1579-images.html",      // "https://www.gutenberg.org/files/1579/1579-h/1579-h.htm",
        "menexenus" => "https://www.gutenberg.org/cache/epub/1682/pg1682-images.html",      // "https://www.gutenberg.org/files/1682/1682-h/1682-h.htm",
        "meno"      => "https://www.gutenberg.org/cache/epub/1643/pg1643-images.html",      // "https://www.gutenberg.org/files/1643/1643-h/1643-h.htm",
        "phaedo"    => "https://www.gutenberg.org/cache/epub/1658/pg1658-images.html",      // "https://www.gutenberg.org/files/1658/1658-h/1658-h.htm",
        "phaedrus"  => "https://www.gutenberg.org/cache/epub/1636/pg1636-images.html",      // "https://www.gutenberg.org/files/1636/1636-h/1636-h.htm",
        "philebus"  => "https://www.gutenberg.org/cache/epub/1744/pg1744-images.html",      // "https://www.gutenberg.org/files/1744/1744-h/1744-h.htm",
        "protagoras" => "https://www.gutenberg.org/cache/epub/1591/pg1591-images.html",     // "https://www.gutenberg.org/files/1591/1591-h/1591-h.htm",
        "parmenides" => "https://www.gutenberg.org/cache/epub/1687/pg1687-images.html",     // "https://www.gutenberg.org/files/1687/1687-h/1687-h.htm",
        "republic"  => "https://www.gutenberg.org/cache/epub/1497/pg1497-images.html",      // "https://www.gutenberg.org/files/1497/1497-h/1497-h.htm",
        "sophist"   => "https://www.gutenberg.org/cache/epub/1735/pg1735-images.html",      // "https://www.gutenberg.org/files/1735/1735-h/1735-h.htm",
        "statesman" => "https://www.gutenberg.org/cache/epub/1738/pg1738-images.html",      // "https://www.gutenberg.org/files/1738/1738-h/1738-h.htm",
        "symposium" => "https://www.gutenberg.org/cache/epub/1600/pg1600-images.html",      // "https://www.gutenberg.org/files/1600/1600-h/1600-h.htm",
        "theaetetus" => "https://www.gutenberg.org/cache/epub/1726/pg1726-images.html",     // "https://www.gutenberg.org/files/1726/1726-h/1726-h.htm",
        "timaeus"   => "https://www.gutenberg.org/cache/epub/1572/pg1572-images.html"       // "https://www.gutenberg.org/files/1572/1572-h/1572-h.htm",
    ];

    $speakers = [
        'ALCIBIADES',
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

    // Dialogue descriptions from Jowett translations (0 or more in each book)
    $dialogueDescriptors = [
        'PERSONS OF THE DIALOGUE',
        'SCENE',
        'PLACE OF THE NARRATION'
    ];


    // Determine which dialogues are requested [all or one only]
    $requestedDialogues = [];
    if ($requestedDialogue == 'all')
        $requestedDialogues = $dialogues;   // all dialogues
    elseif (!array_key_exists(strtolower($requestedDialogue), $dialogues))
        die("Dialogue not found");
    else
        $requestedDialogues = [strtolower($requestedDialogue) => $dialogues[strtolower($requestedDialogue)]];

    foreach ($requestedDialogues as $title => $dialogueUrl) {
        echo "Processing " . $title . "\n";

        // initialize variable for dialogue processsing
        $dialogueDescription = [];
        $toc = [];
        $dialogueStarted = false;
        $speaker = '';
        $paragraphNum = 1;;
        $paragraphText = '';
        $textParagraphsHtml = '';

        // Get HTML file from Guttenberg
        $htmlDoc = file_get_contents($dialogueUrl);
        if ($htmlDoc == false || trim($htmlDoc) == '')
            die('Error: could not retrieve the dialogue from the url');
        $dom = new DomDocument();
        libxml_use_internal_errors(true);
        $dom->loadHTML($htmlDoc);
        libxml_clear_errors();      // clears PHP Warnings

        // Process meta tags
        $xpath = new DOMXPath($dom);
        $metaTags = getMetaTags($title, $xpath->query('/html/head/meta'));

        // Process body
        $nodes = $xpath->query('/html/body//*');
        foreach ($nodes as $node) {
            // Check if Dialogue Ended
            if (guttenbergPreamble($node))
                continue;

            if (guttenbergPostscript($node))
                break;

            if ($node->nodeName == 'a' && $node->getAttribute('class') == 'pginternal') {
                array_push($toc, [ 'content' => $node->nodeValue, 'href' => $node->getAttribute('href')]);
                echo "TOC: ".$node->nodeValue.":".$node->getAttribute('href')."\n";
            }

            // Check if Dialogue Started
            if (!$dialogueStarted) {
                $dialogueStarted = dialogueStarted($node, $metaTags, $dialogueDescriptors);
                if (!$dialogueStarted)
                    continue;
            }

            // process dialogue text
            $nodeValue = trim($node->nodeValue);

            // skip if node has no text
            if ($nodeValue == '')
                continue;

            // record dialogue description, if there is one
            $utterance = explode(":", $nodeValue);
            if (in_array($utterance[0], $dialogueDescriptors)) {
                $dialogueDescription[$utterance[0]] = $utterance[1];
                continue;
            }

            // dialogue paragraphs
            // convert text (by speaker or not) to a formatted div
            if ($node->nodeName == 'p') {
                // speech with dialogue speech character before initial colon (e.g. SOCRATES: blah : blah)
                if (in_array($utterance[0], $speakers)) {
                    $speaker = $utterance[0];
                    for ($i = 1; $i < sizeof($utterance); $i++)
                        $paragraphText = $paragraphText . $utterance[$i];
                } else
                    for ($i = 0; $i < sizeof($utterance); $i++)
                        $paragraphText = $paragraphText . $utterance[$i];

                // TODO: preg_split for sentences that end in i) ?!, ii) ...
                $parSentences = preg_split('/(?<=[.?!;:])\s+/', trim(preg_replace('/\s+/', ' ', $paragraphText)), -1, PREG_SPLIT_NO_EMPTY);
                $textParagraphsHtml .= paragraphHtml($paragraphNum, $speaker, $parSentences);

                // set and reset variables
                $paragraphNum++;
                $paragraphText = '';
                $speaker = '';
            }
        }

        // atypical dialogue end
        if ($metaTags['dc.title'] == 'Critias')
            $textParagraphsHtml .= "<pre>* The rest of the Dialogue of Critias has been lost.</pre>";

        $beautifiedHtmlFile = dialogueHtml($metaTags, $cssFile,  $dialogueUrl, $dialogueDescription, $toc, $textParagraphsHtml);

        // Output Beautified File
        file_put_contents("output/" . $title . ".html", $beautifiedHtmlFile);
    }

    // Copy Css to output location
    $cssFileParts = pathinfo($cssFile);
    if (!copy($cssFile, 'output/' . $cssFileParts['basename']))
        die("Error: failed to copy $cssFile...");
    sleep(3);
}

function getMetaTags(string $dialogue, $headerNodes): array
{
    $metaTags = [];
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
    $subjects = [];

    foreach ($headerNodes as $meta) {
        $name = $meta->getAttribute('name');
        $content = $meta->getAttribute('content');
        if (in_array($name, $metaTagNames))
            if ($name == 'dc.subject')
                array_push($subjects, $content);
            else
                $metaTags[$name] = $content;
    }
    if (!empty($subjects))
        $metaTags['dc.subject'] = $subjects;

    if ($dialogue == 'alcibiadesI' || $dialogue == 'alcibiadesII')
        $metaTags['marcrel.trl'] = "Jowett, Benjamin, 1817-1893";

    return $metaTags;
}

function dialogueStarted($node, $metaTags, $dialogueDescriptors): bool
{
    // Atypical dialogue structure
    if ($metaTags['dc.title'] == 'Apology')
        return $node->nodeName == 'a' && $node->getAttribute('id') == 'chap02' ? true : false;
    if ($metaTags['dc.title'] == 'Menexenus')
        return $node->nodeName == 'h2' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaTags['dc.title'] == 'Laches')
        return $node->nodeName == 'h3' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaTags['dc.title'] == 'Lysis')
        return $node->nodeName == 'h2' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaTags['dc.title'] == 'Cratylus')
        return $node->nodeName == 'p' && $node->getAttribute('class') == 'center' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaTags['dc.title'] == 'Crito')
        return $node->nodeName == 'p' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;

    // typical dialogue structure: dialogue descriptor indicates start of dialogue (usually PERSONS OF DIALOGUE)
    else {
        foreach ($dialogueDescriptors as $description)
            if (str_contains($node->nodeValue, $description))
                return true;
    }
    return false;
}

function guttenbergPostscript($node): bool
{
    return $node->nodeName == 'section' && ($node->getAttribute('id') == 'pg-footer');
}

function guttenbergPreamble($node): bool
{
    return $node->nodeName == 'section' && ($node->getAttribute('id') == 'pg-header');
}

function paragraphHtml(int $paragraphNum, string $speaker, array $parSentences): string
{
    $parNumFormatted = str_pad($paragraphNum, 3, '0', STR_PAD_LEFT);
    $speakerH2 = ($speaker != "") ? "<h2 class=\"speaker\">" . $speaker . "</h2>" : '';
    $parHtml = '';

    foreach ($parSentences as $sentence)
        $parHtml .= "<div class=\"sentence\">" . $sentence . "&nbsp;</div>";

    $parDiv = "<div class=\"speech\">
                <span class=\"ref\">" . $parNumFormatted . "</span>" .
                $speakerH2 .
                $parHtml .
            "</div>";

    return $parDiv;
}

function dialogueHtml($metaTags, $cssFile, $dialogueUrl, $dialogueDescription, array $toc, $dialogueHTML)
{
    $title = $metaTags['dc.title'];
    $author = explode(",", $metaTags['dc.creator'])[0];
    $translator = $metaTags['marcrel.trl'];
    $cssFileParts = pathinfo($cssFile);

    $metaTagsHtml = '';

    foreach ($metaTags as $name => $content) {
        if (is_array($content)) {
            foreach ($content as $unitcontent)
                $metaTagsHtml .= "<meta name=\"".$name."\" content=\"".$unitcontent."\">\n";
        }
        else
            $metaTagsHtml .= "<meta name=\"".$name."\" content=\"".$content."\">\n";
    }

    $header = "<head>
                    <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">
                    <title>" . $title . " | " . $author . "</title>
                    <meta charset=\"utf-8\">
                    <meta name=\"sourceUrl\" content=\"".$dialogueUrl."\"".
                    $metaTagsHtml.
                    "<link href=\"" . $cssFileParts['basename'] . "\" rel=\"stylesheet\">
                </head>";

    $tocHtml = '';
    print_r($toc);
    foreach ($toc as $tocEntry)
        $tocHtml.= "<a href=\"".$tocEntry['href']."\">".$tocEntry['content']."</a><br>";

    $preamble = '';
    foreach ($dialogueDescription as $key => $desc) {
        if ($desc != '')
            $preamble .= "<p class=\"dialogueDescription\"><strong>" . $key . "</strong>:" . $desc;
    }

    // Dialogue Headings: Author, Title, Translator
    $headings = "
            <h1 class=\"dialogueTitle\" lang=\"en\">" . $title . "</h1>
            <h2 class=\"dialogueAuthor\" lang=\"en\"><a href=\"https://en.wikipedia.org/wiki/Plato\">" . $author . "</a></h2>
            <h3 class=\"dialogueTranslator\" lang=\"en\">Translation by " . $translator . "</h3>
            <p class=\"dialogueCopyright\"><small><a href=\"".$dialogueUrl."\">Guttenberg source file</a>&nbsp;and&nbsp;<a href=\"https://www.gutenberg.org/license\">©License</a></small></p>".
            $tocHtml.
            $preamble;

    $dialogueTocEntry = count($toc) - 1;
    $dialogueStart = "<a href=\"".$toc[$dialogueTocEntry]['href']."\">".$toc['content']."</a>";
    // Body of Dialogue
    $beautifiedHtml =
        "<html>".
            $header.
            "<body class=\"default\">
                <div class=\"container\">".
                    $headings.
                    $dialogueStart.
                    $dialogueHTML.
                "</div>
            </body>
        </html>";

    return $beautifiedHtml;
}


if (isset($argv[1]) && isset($argv[2]) && isset($argv[3]))
    beautifyPlato($argv[1], $argv[2], $argv[3]);
else
    die("Usage Error:\nsingle dialogue: php beautifulPlato.php css_file_location output_dir meno\nall dialogues: php beautifulPlato.php css_file_location output_dir all\n\n");

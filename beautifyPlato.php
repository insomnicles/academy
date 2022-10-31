<?php

function getMetaTags($headerNodes): array
{
    $metaData = [];
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
                $metaData[$name] = $content;
    }
    if (!empty($subjects))
        $metaData['dc.subject'] = $subjects;

    return $metaData;
}

function jowettTranslationPlato($metaTags): bool
{
    if (!isset($metaTags['dcterms.source']))
        return false;

    $source = $metaTags['dcterms.source'];
    $guttenbergJowettTranslations = [
        "apology"   => "https://www.gutenberg.org/files/1656/1656-h/1656-h.htm",
        "charmides" => "https://www.gutenberg.org/files/1580/1580-h/1580-h.htm",
        "cratylus"  => "https://www.gutenberg.org/files/1616/1616-h/1616-h.htm",
        "critias"   => "https://www.gutenberg.org/files/1571/1571-h/1571-h.htm",
        "crito"     => "https://www.gutenberg.org/files/1657/1657-h/1657-h.htm",
        "eryxias"   => "https://www.gutenberg.org/files/1681/1681-h/1681-h.htm",
        "euthydemus" => "https://www.gutenberg.org/files/1598/1598-h/1598-h.htm",
        "euthyphro" => "https://www.gutenberg.org/files/1642/1642-h/1642-h.htm",
        "gorgias"   => "https://www.gutenberg.org/files/1672/1672-h/1672-h.htm",
        "ion"       => "https://www.gutenberg.org/files/1635/1635-h/1635-h.htm",
        "laches"    => "https://www.gutenberg.org/files/1584/1584-h/1584-h.htm",
        "laws"      => "https://www.gutenberg.org/files/1750/1750-h/1750-h.htm",
        "lesser-hypias" => "https://www.gutenberg.org/files/1673/1673-h/1673-h.htm",
        "lysis"     => "https://www.gutenberg.org/files/1579/1579-h/1579-h.htm",
        "menexenus" => "https://www.gutenberg.org/files/1682/1682-h/1682-h.htm",
        "meno"      => "https://www.gutenberg.org/files/1643/1643-h/1643-h.htm",
        "phaedo"    => "https://www.gutenberg.org/files/1658/1658-h/1658-h.htm",
        "phaedrus"  => "https://www.gutenberg.org/files/1636/1636-h/1636-h.htm",
        "philebus"  => "https://www.gutenberg.org/files/1744/1744-h/1744-h.htm",
        "protagoras" => "https://www.gutenberg.org/files/1591/1591-h/1591-h.htm",
        "republic"  => "https://www.gutenberg.org/files/1497/1497-h/1497-h.htm",
        "sophist"   => "https://www.gutenberg.org/files/1735/1735-h/1735-h.htm",
        "statesman" => "https://www.gutenberg.org/files/1738/1738-h/1738-h.htm",
        "symposium" => "https://www.gutenberg.org/files/1600/1600-h/1600-h.htm",
        "theaetetus" => "https://www.gutenberg.org/files/1726/1726-h/1726-h.htm",
        "timaeus"   => "https://www.gutenberg.org/files/1572/1572-h/1572-h.htm"
    ];
    foreach ($guttenbergJowettTranslations as $key => $sourceUrl)
        if ($source == $sourceUrl) {
            echo "Processing " . $key . "\n";
            return true;
        }
    return false;
}

function dialogueStarted($node, $metaData, $dialogueDescriptors): bool
{
    // Atypical dialogue structure
    if ($metaData['dc.title'] == 'Apology')
        return $node->nodeName == 'a' && $node->getAttribute('id') == 'chap02' ? true : false;
    if ($metaData['dc.title'] == 'Menexenus')
        return $node->nodeName == 'h2' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaData['dc.title'] == 'Laches')
        return $node->nodeName == 'h3' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaData['dc.title'] == 'Lysis')
        return $node->nodeName == 'h2' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaData['dc.title'] == 'Cratylus')
        return $node->nodeName == 'p' && $node->getAttribute('class') == 'center' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;
    if ($metaData['dc.title'] == 'Crito')
        return $node->nodeName == 'p' && str_contains($node->nodeValue, 'PERSONS OF THE DIALOGUE') ? true : false;

    // typical dialogue structure: dialogue descriptor indicates start of dialogue (usually PERSONS OF DIALOGUE)
    else {
        foreach ($dialogueDescriptors as $description)
            if (str_contains($node->nodeValue, $description))
                return true;
    }
    return false;
}

function dialogueEnded($node): bool
{
    return $node->nodeName == 'section' && ($node->getAttribute('id') == 'pg-footer');
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

function dialogueHtml($metaData, $cssFile, $dialogueDescription, $dialogueHTML)
{
    $title = $metaData['dc.title'];
    $author = explode(",", $metaData['dc.creator'])[0];
    $translator = $metaData['marcrel.trl'];
    $cssFileParts = pathinfo($cssFile);

    $header = "<head>
                <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">
                <title>" . $title . " | " . $author . "</title>
                <meta charset=\"utf-8\">
                <link href=\"" . $cssFileParts['basename'] . "\" rel=\"stylesheet\">
            </head>";

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
            <p class=\"dialogueCopyright\"><small>© Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></small></p>"
        . $preamble;

    // Body of Dialogue
    $beautifiedFile =
        "<html>" .
        $header .
        "<body class=\"default\">
                <div class=\"container\">" .
        $headings .
        $dialogueHTML .
        "</div>
            </body>
        </html>";
    return $beautifiedFile;
}

/**
 * beautifyPlato
 *
 * Beautifies Plato's Works, translated by Benjamin Jowett, from Guttenberg Project
 *
 * The function takes the location of the html file and a css file and creates a beautiful html file
 * Note: DomElement->nodeValue = <DomElement->
 *
 * @param  string   $file       location of dialogue html file: must be a Guttenberg Plato book, Jowett translation only
 * @param  string   $cssFile    location of the css file
 * @param  string   $outputFile location and name of output file
 * @return void
 * @todo 1. Fix: Dialogues that contain errors
 *              Republic:   introduction prepended; books not separated;
 *              Laws:       books not separated;
 *              Laches:     Dialogue description not recorded propertly
 *              Lysis:      Dialogue description not recorded propertly
 *              Phaedo:     person of dialogue missing
 *       2. fix: sentence tokenizer (spreg) does not identify sentences ending with "?!", or "..."
 *       3.	add commandline args for intput, output directories
 *       4. add option to get text from guttenberg site instead of file
 *       5. more guards: i) check file extension of args
 *       6. add link to Guttenberg source file
 */

function beautifyPlato(string $file, string $cssFile, string $outputFile)
{
    // Basic Guards
    if (!file_exists($file))
        die("Html file " . $file . " could not be found");
    if (!file_exists($cssFile))
        die("Css file " . $cssFile . " could not be found");
    $outputFileParts = pathinfo($outputFile);
    if (!is_dir($outputFileParts['dirname']))
        die("Output directory not found");

    // Variable initialization
    // speakers from all Platonic dialogues
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

    // Dialogue descriptions from Jowett translations (0 or more in each book)
    $dialogueDescriptors = [
        'PERSONS OF THE DIALOGUE',
        'SCENE',
        'PLACE OF THE NARRATION'
    ];
    $dialogueDescription = [];

    // paragraph processing variables
    $dialogueStarted = false;
    $speaker = '';
    $paragraphNum = 1;;
    $paragraphText = '';
    $textParagraphsHtml = '';

    // Processing File
    $htmlDoc = file_get_contents($file);

    $dom = new DomDocument();
    libxml_use_internal_errors(true);
    $dom->loadHTML($htmlDoc);
    libxml_clear_errors();      // clears PHP Warnings

    $xpath = new DOMXPath($dom);

    $headerNodes = $xpath->query('/html/head/*');
    $metaData = getMetaTags($headerNodes);

    if (!jowettTranslationPlato($metaData))
        die("Source file is not a Jowett translation of Plato from Project Guttenberg");

    $nodes = $xpath->query('/html/body//*');
    foreach ($nodes as $node) {
        // Check if Dialogue Ended
        if (dialogueEnded($node))
            break;

        // Check if Dialogue Started
        if (!$dialogueStarted) {
            $dialogueStarted = dialogueStarted($node, $metaData, $dialogueDescriptors);
            if (!$dialogueStarted)
                continue;
        }

        // Dialogue Started
        $nodeValue = trim($node->nodeValue);

        // skip if node has no text
        if ($nodeValue == '')
            continue;

        // record dialogue description, if there is one
        $utterance = explode(":", $nodeValue);
        if (in_array($utterance[0], $dialogueDescriptors)) {
            // if (!isset($utterance[1]) )
            //     echo $node->nodeValue;
            $dialogueDescription[$utterance[0]] = $utterance[1];
            continue;
        }

        // Dialogue Paragraphs started
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

            // TODO: doesnt work for sentences that end in i) ?!, ii) ...
            $parSentences = preg_split('/(?<=[.?!;:])\s+/', trim(preg_replace('/\s+/', ' ', $paragraphText)), -1, PREG_SPLIT_NO_EMPTY);
            $textParagraphsHtml .= paragraphHtml($paragraphNum, $speaker, $parSentences);

            // set and reset variables
            $paragraphNum++;
            $paragraphText = '';
            $speaker = '';
        }
    }

    if ($metaData['dc.title'] == 'Critias')
        $textParagraphsHtml .= "<pre>* The rest of the Dialogue of Critias has been lost.</pre>";

    $beautifiedHtmlFile = dialogueHtml($metaData, $cssFile, $dialogueDescription, $textParagraphsHtml);

    // Output Beautified File
    file_put_contents($outputFile, $beautifiedHtmlFile);

    // Copy Css from source to output location
    $cssFileParts = pathinfo($cssFile);
    if (!copy($cssFile, 'output/' . $cssFileParts['basename']))
        die("Error: failed to copy $cssFile...");
}


// beautifyPlato("./sources/plato-euthyphro-tr-jowett-guttenberg.html", "./css/plato-jowett-default.css", "output/plato-euthyphro-tr-jowett-guttenberg-beautified.html");
// beautifyPlato("./sources/plato-apology-tr-jowett-guttenberg.html", "./css/plato-jowett-default.css", "output/plato-apology-tr-jowett-guttenberg-beautified.html");

$sourceFiles = scandir('sources');
foreach ($sourceFiles as $filename) {
    $pathParts = pathinfo($filename);
    if ($pathParts['extension'] != 'html')
        continue;

    beautifyPlato("./sources/" . $pathParts['basename'], "./css/plato-jowett-default.css", "output/" . $pathParts['filename'] . "-beautified.html");
}

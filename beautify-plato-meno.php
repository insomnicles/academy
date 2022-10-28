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
 */

function beautifyMeno(string $file, string $cssFile, string $outputFile) {

    $dom = new DomDocument();
    $htmlDoc = file_get_contents($file);
    $dom->loadHTML($htmlDoc);
    $child_elements = $dom->getElementsByTagName('p');

    // variable initialization
    $title = "MENO";
    $author = "Plato";
    $translator = "Benjamin Jowett";
    $translationYear = 0;
    $publicationYear = 0;
    $license = 'guttenberg';

    $characters = [ 'PERSONS OF THE DIALOGUE', 'SOCRATES', 'MENO', 'BOY', 'ANYTUS'];
    $speechNo = 1;
    $textInHtml = '';
    $speaker = '';
    $speech = '';

    foreach ($child_elements as $par) {
        $utterance = explode (":", trim($par->nodeValue));

        if (!array_key_exists(0, $utterance))
            $speech = $par->nodeValue;

        if ($utterance[0] == 'PERSONS OF THE DIALOGUE')
            continue;

        if (in_array($utterance[0], $characters)) {
            $speaker = trim($utterance[0]);
            for ($i=1; $i < sizeof($utterance); $i++)
                $speech = $speech.$utterance[$i];
        }

        $speechNum = str_pad($speechNo, 3, '0', STR_PAD_LEFT);
        $speechDiv = <<<EOT
            <div class="speech">
                <span class="ref">$speechNum</span>
                <h2 class="speaker">$speaker</h2>
                <div class="sentence">$speech</div>
            </div>
        EOT;

        $speechNo++;
        $textInHtml.=$speechDiv;
        $speech = '';
    }

    $head = "<head>
                <meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\">
                <title>".$title." | ".$author."</title>
                <meta charset=\"utf-8\">
                <link href=\"".$cssFile."\" rel=\"stylesheet\">
            </head>";

    $headings = "
            <nav><a href=\"https://en.wikipedia.org/wiki/Plato\">".$author."</a></nav>
            <h1 lang=\"en\">".$title."</h1>
            <h3 lang=\"en\">Translation by ".$translator."</h3>
            <!-- <h4 lang=\"en\">Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></h4> -->
            <p class=\"copyright\"><small>© Public Domain: <a href=\"https://www.gutenberg.org/license\">Project Guttenberg License</a></small></p>
            ";

    $beautifiedFile =
            "<html>".$head."
                <body class=\"default\">
                    <div class=\"container\">".
                        $headings.
                        $textInHtml.
                    "</div>
                </body>
            </html>";

    file_put_contents($outputFile, $beautifiedFile);
    if (!copy("css/".$cssFile, 'output/'.$cssFile)) {
        echo "failed to copy $cssFile...\n";
    }
}

beautifyMeno("./meno/plato-meno-text.html", "greek-learner-text.css", "output/plato-meno-beautified.html");

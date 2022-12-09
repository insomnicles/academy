var section_active = 0

function firstSection() {
    showSection(0)
}

function previousSection() {
    var sections = document.getElementsByClassName('book_section');
    let num_of_sections = sections.length;
    var section_active = 0;

    if (num_of_sections == 0)
        return

    for (let i = 0; i < sections.length; i++)
        if (sections[i].style.display == "block") {
            section_active = i;
            break;
        }

    if (section_active == 0)
        return

    section_active--;
    showSection(section_active)
}

function nextSection() {
    var sections = document.getElementsByClassName('book_section');
    let num_of_sections = sections.length;
    var section_active = 0;

    if (num_of_sections == 0)
        return

    for (let i = 0; i < sections.length; i++)
        if (sections[i].style.display == "block") {
            section_active = i;
            break;
        }

    if (section_active == (num_of_sections - 1))
        return

    section_active++;
    showSection(section_active)
}


function lastSection() {
    let last_section = document.getElementsByClassName('book_section').length - 1
    showSection(last_section)
}

function showSection(section_div) {
    var section_divs = document.getElementsByClassName('book_section');

    for (let i = 0; i < section_divs.length; i++)
        section_divs[i].style.display = "none";

    section_divs[section_div].style.display = "block";
    section_active = section_divs[section_div].id
    console.log(section_active)

    return true;
}

function showToc() {
    var section_divs = document.getElementsByClassName('book_section')

    for (let i = 0; i < section_divs.length; i++)
        section_divs[i].style.display = "none";

    return true;
}

function showExplanations() {
    var expl_containers = document.getElementsByClassName('explanation_container')

    show = (expl_containers[0].style.display == "none") ? "block" : "none";
    for (let i = 0; i < expl_containers.length; i++)
        expl_containers[i].style.display = show;
}

function hideRefs() {
    var ref_divs = document.getElementsByClassName('ref')

    if (ref_divs[0].style.display == "none")
        val = "block"
    else
        val = "none"

    for (let i = 0; i < ref_divs.length; i++)
        ref_divs[i].style.display = val;

    return true;
}

function darklightMode(mode) {
    var dark_link = document.getElementById('link_dark_mode');
    var light_link = document.getElementById('link_light_mode');

    console.log(mode);
    if (mode == 'dark') {
        light_link.style.display = "block";
        dark_link.style.display = "none";
        //change color pref
    }
    else if (mode == 'light') {
        light_link.style.display = "none";
        dark_link.style.display = "block";
        //change color pref
    }
    else {
        console.log("Color mode not recognized");
        light_link.style.display = "block";
        dark_link.style.display = "none";
    }
}

function formatSize() {
    const element = document.querySelector('.book_section')
    const style = getComputedStyle(element)
    fontSize = style.fontSize;

    if (fontSize == "20px")
        newFontSize = "10px";
    else if (fontSize == "18px")
        newFontSize = "20px";
    else if (fontSize == "16px")
        newFontSize = "18px";
    else if (fontSize == "14px")
        newFontSize = "16px";
    else if (fontSize == "12px")
        newFontSize = "14px";
    else if (fontSize == "10px")
        newFontSize = "12px";
    else
        newFontSize = "16px";

    var books_sections = document.getElementsByClassName('book_section');
    for (let i = 0; i < books_sections.length; i++) {
        books_sections[i].style.fontSize = newFontSize;
        // books_sections[i].style.backgroundColor = 'lime';
    }
    var speeches = document.getElementsByClassName('speech');
    for (let i = 0; i < speeches.length; i++) {
        speeches[i].style.fontSize = newFontSize;
        // speeches[i].style.backgroundColor = 'red';
    }
    var speakers = document.getElementsByClassName('speaker');
    for (let i = 0; i < speakers.length; i++) {
        speakers[i].style.fontSize = newFontSize;
    }
}
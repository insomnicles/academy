function showDiv(div) {

    var section_divs = document.getElementsByClassName('book_section')

    for (let i = 0; i < section_divs.length; i++)
        section_divs[i].style.display = "none";
    div.style.display = "block";

    return true;
}

function showToc() {
    var section_divs = document.getElementsByClassName('book_section')

    for (let i = 0; i < section_divs.length; i++)
        section_divs[i].style.display = "none";

    return true;
}

function darklightMode(mode) {
    var dark_link = document.getElementById('link_dark_mode');
    var light_link = document.getElementById('link_light_mode');

    if (mode == 'dark') {
        light_link.style.display = "block";
        dark_link.style.display = "none";
    }
    else if (mode == 'light') {
        light_link.style.display = "none";
        dark_link.style.display = "block";

    }
    else {
        console.log("ELSE");
        light_link.style.display = "block";
        dark_link.style.display = "none";
    }
}

function formatSize() {
    //var book_section = document.getElementsByClassName('book_section');
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
        // books_sections[i].style.backgroundColor = 'red';
    }
}
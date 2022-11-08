function showDiv(div) {

    var section_divs = document.getElementsByClassName('book_section')

    for (let i = 0; i < section_divs.length; i++)
        section_divs[i].style.display = "none";
    div.style.display = "block";

    return true;
}
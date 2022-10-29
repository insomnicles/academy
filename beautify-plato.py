try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

input_filename = "./meno/plato-meno-text.html"
css_filename = "./css/greek-learner-text.css"
output_filename = "./output/plato-meno-py-formatted.html"
characters =  [ 'PERSONS OF THE DIALOGUE' = 'PERSONS OF THE DIALOGUE', 'SOCRATES' = 'SOCRATES', 'MENO' = 'MENO', 'BOY' = 'BOY', 'ANYTUS' = 'ANYTUS' ];
print(characters);
exit 1;
f = open(input_filename, "r")
parsed_html = BeautifulSoup(f,'html5lib')

#print(parsed_html.body.find('p').text)
#print(parsed_html.body.find_all('p').text)
for tag in parsed_html.find_all('p'):
    utterance = tag.split(':')
    
    if utterance.len
    print(tag.text)
#print(parsed_html.body.find('div', attrs={'class':'container'}).text)
#print(f.read())
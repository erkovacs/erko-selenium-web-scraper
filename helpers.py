from bs4 import BeautifulSoup
from bs4.element import Comment

def is_tag_visible (element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def rip_text (body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(is_tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)
import logging

class Beautifier:
    created_doc = ""
    src, metadata, toc, body = {}, {}, {}, {}

    def __init__(self):
        logging.basicConfig(filename='html2prettyhtml.log', filemode="a", level=logging.DEBUG)
        logging.info('Created Prettifier')
        pass

    def create(self, structured_doc):
        self.src = structured_doc['src']
        self.metadata = structured_doc['metadata']
        self.toc = structured_doc['toc']
        self.body = structured_doc['body']
        self.create_doc()

    def get(self):
        return self.created_doc

    def reset(self):
        self.created_doc = ""
        self.src, self.metadata, self.toc, self.body = {}, {}, {}, {}


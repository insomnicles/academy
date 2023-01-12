from extractors.gutenberg.gutenberg import GutenbergExtractor
from extractors.gutenberg.gutenberg_epub import GutenbergEpubExtractor

class ExtractorFactory():
    def create(self, source, src_type, src_file, output_dir, save_src, save_json): 
        if source == 'gutenberg' and src_type == "html":
            return GutenbergExtractor(src_file, output_dir, save_src, save_json)
        if source == 'gutenberg' and src_type == "epub":
            return GutenbergEpubExtractor(src_file, output_dir, save_src, save_json)
        else:
            raise Exception("Extractor for source " + source + " not found.")
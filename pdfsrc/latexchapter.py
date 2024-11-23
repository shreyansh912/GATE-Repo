
from .settings import *
from .styles import *
from .latexfile import *

from typing import List

class LatexChapter:
    def __init__(self, config : Settings, basefile : str, style : Styles, chapterFilename : str) -> None:
        self.files : List[LatexFile] = []
        self.config : Settings = config
        self.chapter = ''
        self.style = style
        self.compiledfile = chapterFilename

        self.base = ''

        if basefile != None:
            with open(basefile) as f:
                self.base = f.read()

    # append a file
    def add_file(self, file : LatexFile):
        self.files.append(file)

    # combine all code and make chapter file
    def compile(self):
        chapter_code = self.base

        if self.config.useSections:
            section_codes = {}
            for file in self.files:
                if file.section not in section_codes:
                    section_codes[file.section] = ''
                section_codes[file.section] += file.getFileRepr()
            for section_alias, section_code in section_codes.items():
                chapter_code += self.style.applySectionStyle(section_alias, section_code)
        else:
            for file in self.files:
                chapter_code += file.getFileRepr()
        
        with open(self.compiledfile, 'w') as f:
            f.write(self.style.applyChapterStyle(chapter_code))

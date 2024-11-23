
import re

from .settings import *
from .styles import *

# forces lowercase, and removes extra whitespace
def get_insensitive_str(string : str):
    string = string.strip()
    string = string.lower()
    latex_comment = string.find('%')
    if latex_comment != -1:
        string = string[:latex_comment]
    return ' '.join(item for item in string.split(' ') if item)

class LatexFile:
    # get text from inside brakets of specific macro
    # Eg. \input{some file} gets 'some file' if macro = '\\input'
    def getCommandInfo(self, text : str, macro : str):
        macro = macro.replace('\\', '\\\\')
        pattern = f'{macro}{{(.+\\s*)}}'

        lcmd = re.findall(pattern, text)

        if len(lcmd) == 0:
            raise Exception(f'Fatal Error: {self.filename} does not contain desciptor command {macro}.')
        elif len(lcmd) > 1:
            self.config.log(f'Warning: macro {macro} used mutiple times in file {self.filename}')

        return re.findall(pattern, text)[0]

    def isFileSolved(self, text : str) -> bool:
        offset = text.find(self.config['latex.hints.solution'])
        for condition in self.config['pdf.conditions.solved']:
            if text.find(condition, offset) == -1:
                return False
        return True

    def isValidLatexFile(self, text : str) -> bool:
        for condition in self.config['pdf.conditions.validlatex']:
            condition = condition.replace('\\', '\\\\') + '[\\s\\{]'
            
            occurances = re.findall(condition, text)
            if not occurances:
                return False
        return True

    # get author, chapter etc. info from latex file
    def getLatexFileData(self):
        latex_code = ''
        author = ''
        chapter = ''
        question_code = ''
        with open(self.filename, 'r') as f:
            latex_code = f.read()

        if not self.isValidLatexFile(latex_code):
            return (None, None, None, None, False)

        author = self.getCommandInfo(latex_code, self.config['latex.hints.author'])
        if self.config['latex.toggles.useFolderNames']:
            chapter = self.fileroot[self.fileroot.find(self.config['latex.root']) + len(self.config['latex.root']):].split('/')[1]
        else:
            chapter = self.getCommandInfo(latex_code, self.config['latex.hints.chapter'])
            chapter = get_insensitive_str(chapter)

        author = get_insensitive_str(author)

        question_code = ''
        if self.config.assumeFileFormat == 'question-solution':
            question_macro = self.config['latex.hints.question']
            solution_macro = self.config['latex.hints.solution']

            question_loc = latex_code.find(question_macro)

            begin = question_loc + len(question_macro) + 1
            end = latex_code.find(solution_macro)

            if question_loc == -1:
                raise Exception(f'Fatal Error: {self.filename} does not contain desciptor macro {question_macro}.')
            if end == -1:
                raise Exception(f'Fatal Error: {self.filename} does not contain desciptor macro {solution_macro}.')
            
            if self.isFileSolved(latex_code):
                self.config.getAuthor(author).addSolution(self.filename)
            else:
                self.config.getAuthor(author).addQuestion(self.filename)

            question_code = latex_code[begin : end]

        section_name = ''
        # check for \section in preamble if useSections is True
        if self.config.useSections:
            iffalse = latex_code.find('\\iffalse')
            fi = latex_code.find('\\fi')
            section = re.findall(r'(\\\s*section\s*\*?\s*\{\s*(.+)\s*\})', latex_code)
            if len(section) == 0:
                raise Exception(f'Fatal Error: {self.filename} has no \\section macro')
            elif len(section) > 1:
                raise Exception(f'Fatal Error: {self.filename} has more than one \\section')
            else:
                section_name = section[0][1]
                section_pos = latex_code.find(section[0][0])
                if not (iffalse < section_pos and section_pos < fi):
                    raise Exception(f'Fatal Error: {self.filename} does not have a \\section in preamble(i.e before \\fi)')
                if section_name not in self.config['pdf.sections']:
                    possible_values = self.config['pdf.sections'].keys()
                    raise Exception(f'Fatal Error: {self.filename} possible values for \\section are: {possible_values}')

        return (author, chapter, question_code, section_name, True)

    def __init__(self, file : str, fileroot : str, style : Styles, config : Settings) -> None:
        self.filename = file
        self.fileroot = fileroot
        self.config = config
        self.author, self.chapter, self.question_code, self.section, self.isMainFile = self.getLatexFileData()
        self.style : Styles = style

    # return file code to write to a chapter
    def getFileRepr(self) -> str:
        if self.config.assumeFileFormat == 'question-solution':
            return self.style.applyQuestionStyle(self.question_code, f'\\input{{{self.filename}}}\n')
        elif self.config.assumeFileFormat == 'include-all-post-fi':
            return f'\\input{{{self.filename}}}\n'


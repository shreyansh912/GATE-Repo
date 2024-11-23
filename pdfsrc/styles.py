
from .settings import *

class Styles:
    def __init__(self, config : Settings):
        with open(config['pdf.styles.chapter']) as f:
            self.chapter : str = f.read()

        with open(config['pdf.styles.question']) as f:
            self.question : str = f.read()
            
        with open(config['pdf.styles.section']) as f:
            self.section : str = f.read()
        
        self.stylemacro = config['pdf.styles.macro']
        self.sectionsinfo = config['pdf.sections']

        # if the style macros were not found, print warning
        if self.chapter.find(self.stylemacro + '{chapter}') == -1:
            config.log(f'Warning: Did not find style macro {config["pdf.styles.macro"]}{{chapter}} in chapter style file {config["pdf.styles.chapter"]}')
        if self.question.find(self.stylemacro + '{question}') == -1:
            config.log(f'Warning: Did not find style macro {config["pdf.styles.macro"]}{{question}} in question style file {config["pdf.styles.question"]}')
        if self.question.find(self.stylemacro + '{solution}') == -1:
            config.log(f'Warning: Did not find style macro {config["pdf.styles.macro"]}{{solution}} in question style file {config["pdf.styles.question"]}')
    
    def applyChapterStyle(self, latex_code : str):
        return self.chapter.replace(self.stylemacro + '{chapter}', latex_code, 1)

    def applySectionStyle(self, section_alias, latex_code : str):
        return self.section.replace(self.stylemacro + '{section.name}', self.sectionsinfo[section_alias]['name'], 1).replace(self.stylemacro + '{section}', latex_code, 1)

    def applyQuestionStyle(self, latex_code_question : str, latex_code_soln : str):
        return self.question.replace(self.stylemacro + '{question}', latex_code_question).replace(self.stylemacro + '{solution}', latex_code_soln)

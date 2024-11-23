

class AuthorCell:
    def __init__(self, author : str):
        self.author = author
        self.solutions = []
        self.questions = []

    def addSolution(self, texfile : str):
        self.solutions.append(texfile)
    def addQuestion(self, texfile : str):
        self.questions.append(texfile)
    
    def __repr__(self) -> str:
        repr : str = self.author + ':\n'

        repr += '\tSolutions:\n'
        for soln in self.solutions:
            repr += f'\t\t{soln}\n'
        
        repr += '\tQuestions:\n'
        for ques in self.questions:
            repr += f'\t\t{ques}\n'
        return repr

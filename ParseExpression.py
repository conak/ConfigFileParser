
import re

class ExpressionElement:
    def __init__(self, text):
        self._text = text
    def getText(self):
        return self._text

class CodeText(ExpressionElement):
    pass
    
# cat(drive, ":\\")

def parseStringLiterals(text):
    tokens = []
    
    # note that regex string literal is not a raw string!  (necessary for escaping quotes)
    CODE_TEXT = re.compile("[^\"\']+")
    STRING_LITERAL_DOUBLE_QUOTE = re.compile(r'"(?:\\"|[^"])*"')
    
    pos = 0
    while pos < len(text):
        
    

tokens = []
tokens.append(ExpressionCode("cat(drive, "))
tokens.append(ExpressionStringLiteral(r'":\\"'))
tokens.append(ExpressionCode(")"))

tokens = []
tokens.append(ExpressionSymbol("cat"))
tokens.append(ExpressionLeftParen("("))
tokens.append(ExpressionSymbol("drive"))
tokens.append(ExpressionComma(","))
tokens.append(ExpressionWhitespace(" "))
tokens.append(ExpressionTextQualifier('"'))
tokens.append(ExpressionStringLiteral(":"))
tokens.append(ExpressionStringEscape(r"\\"))
tokens.append(ExpressionTextQualifier('"'))
tokens.append(ExpressionRightParen("("))



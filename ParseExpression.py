
import re
from readStringLiteral import readStringLiteral

class ExpressionElement:
    def __init__(self, text):
        self._text = text
    def getText(self):
        return self._text
    def __str__(self):
        return self.__class__.__name__ + "('" + self._text + "')"

class CodeText(ExpressionElement):
    pass

class QuotedString(ExpressionElement):
    pass
    
def parseStringLiterals(text):
    tokens = []
    
    # note that regex string literal is not a raw string!  (necessary for escaping quotes)
    CODE_TEXT = re.compile("[^\"\']+")
    
    pos = 0
    while pos < len(text):
        m_CODE_TEXT = CODE_TEXT.match(text[pos:])
        string_literal_text = readStringLiteral(text[pos:])
        
        if m_CODE_TEXT:
            tokens.append(CodeText(m_CODE_TEXT.group(0)))
            pos += len(m_CODE_TEXT.group(0))
        elif string_literal_text is not None:
            tokens.append(QuotedString(string_literal_text))
            pos += len(string_literal_text)
        else:
            raise Exception("Parse fail: " + text[pos:])
    
    return tokens

# cat(drive, ":\\")
text = r'cat(drive, ":\\")'
    
for token in parseStringLiterals(text):
    print(token)

# tokens = []
# tokens.append(ExpressionCode("cat(drive, "))
# tokens.append(ExpressionStringLiteral(r'":\\"'))
# tokens.append(ExpressionCode(")"))

# tokens = []
# tokens.append(ExpressionSymbol("cat"))
# tokens.append(ExpressionLeftParen("("))
# tokens.append(ExpressionSymbol("drive"))
# tokens.append(ExpressionComma(","))
# tokens.append(ExpressionWhitespace(" "))
# tokens.append(ExpressionTextQualifier('"'))
# tokens.append(ExpressionStringLiteral(":"))
# tokens.append(ExpressionStringEscape(r"\\"))
# tokens.append(ExpressionTextQualifier('"'))
# tokens.append(ExpressionRightParen("("))



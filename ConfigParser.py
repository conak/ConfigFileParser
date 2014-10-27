
import sys
import re

EXIT_PARSE_SUCCESS = 0
EXIT_PARSE_FAIL = 1

class ConfigParserException(Exception):
    pass

class UnrecognizedTokenTypeException(ConfigParserException):
    pass
class ParseFailException(ConfigParserException):
    pass
class DuplicateKeyException(ConfigParserException):
    pass
class KeyValuePairingException(ConfigParserException):
    pass
class UndefinedKeyException(ConfigParserException):
    pass

class Token:
    def __init__(self, typeName, text):
        self._typeName = typeName
        self._text = text
    def getTypeName(self):
        return self._typeName
    def getText(self):
        return self._text
    def __str__(self):
        return self.getTypeName() + '("' + self.getText() + '")'

class KeyValueObject:
    def __str__(self):
        return self.__class__.__name__ + '("' + self.getText() + '")'

class KeyObject(KeyValueObject):
    def __init__(self, text):
        self._text = text
    def getText(self):
        return self._text
    
class ValueObject(KeyValueObject):
    def __init__(self, tokens):
        self._tokens = tokens
        self._symbolDict = None
    def setSymbolDict(self, symbolDict):
        self._symbolDict = symbolDict
    def getText(self):
        out = ""
        for token in self._tokens:
            if token.getTypeName() == "literal_text":
                out += token.getText()
            elif token.getTypeName() == "symbol":
                if token.getText() not in self._symbolDict:
                    raise UndefinedKeyException("Undefined key: " + token.getText())
                out += self._symbolDict[token.getText()].getText()
            else:
                raise UnrecognizedTokenTypeException("Unrecognized token type in ValueObject: '" + token.getTypeName() + "'")
        
        return out
    def __str__(self):
        out = ""
        out += "ValueObject("
        for i in range(len(self._tokens)):
            out += str(self._tokens[i])
            if i < len(self._tokens) - 1:
                out += ", "
        out += ")"
        
        return out
        
def parseItems(text):
    KEY_VALUE = re.compile(r"^([A-Za-z_][A-Za-z_0-9]*)(?:(\s+)(.*))?$")
    COMMENT = re.compile(r"^\#")
    
    tokens = []
    lines = text.split("\n")
    for line in lines:
        m_KEY_VALUE = KEY_VALUE.match(line)
        m_COMMENT = COMMENT.match(line)
        if line == "":
            tokens.append(Token("blank_line", ""))
        elif m_COMMENT:
            tokens.append(Token("comment", line))
        elif m_KEY_VALUE:
            tokens.append(Token("key", m_KEY_VALUE.group(1)))
            if m_KEY_VALUE.group(2) is not None:
                tokens.append(Token("whitespace", m_KEY_VALUE.group(2)))
            if m_KEY_VALUE.group(3) is not None:
                tokens.append(Token("value", m_KEY_VALUE.group(3)))
        else:
            raise ParseFailException("Parse fail: '" + line + "'")
    
    return tokens

def parseValueToken(token):
    tokens = []
    
    LITERAL_TEXT = re.compile(r"^[^{]+")
    EXPRESSION = re.compile(r"^\{([A-Za-z_][A-Za-z_0-9]*)\}")
    
    text = token.getText()
    pos = 0
    while pos < len(text):
        m_LITERAL_TEXT = LITERAL_TEXT.match(text[pos:])
        m_EXPRESSION = EXPRESSION.match(text[pos:])
        if m_LITERAL_TEXT:
            tokens.append(Token("literal_text", m_LITERAL_TEXT.group(0)))
            pos += len(m_LITERAL_TEXT.group(0))
        elif m_EXPRESSION:
            tokens.append(Token("symbol", m_EXPRESSION.group(1)))
            pos += len(m_EXPRESSION.group(0))
        else:
            raise ParseFailException("Parse fail: '" + text[pos:] + "'")
    
    return ValueObject(tokens)
    
def parseValues(itemTokens):
    objects = []
    for token in itemTokens:
        if token.getTypeName() == "key":
            objects.append(KeyObject(token.getText()))
        elif token.getTypeName() == "value":
            objects.append(parseValueToken(token))
    return objects

def parseConfigText(text):
    object_list = parseValues(parseItems(text))
    object_dict = {
        "__LEFT_CURLY_BRACE__": ValueObject([Token("literal_text", "{")]),
        "__RIGHT_CURLY_BRACE__": ValueObject([Token("literal_text", "}")]),
        "__SPACE__": ValueObject([Token("literal_text", " ")]),
        "__TAB__": ValueObject([Token("literal_text", "\t")]),
    }
    i = 0
    while i < len(object_list):
        if isinstance(object_list[i], KeyObject):
            key_name = object_list[i].getText()
            if key_name in object_dict:
                raise DuplicateKeyException("Duplicate key: " + key_name)
            value = None
            if i < len(object_list) - 1 and isinstance(object_list[i + 1], ValueObject):
                object_dict[key_name] = object_list[i + 1]
                i += 2
            else:
                object_dict[key_name] = ValueObject([])
                i += 1
        else:
            raise KeyValuePairingException("Key/value pairing error")


    for key in object_dict:
        object_dict[key].setSymbolDict(object_dict)
            
    config_dict = {}
    for key in object_dict:
        config_dict[key] = object_dict[key].getText()
    
    return config_dict
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ConfigParser.py config_file")
        exit(1)
    config_text = ""
    with open(sys.argv[1], "rt") as f:
        config_text = f.read()
    
    try:
        config_dict = parseConfigText(config_text)
    except ConfigParserException as e:
        print("Config file parse failed")
        print(e)
        exit(EXIT_PARSE_FAIL)
    
    print("Config file parse succeeded")
    print("Config parameter dump:\n")
    
    for key in config_dict:
        print(key + ": " + config_dict[key])

    
    exit(EXIT_PARSE_SUCCESS)
    

import re

def readStringLiteral(text):
    STRING_LITERAL_DOUBLE_QUOTED = re.compile(r'(?:\\.|[^"])*')
    STRING_LITERAL_SINGLE_QUOTED = re.compile(r"(?:\\.|[^'])*")
    
    out = None
    
    if len(text) >= 2:
        if text[0] == '"' or text[0] == "'":
            text_qualifier = text[0]
            regex = None
            if text_qualifier == '"':
                regex = STRING_LITERAL_DOUBLE_QUOTED
            elif text_qualifier == "'":
                regex = STRING_LITERAL_SINGLE_QUOTED
            else:
                assert(False)
            
            m0 = regex.match(text[1:])
            if m0:
                if len(text) > len(m0.group(0)) + 1 and text[len(m0.group(0)) + 1] == text_qualifier:
                    out = text_qualifier + m0.group(0) + text_qualifier
    return out

if __name__ == "__main__":
    with open("string_literal_test.txt", "rt") as f:
        for line in f:
            if line.replace("\n", "") != "":
                components = line.replace("\n", "").split("\t")
                q = components[0]
                k = components[1]
                
                if readStringLiteral(q)[1:-1] != k:
                    print("TEST FAILED")
                    print("Input: [" + q + "]")
                    print("Expected: [" + k + "]")
                    print("Returned: [" + readStringLiteral(q)[1:-1] + "]")
                    print()

    with open("string_parse_fail_test.txt", "rt") as f:
        for line in f:
            q = line.replace("\n", "")
            if q != "":
                if readStringLiteral(q) is not None:
                    print("TEST FAILED")
                    print("Input: [" + q + "]")
                    print("Expected parse fail")
                    print()




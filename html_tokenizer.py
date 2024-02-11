import tokens

class Tokenizer:
    def __init__(self, content: str):
        self.content = content
        self.position = -1
        self.line = -1
        self.column = -1
        self.current_character = None

    def advance(self):
        self.position += 1
        self.column += 1

        if self.position >= len(self.content):
            raise RuntimeError('error')

        self.current_character = self.content[self.position]

    def parse_string(self):
        start_quote = self.current_character

        self.advance()

        string_end = self.content.find(start_quote, self.position)
        if string_end == -1:
            raise RuntimeError('error')

        token_content = self.content[self.position : string_end]

        self.column += string_end - self.position
        self.position = string_end

        return tokens.String(token_content)

    def parse_identifier(self):
        token_content = ""

        while self.current_character.isalnum():
            token_content += self.current_character
            self.advance()

        self.position -= 1
        self.column -= 1

        return tokens.Identifier(token_content)

    def skip_whitespaces(self):
        while self.current_character in ' \t\r\n':
            if self.current_character == '\n':
                self.line += 1
                self.column = -1

            self.advance()

    def get_token(self):
        if self.position + 1 >= len(self.content):
            return tokens.EndOfFile()

        self.advance()

        self.skip_whitespaces()

        if self.current_character == '<':
            self.advance()
            self.skip_whitespaces()

            if self.current_character == '/':
                return tokens.OpenTagSlash()

            self.position -= 1
            self.column -= 1
                
            return tokens.OpenTag()

        elif self.current_character == '>':
            return tokens.CloseTag()

        elif self.current_character == '"':
            return self.parse_string()

        elif self.current_character == '=':
            return tokens.Equals()
        
        return self.parse_identifier()

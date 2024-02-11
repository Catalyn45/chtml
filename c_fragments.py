class CPrelude:
    def __init__(self):
        self.content = """
            #include <stdlib.h>
            #include <stdio.h>

            void print_number(int number) {
                printf("%d\\n", number);
            }

            void print_string(char* string) {
                printf("%s\\n", string);
            }

            char at_index(char* string, int position) {
                return string[position];
            }

            void write_index(char* string, int position, char value) {
                string[position] = value;
            }
        """

    def build(self):
        return self.content

class CStatementsFragment:
    def __init__(self):
        self.content = """
            {statements}
        """

    def add_statement(self, statement):
        self.content = self.content.replace("{statements}", statement + "\n{statements}")

    def build(self):
        return self.content.replace("{statements}", "")

class CIfStatementFragment:
    def __init__(self):
        self.content = """if ({condition}) {
                {true_statements}
            } else {
                {false_statements}
            }
        """

    def set_condition(self, condition):
        self.content = self.content.replace("{condition}", condition)

    def add_true_statement(self, statement):
        self.content = self.content.replace("{true_statements}", statement + "\n{true_statements}")

    def add_false_statement(self, statement):
        self.content = self.content.replace("{false_statements}", statement + "\n{false_statements}")

    def build(self):
        return self.content.replace("{true_statements}", "").replace("{false_statements}", "")

class CWhileStatementFragment():
    def __init__(self):
        self.content = """while (1) {
            {statements}
        }
        """

    def add_statement(self, statement):
        self.content = self.content.replace("{statements}", statement + "\n{statements}")

    def build(self):
        return self.content.replace("{statements}", "")

class CFunctionFragment:
    def __init__(self):
        self.content = """
            {return_type} {function_name}({parameters}) {
                {statements}
            }
        """

    def set_return_type(self, return_type):
        self.content = self.content.replace("{return_type}", return_type)

    def set_function_name(self, function_name):
        self.content = self.content.replace("{function_name}", function_name)

    def add_parameter(self, parameter):
        parameters_pos = self.content.find("{parameters}")
        if self.content[parameters_pos - 1] != "(":
            self.content = self.content.replace("{parameters}", ", {parameters}")

        self.content = self.content.replace("{parameters}", parameter + "{parameters}")

    def add_statement(self, statement):
        self.content = self.content.replace("{statements}", statement + "\n{statements}")

    def build(self):
        return self.content.replace("{statements}", "").replace("{parameters}", "")

class CExpressionFragment:
    def __init__(self, operator=None, content=""):
        self.operator = operator
        self.content = content

    def add_expression(self, expression):
        if self.content != "" and self.operator is not None:
            self.content += f" {self.operator} "

        self.content += expression

    def build(self, paranthesis=True):
        if self.operator is None:
            paranthesis = False

        return (paranthesis and "(" or "") + self.content + (paranthesis and ")" or "")
        
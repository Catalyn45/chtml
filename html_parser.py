import html_tokenizer
import tokens
import c_fragments

class Parser:
    def __init__(self, tokenizer: html_tokenizer.Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = None

    def advance(self):
        self.current_token = self.tokenizer.get_token()

    def parse_open_tag(self, out_props = {}):
        if type(self.current_token) is not tokens.OpenTag:
            raise RuntimeError('error')

        self.advance()
        if type(self.current_token) is not tokens.Identifier:
            raise RuntimeError('error')

        tag_name = self.current_token.content

        self.advance()
        while type(self.current_token) is tokens.Identifier:
            prop = self.current_token.content

            self.advance()
            if type(self.current_token) is not tokens.Equals:
                raise RuntimeError('error')

            self.advance()
            if type(self.current_token) is not tokens.String:
                raise RuntimeError('error')

            value = self.current_token.content
            out_props[prop] = value

            self.advance()

        if type(self.current_token) is not tokens.CloseTag:
            raise RuntimeError('error')

        self.advance()
        return tag_name

    def parse_close_tag(self, close_tag_name):
        if type(self.current_token) is not tokens.OpenTagSlash:
            raise RuntimeError('error')

        self.advance()
        if type(self.current_token) is not tokens.Identifier:
            raise RuntimeError('error')

        tag_name = self.current_token.content
        if tag_name != close_tag_name:
            raise RuntimeError('error')

        self.advance()
        if type(self.current_token) is not tokens.CloseTag:
            raise RuntimeError('error')

        self.advance()

    def parse_script(self):
        self.parse_close_tag('script')
    
    def parse_scripts(self):
        while type(self.current_token) is not tokens.OpenTagSlash:
            tag_name = self.parse_open_tag()

            if tag_name != 'script':
                raise RuntimeError('error')

            self.parse_script()

    def parse_head(self):
        tag_name = self.parse_open_tag()

        if tag_name != "head":
            raise RuntimeError('error')

        self.parse_scripts()

        self.parse_close_tag(tag_name)

    def parse_parameter(self):
        parameter = self.current_token
        self.advance()

        print(parameter)

        self.parse_close_tag('li')

    def parse_parameters(self, fragment):
        while type(self.current_token) != tokens.OpenTagSlash:
            props = {}
            tag_name = self.parse_open_tag(props)

            if tag_name != 'li':
                raise RuntimeError('error')

            if type(self.current_token) is not tokens.Identifier:
                raise RuntimeError('error')

            fragment.add_parameter(f"{props['class']} {self.current_token.content}")

            self.advance()

            self.parse_close_tag('li')

        self.parse_close_tag('ol')

    def parse_expression_statement(self, tag_name, props, fragment):
        expression_fragment = c_fragments.CExpressionFragment()

        self.parse_expression(expression_fragment, tag_name, props)

        statement_string = expression_fragment.build() + ";\n"

        fragment.add_statement(statement_string)


    def parse_expressions(self, fragment):
        while type(self.current_token) is not tokens.OpenTagSlash:
            self.parse_expression(fragment)

    def parse_number(self, fragment):
        fragment.add_expression(self.current_token.content)
        self.advance()

    def parse_string(self, fragment):
        fragment.add_expression('"' + self.current_token.content + '"')
        self.advance()

    def parse_add(self, fragment):
        add_fragment = c_fragments.CExpressionFragment('+')

        self.parse_expressions(add_fragment)

        self.parse_close_tag('h1')

        fragment.add_expression(add_fragment.build())

    def parse_minus(self, fragment):
        minus_fragment = c_fragments.CExpressionFragment('-')

        self.parse_expressions(minus_fragment)

        self.parse_close_tag('h2')

        fragment.add_expression(minus_fragment.build())

    def parse_multipy(self, fragment):
        multiply_fragment = c_fragments.CExpressionFragment('*')

        self.parse_expressions(multiply_fragment)

        self.parse_close_tag('h3')

        fragment.add_expression(multiply_fragment.build())


    def parse_division(self, fragment):
        division_fragment = c_fragments.CExpressionFragment('/')

        self.parse_expressions(division_fragment)

        self.parse_close_tag('h4')

        fragment.add_expression(division_fragment.build())

    def parse_and(self, fragment):
        and_fragment = c_fragments.CExpressionFragment('&&')

        self.parse_expressions(and_fragment)

        self.parse_close_tag('h5')

        fragment.add_expression(and_fragment.build())

    def parse_or(self, fragment):
        or_fragment = c_fragments.CExpressionFragment('||')

        self.parse_expressions(or_fragment)

        self.parse_close_tag('h6')

        fragment.add_expression(or_fragment.build())

    def parse_not(self, fragment):
        not_fragment = c_fragments.CExpressionFragment(content="!")
        self.parse_expression(not_fragment)

        self.parse_close_tag('u')

        fragment.add_expression(not_fragment.build())

    def parse_equals(self, fragment):
        equal_fragment = c_fragments.CExpressionFragment('==')

        self.parse_expression(equal_fragment)
        self.parse_expression(equal_fragment)

        self.parse_close_tag('i')

        fragment.add_expression(equal_fragment.build())


    def parse_less(self, fragment):
        less_fragment = c_fragments.CExpressionFragment('<')

        self.parse_expression(less_fragment)
        self.parse_expression(less_fragment)

        self.parse_close_tag('b')

        fragment.add_expression(less_fragment.build())


    def parse_greater(self, fragment):
        greater_fragment = c_fragments.CExpressionFragment('>')

        self.parse_expression(greater_fragment)
        self.parse_expression(greater_fragment)

        self.parse_close_tag('strong')

        fragment.add_expression(greater_fragment.build())


    def parse_variable_reference(self, props, fragment):
        fragment.add_expression(props['href']) 

    def parse_argument(self, fragment):
        tag_name = self.parse_open_tag()

        if tag_name != 'li':
            raise RuntimeError('error')
        
        self.parse_expression(fragment)

        self.parse_close_tag('li')

    def parse_call(self, props, fragment):
        arguments_fragment = c_fragments.CExpressionFragment(",")

        while type(self.current_token) is not tokens.OpenTagSlash:
            self.parse_argument(arguments_fragment)

        self.parse_close_tag('ul')

        fragment.add_expression(props['id'] + arguments_fragment.build())

    def parse_assignment(self, props, fragment):
        assignment_fragment = c_fragments.CExpressionFragment("=")

        assignment_fragment.add_expression(props['id'])

        self.parse_expression(assignment_fragment)

        self.parse_close_tag('span')

        expr_string = ""
        if props.get('class'):
            expr_string += props['class'] + " "

        expr_string += assignment_fragment.build(paranthesis=False)

        fragment.add_expression(expr_string)


    def parse_primitive(self, fragment):
        if type(self.current_token) is tokens.Identifier:
            self.parse_number(fragment)

        elif type(self.current_token) is tokens.String:
           self.parse_string(fragment)
        else:
            raise RuntimeError()

        self.parse_close_tag('p')

    def parse_expression(self, fragment, tag_name=None, props=None):
        if type(self.current_token) is not tokens.OpenTagSlash:
            if tag_name is None:
                props={}
                tag_name = self.parse_open_tag(props)

            if tag_name == 'p':
                self.parse_primitive(fragment)
            elif tag_name == 'h1':
                self.parse_add(fragment)
            elif tag_name == 'h2':
                self.parse_minus(fragment)
            elif tag_name == 'h3':
                self.parse_multipy(fragment)
            elif tag_name == 'h4':
                self.parse_division(fragment)
            elif tag_name == 'h5':
                self.parse_and(fragment)
            elif tag_name == 'h6':
                self.parse_or(fragment)
            elif tag_name == 'u':
                self.parse_not(fragment)
            elif tag_name == 'i':
                self.parse_equals(fragment)
            elif tag_name == 'b':
                self.parse_less(fragment)
            elif tag_name == 'strong':
                self.parse_greater(fragment)
            elif tag_name == 'link':
                self.parse_variable_reference(props, fragment)
            elif tag_name == 'ul':
                self.parse_call(props, fragment)
            elif tag_name == 'span':
                self.parse_assignment(props, fragment)
            else:
                raise RuntimeError('error')

    def parse_loop(self, fragment):
        loop_fragment = c_fragments.CWhileStatementFragment()

        self.parse_statements(loop_fragment)

        self.parse_close_tag('textarea')

        fragment.add_statement(loop_fragment.build())

    def parse_if(self, fragment):
        condition_fragment = c_fragments.CIfStatementFragment()

        # parse condition
        tag_name = self.parse_open_tag()
        if tag_name != 'thead':
            raise RuntimeError('error')

        expression_fragment = c_fragments.CExpressionFragment()
        self.parse_expression(expression_fragment)

        self.parse_close_tag('thead')

        condition_fragment.set_condition(expression_fragment.build())

        true_statements = c_fragments.CStatementsFragment()
        # parse true side
        tag_name = self.parse_open_tag()
        if tag_name != 'tbody':
            raise RuntimeError('error')

        self.parse_statements(true_statements)

        self.parse_close_tag('tbody')

        condition_fragment.add_true_statement(true_statements.build())

        # parse false side
        if type(self.current_token) is not tokens.OpenTagSlash:
            false_statements = c_fragments.CStatementsFragment()
            tag_name = self.parse_open_tag()
            if tag_name != 'tfoot':
                raise RuntimeError('error')

            self.parse_statements(false_statements)

            self.parse_close_tag('tfoot')

            condition_fragment.add_false_statement(false_statements.build())
        
        self.parse_close_tag('table')

        fragment.add_statement(condition_fragment.build())

    def parse_return(self, fragment):
        expression_fragment = c_fragments.CExpressionFragment()
        self.parse_expression(expression_fragment)

        self.parse_close_tag('a')

        fragment.add_statement("return " + expression_fragment.build() + ";\n")

    def parse_break(self, fragment):
        fragment.add_statement("break;\n") 

    def parse_statement(self, fragment):
        props = {}
        tag_name = self.parse_open_tag(props)

        if tag_name == 'ol':
            self.parse_parameters(fragment)
        elif tag_name == 'textarea':
            self.parse_loop(fragment)
        elif tag_name == 'table':
            self.parse_if(fragment)
        elif tag_name == 'a':
            self.parse_return(fragment)
        elif tag_name == 'hr':
            self.parse_break(fragment)
        else:
            self.parse_expression_statement(tag_name, props, fragment)

    def parse_statements(self, fragment):
        while type(self.current_token) is not tokens.OpenTagSlash:
            self.parse_statement(fragment)

    def parse_div(self, props, statements_fragment):
        function_fragment = c_fragments.CFunctionFragment()

        function_fragment.set_function_name(props['id'])
        function_fragment.set_return_type(props['class'])

        self.parse_statements(function_fragment)

        self.parse_close_tag('div')

        statements_fragment.add_statement(function_fragment.build())


    def parse_divs(self, fragment):
        while type(self.current_token) is not tokens.OpenTagSlash:
            props = {}
            tag_name = self.parse_open_tag(props)

            if tag_name != "div":
                raise RuntimeError('error')

            self.parse_div(props, fragment)

    def parse_body(self, fragment):
        tag_name = self.parse_open_tag()

        if tag_name != "body":
            raise RuntimeError('error')

        self.parse_divs(fragment) 

        self.parse_close_tag(tag_name)

    def parse(self):
        self.advance()

        tag_name = self.parse_open_tag()

        if tag_name != 'html':
            raise RuntimeError('error')
        
        statements_fragment = c_fragments.CStatementsFragment()

        self.parse_head()
        self.parse_body(statements_fragment)

        self.parse_close_tag(tag_name)

        c_prelude = c_fragments.CPrelude()

        return c_prelude.build() + statements_fragment.build()

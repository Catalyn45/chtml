# CHTML

This is a transpiler which transforms the HTML markup language into a full working turing complete programming language.

## How to use

`python ./main.py <input_html_name> <output_binary_name>`

example:  
    `python ./main.py ./programs/fibonacci.html output`

## Documentation

As a generale rule, the `id` property is considered the identifier and `class` property is considered the type.

### Minimal program:
```html
<html>
    <head></head>
    <body>
        <div id="main" class="int">
        </div>
    </body>
</html>
```

### Primitives:  
numbers
```html
<p>10</p>
```

strings
```html
<p>"hello"</p>
```

### Expressions
Add `10` and `20`
```html
<h1>
    <p>10</p>
    <p>20</p>
</h1>
```

Subtract `10` from `20`
```html
<h2>
    <p>20</p>
    <p>10</p>
</h2>
```

Multiply `10` and `20`
```html
<h3>
    <p>10</p>
    <p>20</p>
</h3>
```

Divide `20` by `10`
```html
<h4>
    <p>20</p>
    <p>10</p>
</h4>
```

Add variable `a` and 10
```html
<h1>
    <link href="a">
    <p>10</p>
</h1>
```

Check if `a` and `b` are true
```html
<h5>
    <link href="a">
    <link href="b">
</h5>
```

Check if `a` or `b` are true
```html
<h6>
    <link href="a">
    <link href="b">
</h6>
```

Not `a`
```html
<u>
    <link href="a">
</u>
```

Check if `a` equals `b`
```html
<i>
    <link href="a">
    <link href="b">
</i>
```

Check if `a` is less than `b`
```html
<b>
    <link href="a">
    <link href="b">
</b>
```

Check if `a` is greater than `b`
```html
<strong>
    <link href="a">
    <link href="b">
</strong>
```

Call function `fibonacci` with argument `5`
```html
<ul id="fibonacci">
    <li><p>5</p></li>
</ul>
```

### Statements
create a new variable `a` of type `int` which will be
initializated with `10`.
```html
<span id="a" class="int">
    <p>10</p>
</span>
```

change the value of variable `a` to `20` ( we don't use the `class` property)
```html
<span id="a">
    <p>20</p>
</span>
```

create an if statement. the `thead` is the condition for the if statement, `tbody` are the statements if the for the true branch and `tfoot` the statements for the false branch.
```html
<table>
    <thead>
        <b>
            <link href="a">
            <p>20</p>
        </b>
    <thead>
    <tbody>
        <ul id="print">
            <li><p>"success"</p></li>
        </ul>
    </tbody>
    <tfoot>
        <ul id="print">
            <li><p>"failure"</p></li>
        </ul>
    </tfoot>
</table>
```

create an infinite loop with `textarea`, and use the `hr` to break from the loop
```html
<textarea>
    <table>
        <thead>
            <b>
                <link href="a">
                <p>0<p>
            </b>
        <thead>

        <tbody>
            <hr>
        </tbody>
    </table>
<textarea>
```

### Functions
Create a new function named `fibonacci` which will return an `int`
```html
<div id="fibonacci" class="int">
</div>
```

### Parameters
Fibonacci function will receive a parameter of type `int` identified `n`. The parameters declaration location doesn't need to be at the begining of the function
```html
<div id="fibonacci" class="int">
    <ol>
        <li class="int">n</li>
    </ol>
</div>
```

### Return
Fibonacci function will return the number `10`
```html
<div id="fibonacci" class="int">
    <a>
        <p>10</p>
    </a>
</div>
```

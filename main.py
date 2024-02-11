import html_tokenizer
import html_parser
import sys
import os

def main():
    input_file = sys.argv[1] 
    output_file = sys.argv[2] 

    print(input_file, output_file)

    with open(input_file) as f:
        input = f.read()

    tokenizer = html_tokenizer.Tokenizer(input)
    parser =  html_parser.Parser(tokenizer)

    output_content = parser.parse()

    with open(f"{output_file}.c", 'w') as f:
        f.write(output_content)

    if sys.platform == "linux":
        os.system(f"gcc -i {output_file}.c -o {output_file}")
    elif sys.platform == "win32":
        os.system(f"cl -i {output_file}.c -o {output_file}.exe")
    else:
        print('Unsupported os, compile the generated C file yourself')

if __name__ == "__main__":
    main()
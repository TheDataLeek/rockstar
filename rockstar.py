#!/usr/bin/env python3.6

import sys
import argparse
import pathlib
import lark
from fabulous import color


parser = lark.Lark(r'''
    start: (expression newline)+

    newline: "\n"

    blank: newline newline

    expression: newline
              | function
              | block
              | input
              | output
              | loop
              | conditional
              | math
              | increment
              | decrement
              | assign
              | pronoun
              | literal
              | variable
              | blank

    function: function_start expression+ function_end return
        function_start: variable "takes" variable( "and" variable)*
        return: "Give back" expression
        function_end: blank

    block: block_start block_end
        block_start: conditional
                   | loop
        block_end: blank

    output: output_token expression
        output_token: "Say"
                    | "Shout"
                    | "Whisper"
                    | "Scream"

    loop: loop_token expression loop_end
        loop_token: "While"
                  | "Until"
        loop_end: break
                | continue
            break: "break" | /[Bb]reak it down/
            continue: "continue" | /[Tt]ake it to the top/

    input: /[Ll]isten/ ["to" variable]

    conditional: /[Ii]f/ expression comparison_token expression [/[Ee]lse/ expression]
        comparison_token: equals
                        | not_equals
                        | greater_than
                        | less_than
                        | greater_than_or_equal_to
                        | less_than_or_equal_to
            equals: "is"
            not_equals: "is not"
                      | "ain't"
            greater_than: "is" greater_token "than"
                greater_token: "higher"
                             | "greater"
                             | "bigger"
                             | "stronger"
            less_than: "is" less_token "than"
                less_token: "lower"
                          | "less"
                          | "smaller"
                          | "weaker"
            less_than_or_equal_to: "is as" less_than_or_equal_token "as"
                less_than_or_equal_token: "low"
                                        | "little"
                                        | "small"
                                        | "weak"
            greater_than_or_equal_to: "is as" greater_than_or_equal_token "as"
                greater_than_or_equal_token: "high"
                                           | "great"
                                           | "big"
                                           | "strong"

    math: plus
        | minus
        | times
        | over
        plus: expression plus_token expression
            plus_token: "plus"
                      | "with"
        minus: expression minus_token expression
            minus_token: "minus"
                       | "without"
        times: expression times_token expression
            times_token: "times"
                       | "of"
        over: expression over_token expression
            over_token: "over"
                      | "by"

    increment: /[Bb]uild/ variable "up"
    decrement: /[Kk]nock/ variable "down"

    assign: /[Pp]ut/ expression /[Ii]nto/ variable

    pronoun: "it"
           | "he"
           | "she"
           | "him"
           | "her"
           | "them"
           | "they"

    comment: "(" [WORD( WORD)*] ")"

    variable: common_variable
            | proper_variable
        proper_variable: (UCASE_LETTER LCASE_LETTER*)+
        common_variable: common_token LCASE_LETTER+
            common_token: "a"
                        | "an"
                        | "the"
                        | "my"
                        | "your"

    poetic_literal: type_literal
                  | string_literal
                  | number_literal
        type_literal: variable "is" literal
        string_literal: variable "says" STRING_INNER
        number_literal: variable number_literal_token STRING_INNER
            number_literal_token: "is"
                                | "was"
                                | "were"

    literal: null
           | true
           | false
           | string
           | number
           | undefined
        true: "true"
            | "right"
            | "yes"
            | "ok"
        false: "false"
             | "wrong"
             | "no"
             | "lies"
        string: ESCAPED_STRING
        number: SIGNED_NUMBER
        undefined: "mysterious"
        null: "null"
            | "nothing"
            | "nowhere"
            | "nobody"

    %import common.UCASE_LETTER
    %import common.LCASE_LETTER
    %import common.WORD
    %import common.STRING_INNER
    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %import common.WS_INLINE
    %ignore WS_INLINE
''', start='start')


class Rockstar(lark.Transformer):
    def start(self, _):
        return None

    def expression(self, value):
        return value[0]

    def output(self, args):
        print(args[1])
        return None

    def comment(self, _):
        return None

    def assign(self, args):
        print(color.red(args))

    def pronoun(self, args):
        print(color.red(args))

    def literal(self, value):
        return value[0]

    def string(self, s):
        return s[0][1:-1]

    def null(self, _): None

    def undefined(self, _): None

    def true(self, _): True

    def false(self, _): False


def main():
    args = get_args()

    if len(args.files) == 0:
        path = pathlib.Path('.')
        for f in path.glob('*.rockstar'):
            execute_file(f, f.read_text())
    else:
        for filename in args.files:
            f = pathlib.Path(filename)
            execute_file(f, f.read_text())


def execute_file(filename, contents):
    print(color.green(filename))
    tree = parser.parse(contents)
    print(tree.pretty())
    print(Rockstar().transform(tree))


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', metavar='F', type=str, nargs='*',
                        help='File(s) to run')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    sys.exit(main())

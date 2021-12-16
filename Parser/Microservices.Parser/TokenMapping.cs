using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Compilation.Parser {

    static class TokenMapping {
        public enum Meaning {
            ProgramNameDefinition,
            VariableAssigning
        }

        public static readonly Table[] Grammars = new Table[] {
            new(Meaning.ProgramNameDefinition, new TableEntry[] { new(Modifer.Simple, new[] { Token.Program }),
                                                      new(Modifer.Simple, new[] { Token.InternalName }),
                                                      new(Modifer.Simple, new[] { Token.Semicolon })  }),

            new(Meaning.VariableAssigning, new TableEntry[] { new(Modifer.Simple, new[] { Token.InternalName }),
                                                      new(Modifer.Simple, new[] { Token.Assign }),
                                                      new(Modifer.Repeateble, new[] { Token.Integer, Token.InternalName, Token.ArithmeticOperator, Token.ParenthesisLeft, Token.ParenthesisRight }),
                                                      new(Modifer.Simple, new[] { Token.Semicolon })  })
        };


        public struct Table {
            public Table(Meaning mean, TableEntry[] sequence) {
                this.mean = mean;
                this.sequence = sequence;
            }

            public Meaning mean;
            public TableEntry[] sequence;
        }

        public struct TableEntry {
            public TableEntry(Modifer modifiers, Token[] tokens) {
                this.modifiers = modifiers;
                this.tokens = tokens;
            }

            public Modifer modifiers;
            public Token[] tokens;
        }

        public enum Modifer {
            Simple, //Just value set
            Nullable, //Allow to skip this set
            Repeateble, //Allow to repeat multiple times
            Not = 4 //Invert white-list set to a black-list set
        }

        public enum Token { //"_" - means "flexible" category (need more accurate recognition)
            Program, //program name definition keyword
            Begin, End, //code section
            Colon, //in this case, colon is keyword
            Dot, //End of program
            Comma, //Argument list or var def
            Semicolon, //End of phrase

            Var, //Varables definition or pointer
            IntegerDef, //DataType name: Integer
            Const, //Const var

            Assign, //Assing value to variable
            Exit, //Exit from the program

            //DataTypes
            InternalName, //Variable-valid sequence (variable, function-name, etc.)
            Integer, //Integer value (like 89)
            Boolean, //True or False values

            ParenthesisLeft, // (
            ParenthesisRight, // )

            ArithmeticOperator, //+, -, *, /, etc.
            LogicOperator, //and, or
            ComparsionOperator, // >, <, =, <>, <=, >=

            LoopFor, //for
            LoopFor_to, //1 to 9
            LoopFor_downto, //9 downto 1
            LoopWhile, //while
            Loop_do //while <condition> do
        }

        //([a-zA-Z_]\w*)|([\d+*\-\/]+)|(\((?:[a-zA-Z_]\w*|[\d+*\-\/]|((?3)))+\))
        public static readonly Dictionary<string, Token> TokenCvt = new(new KeyValuePair<string, Token>[] {
            new("program", Token.Program),
            new("begin", Token.Begin),
            new("end", Token.End),
            new("colon", Token.Colon),
            new("dot", Token.Dot),
            new("comma", Token.Comma),
            new("semicolon", Token.Semicolon),

            new("var", Token.Var),
            new("integer-word", Token.IntegerDef),
            new("const", Token.Const),

            new("assign", Token.Assign),
            new("exit", Token.Exit),

            new("internal-name", Token.InternalName),
            new("number", Token.Integer),
            new("boolean", Token.Boolean),

            new("left-parenthesis", Token.ParenthesisLeft),
            new("right-parenthesis", Token.ParenthesisRight),

            new("arithmetic-operator", Token.ArithmeticOperator),
            new("logic-operator", Token.LogicOperator), 
            new("comparsion-operator", Token.ComparsionOperator),

            new("for", Token.LoopFor),
            new("to", Token.LoopFor_to),
            new("downto", Token.LoopFor_downto),
            new("while", Token.LoopWhile),
            new("do", Token.Loop_do)
        });
    }
}

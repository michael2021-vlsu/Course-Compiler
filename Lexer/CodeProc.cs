using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace Compilation.Lexer {
    class CodeProc {
        string[] code;

        public CodeProc(string[] code) {
            this.code = code;
        }

        List<Program.Token> tokens = new();

        struct TapePos {
            public TapePos(byte method, string pattern, bool prohibitFollowLetters, string token, bool toLowerCase) {
                this.method = method;
                this.pattern = pattern;
                this.prohibitFollowLetters = prohibitFollowLetters;
                this.token = token;
                this.toLowerCase = toLowerCase;
            }
            public byte method; //0 - StartsWith, 1 - regex
            public string pattern;
            public bool prohibitFollowLetters;
            public string token;
            public bool toLowerCase;
        }

        TapePos[] tape = new TapePos[] {
            new(0, "program", true, "program", true),
            new(0, "procedure", true, "procedure", true),
            new(0, "begin", true, "begin", true),
            new(0, "end", true, "end", true),
            new(0, ":=", false, "assign", false),

            new(0, "var", true, "var", true),
            new(0, "integer", true, "integer-word", true),
            new(0, "const", true, "const", true),

            new(0, "exit", true, "exit", true),
            
            new(0, "(", false, "left-parenthesis", false),
            new(0, ")", false,"right-parenthesis", false),

            new(1, "^[+*\\-\\/]", false, "arithmetic-operator", false),
            new(0, "div", true, "arithmetic-operator", true),
            new(0, "mod", true, "arithmetic-operator", true),

            new(0, "and", true, "logic-operator", true),
            new(0, "or", true, "logic-operator", true),

            new(0, "<>", false, "comparsion-operator", false),
            new(0, "<=", false, "comparsion-operator", false),
            new(0, ">=", false, "comparsion-operator", false),
            new(0, "=", false, "comparsion-operator", false),
            new(0, "<", false, "comparsion-operator", false),
            new(0, ">", false, "comparsion-operator", false),
           
            new(0, "for", true, "for", true),
            new(0, "to", true, "to", true),
            new(0, "downto", true, "downto", true),
            new(0, "while", true, "while", true),
            new(0, "do", true, "do", true),

            new(0, ":", false, "colon", false),
            new(0, ".", false, "dot", false),
            new(0, ",", false, "comma", false),
            new(0, ";", false, "semicolon", false),

            new(0, "true", false, "boolean", true),
            new(0, "false", false, "boolean", true),

            new(1, "^[0-9]+", false, "number", false),
            new(1, "^[a-zA-Z_][a-zA-Z0-9_]+", false, "internal-name", false)
        };

        readonly char[] Letters = "abcdefghijklmnopqrstuvwxyz".ToCharArray();

        public Program.Output Run() {
            for (int linei = 0; linei != code.Length; ++linei) {
                string line = code[linei];
                StringBox[] lineparts = new StringBox(code[linei]).Split(' ');

                foreach (var part in lineparts) {
                    if (part.Length == 0) continue;

                    string token = null, strpart = part.ExtactString();
                    foreach (var pos in tape) {
                        if (pos.method == 0) {
                            if (pos.toLowerCase) {
                                var lw = strpart.ToLower();
                                if (pos.pattern == lw) {
                                    strpart = lw;
                                    token = pos.token;
                                    break;
                                }
                            } else {
                                if (pos.pattern == strpart) {
                                    token = pos.token;
                                    break;
                                }
                            }
                        } else {
                            if (pos.toLowerCase) {
                                var lw = strpart.ToLower();
                                if (Regex.IsMatch(lw, pos.pattern + '$')) {
                                    strpart = lw;
                                    token = pos.token;
                                    break;
                                }
                            } else {
                                if (Regex.IsMatch(strpart, pos.pattern + '$')) {
                                    token = pos.token;
                                    break;
                                }
                            }
                        }
                    }

                    if (token == null) {
                        do {
                            int initLen = strpart.Length;
                            foreach (var pos in tape) {
                                if (pos.method == 0) {
                                    if (pos.toLowerCase) {
                                        var lw = strpart.ToLower();
                                        if (lw.StartsWith(pos.pattern)) {
                                            if (pos.prohibitFollowLetters) {
                                                char c = lw[pos.pattern.Length];
                                                if (Letters.All(l => l != c)) {
                                                    tokens.Add(new Program.Token(pos.token, pos.pattern, linei, part.StartNumber));
                                                    strpart = part.RemoveSub(0, pos.pattern.Length).ExtactString();
                                                    break;
                                                }
                                            } else {
                                                tokens.Add(new Program.Token(pos.token, pos.pattern, linei, part.StartNumber));
                                                strpart = part.RemoveSub(0, pos.pattern.Length).ExtactString();
                                                break;
                                            }
                                        }
                                    } else {
                                        if (strpart.StartsWith(pos.pattern)) {
                                            if (pos.prohibitFollowLetters) {
                                                char c = char.ToLower(strpart[pos.pattern.Length]);
                                                if (Letters.All(l => l != c)) {
                                                    tokens.Add(new Program.Token(pos.token, pos.pattern, linei, part.StartNumber));
                                                    strpart = part.RemoveSub(0, pos.pattern.Length).ExtactString();
                                                    break;
                                                }
                                            } else {
                                                tokens.Add(new Program.Token(pos.token, pos.pattern, linei, part.StartNumber));
                                                strpart = part.RemoveSub(0, pos.pattern.Length).ExtactString();
                                                break;
                                            }
                                        }
                                    }
                                } else {
                                    if (pos.toLowerCase) {
                                        var lw = strpart.ToLower();
                                        var match = Regex.Match(lw, pos.pattern);
                                        if (match.Success) {
                                            if (pos.prohibitFollowLetters) {
                                                char c = lw[match.Value.Length];
                                                if (Letters.All(l => l != c)) {
                                                    tokens.Add(new Program.Token(pos.token, match.Value, linei, part.StartNumber));
                                                    strpart = part.RemoveSub(0, match.Value.Length).ExtactString();
                                                    break;
                                                }
                                            } else {
                                                tokens.Add(new Program.Token(pos.token, match.Value, linei, part.StartNumber));
                                                strpart = part.RemoveSub(0, match.Value.Length).ExtactString();
                                                break;
                                            }
                                        }
                                    } else {
                                        var match = Regex.Match(strpart, pos.pattern);
                                        if (match.Success) {
                                            if (pos.prohibitFollowLetters) {
                                                char c = char.ToLower(strpart[match.Value.Length]);
                                                if (Letters.All(l => l != c)) {
                                                    tokens.Add(new Program.Token(pos.token, match.Value, linei, part.StartNumber));
                                                    strpart = part.RemoveSub(0, match.Value.Length).ExtactString();
                                                    break;
                                                }
                                            } else {
                                                tokens.Add(new Program.Token(pos.token, match.Value, linei, part.StartNumber));
                                                strpart = part.RemoveSub(0, match.Value.Length).ExtactString();
                                                break;
                                            }
                                        }
                                    }
                                }
                            }
                            if (strpart.Length == initLen) {
                                return Program.Output.MakeFail("синтаксическая конструкция не может быть распознана: " + strpart, linei, part.StartNumber);
                            }
                        } while (strpart.Length != 0);
                    } else {
                        tokens.Add(new Program.Token(token, strpart, linei, part.StartNumber));
                    }
                }
            }

            return Program.Output.MakeSucess(tokens.ToArray());
        }
    }
}

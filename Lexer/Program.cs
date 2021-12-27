using System;
using System.Collections.Generic;
namespace Compilation.Lexer {
    class Program {
        static void Main(string[] args) {
            MicroServerAPI.MicroService mserv = new("http://localhost:8080/5-semestr/compiler/get-job", "http://localhost:8080/5-semestr/compiler/post-job", true);

            while (true) {
                Input session = mserv.GetJob<Input>("Compilation.Lexer", out MicroServerAPI.ResponseAddress address);

                CodeProc processor = new(session.source);
                Output output = processor.Run();

                mserv.PostFinalResult<Output>("Compilation.Lexer.Output", address, output);
            }
        }

        struct Input {
            public string session_id;
            public string[] source;
        }

        public struct Token {
            public Token(string type, string content, int line, int column) {
                this.type = type;
                this.content = content;
                this.line = line;
                this.column = column;
            }

            public string type,
                content;
            public int line,
                column;
        }

        public struct Output {
            public static Output MakeFail(string errorDesc, int errorLine, int errorColumn) {
                var outp = new Output();
                outp.success = false;
                outp.tokens = null;
                outp.errorDesc = errorDesc;
                outp.errorLine = errorLine;
                outp.errorColumn = errorColumn;
                return outp;
            }

            public static Output MakeSucess(Token[] tokens) {
                var outp = new Output();
                outp.success = true;
                outp.tokens = tokens;
                outp.errorDesc = null;
                outp.errorLine = 0;
                outp.errorColumn = 0;
                return outp;
            }

            public bool success;
            public string errorDesc;
            public int errorLine,
                errorColumn;

            public Token[] tokens;
        }
    }
}

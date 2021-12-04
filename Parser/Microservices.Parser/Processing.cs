using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Compilation.Parser.IOstructs;
using Compilation.Parser.AST;

namespace Compilation.Parser {
    partial class Processor {
        Input input;

        public Processor(Input input) {
            this.input = input;
        }

        public Output Run() {

            return new();
        }
    }
}

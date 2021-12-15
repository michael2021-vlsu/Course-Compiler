using Compilation.Parser.AST;

namespace Compilation.Parser.IOstructs {
    struct Token {
        public string type, 
            content;
        public uint line, 
            column;
    }

    struct Input {
        public string session_id;
        public Token[] tokens;
    }

    class TreeRoot {
        public TreeRoot(TreeNode[] main, Procedure[] functions) {
            this.main = main;
            this.functions = functions;
        }

        public TreeNode[] main;
        public Procedure[] functions;
    }

    

    struct Output {
        public bool success;
        public string errorDesc;
        public uint errorLine, 
            errorColumn;

        public VarDefConstable[] variables;
        public TreeRoot syntaxTree;
    }
}

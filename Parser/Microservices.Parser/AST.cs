
namespace Compilation.Parser.AST {
    struct VarDef {
        public VarDef(string name, string type) {
            this.name = name;
            this.type = type;
        }
        public string name,
            type;
    }
    struct VarDefConstable {
        public VarDefConstable(string name, string type, bool constValue) {
            this.name = name;
            this.type = type;
            this.constValue = constValue;
        }
        public string name,
            type;
        public bool constValue;
    }

    abstract class TreeNode {
        public TreeNode(string type) {
            this.type = type;
        }
        public string type;
    }

    abstract class Operator : TreeNode {
        public Operator(string @operator) : base("operator") {
            this.@operator = @operator;
        }
        public string @operator;
    }

    abstract class Binary : Operator {
        public Binary(string @operator, TreeNode operandLeft, TreeNode operandRight) : base(@operator) {
            this.operandLeft = operandLeft;
            this.operandRight = operandRight;
        }
        public TreeNode operandLeft,
            operandRight;
    }
    abstract class Unary : Operator {
        public Unary(string @operator, TreeNode operandRight) : base(@operator) {
            this.operandRight = operandRight;
        }
        public TreeNode operandRight;
    }

    namespace ArithmeticOperators {
        class UMinus : Unary {
            public UMinus(TreeNode b) : base("u_minus", b) { }
        }
        class Plus : Binary {
            public Plus(TreeNode a, TreeNode b) : base("plus", a, b) { }
        }
        class Minus : Binary {
            public Minus(TreeNode a, TreeNode b) : base("minus", a, b) { }
        }
        class Multiply : Binary {
            public Multiply(TreeNode a, TreeNode b) : base("multiply", a, b) { }
        }
        class Divide : Binary {
            public Divide(TreeNode a, TreeNode b) : base("divide", a, b) { }
        }
        class Div : Binary {
            public Div(TreeNode a, TreeNode b) : base("div", a, b) { }
        }
        class Mod : Binary {
            public Mod(TreeNode a, TreeNode b) : base("mod", a, b) { }
        }
    }

    namespace LogicOperators {
        class Not : Unary {
            public Not(TreeNode b) : base("not", b) { }
        }
        class And : Binary {
            public And(TreeNode a, TreeNode b) : base("and", a, b) { }
        }
        class Or : Binary {
            public Or(TreeNode a, TreeNode b) : base("or", a, b) { }
        }
        class Less : Binary {
            public Less(TreeNode a, TreeNode b) : base("less", a, b) { }
        }
        class More : Binary {
            public More(TreeNode a, TreeNode b) : base("more", a, b) { }
        }
        class Equal : Binary {
            public Equal(TreeNode a, TreeNode b) : base("equal", a, b) { }
        }
        class LessEqual : Binary {
            public LessEqual(TreeNode a, TreeNode b) : base("less-equal", a, b) { }
        }
        class MoreEqual : Binary {
            public MoreEqual(TreeNode a, TreeNode b) : base("more-equal", a, b) { }
        }
        class NotEqual : Binary {
            public NotEqual(TreeNode a, TreeNode b) : base("non-equal", a, b) { }
        }
    }


    namespace DataTypes {
        class Integer : TreeNode {
            public Integer(int number) : base("number") {
                this.number = number;
            }
            public int number;
        }

        class String : TreeNode {
            public String(string @string) : base("string") {
                this.@string = @string;
            }
            public string @string;
        }
    }
    

    class Call : TreeNode {
        public Call(string function, TreeNode[] arguments) : base("call") {
            this.function = function;
            this.arguments = arguments;
        }
        public string function;
        public TreeNode[] arguments;
    }

    class Exit : Call {
        public Exit() : base("exit", new TreeNode[] { new DataTypes.Integer(0) }) { }
    }

    class Variable : TreeNode {
        public Variable(string name) : base("variable") {
            this.name = name;
        }
        public string name;
    }

    class Goto : TreeNode {
        public Goto(string identifer) : base("goto") {
            this.identifer = identifer;
        }
        public string identifer;
    }

    class Marker : TreeNode {
        public Marker(string identifer) : base("marker") {
            this.identifer = identifer;
        }
        public string identifer;
    }

    abstract class Loop : TreeNode {
        public Loop(string loop) : base("loop") {
            this.loop = loop;
        }
        public string loop;
    }

    class While : Loop {
        public While(TreeNode[] body, TreeNode condition) : base("while") {
            this.body = body;
            this.condition = condition;
        }
        public TreeNode[] body;
        public TreeNode condition;
    }

    class For : Loop {
        public For(TreeNode[] body, TreeNode condition, TreeNode stepmaker) : base("for") {
            this.body = body;
            this.condition = condition;
            this.stepmaker = stepmaker;
        }
        public TreeNode[] body;
        public TreeNode condition;
        public TreeNode stepmaker;
    }


    class Function {
        public Function(string name, VarDef[] arguments, VarDef @return, VarDefConstable[] variables, TreeNode[] body) {
            this.name = name;
            this.arguments = arguments;
            this.@return = @return;
            this.variables = variables;
            this.body = body;
        }
        public string name;
        public VarDef[] arguments;
        public VarDef @return;
        public VarDefConstable[] variables;
        public TreeNode[] body;
    }
}

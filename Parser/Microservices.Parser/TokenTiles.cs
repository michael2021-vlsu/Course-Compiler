using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace Compilation.Parser {

    static class TokenTiles {

        public enum Meaning { //"_" - means that the token is used mainly in the service space of the program
            ProgNameDef_,
            BeginSection_,
            EndSection_,
            VarDef_,
            EndProgram_,
            DataType_,
            Const_,
            VarNamesList_,
            EndPhrase,
            Exit,
            ParamList,
            ParamList_Reference,
            ArgumentsList,
            Variable,
            Assign,
            ArithmEquation, 
            LogicEquation,
            EquationGroupBegin,
            EquationGroupEnd,
            FunctionName
        }

        //([a-zA-Z_]\w*)|([\d+*\-\/]+)|(\((?:[a-zA-Z_]\w*|[\d+*\-\/]|((?3)))+\))
        public static readonly Dictionary<string, IEnumerable<Meaning>> staticmean = new(new KeyValuePair<string, IEnumerable<Meaning>>[] {
            new("program", new[] { Meaning.ProgNameDef_ }),
            new("begin", new[] { Meaning.BeginSection_ }),
            new("end", new[] { Meaning.EndSection_ }),
            
            new("colon", new[] { Meaning.VarDef_, Meaning.ParamList }),
            new("dot", new[] { Meaning.EndProgram_ }), // + Meaning.ArrayIndexesSplitter
            new("datatype", new[] { Meaning.DataType_ }), //integer, real
            new("const", new[] { Meaning.Const_ }),
            new("var", new[] { Meaning.VarDef_, Meaning.ParamList_Reference }),
            new("comma", new[] { Meaning.VarNamesList_, Meaning.ArgumentsList, Meaning.ParamList }),

            new("semicolon", new[] { Meaning.EndPhrase }),
            new("exit", new[] { Meaning.Exit }),
            new("assign", new [] { Meaning.Assign }),
            new("variable", new [] { Meaning.Variable, Meaning.FunctionName }),
            new("left parenthesis", new[] { Meaning.FunctionName, Meaning.EquationGroupBegin }),
            new("right parenthesis", new[] { Meaning.FunctionName, Meaning.EquationGroupEnd }),

            new("arithmetic operator", new[] { Meaning.ArithmEquation, Meaning.LogicEquation }), //Like 12+19-48/45 or 12+1 != 14
            new("logic operator", new [] { Meaning.LogicEquation, Meaning.ArithmEquation }),
            new("comparsion operator", new [] { Meaning.LogicEquation, Meaning.ArithmEquation })
        });
    }
}

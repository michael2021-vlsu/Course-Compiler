import MicroServerAPI
from LibAsm import FuncAsm

ProcCodGen = MicroServerAPI.MicroService(url_get='http://localhost:8080/5-semestr/compiler/get-job',
									 url_post='http://localhost:8080/5-semestr/compiler/post-job',
									 persistentMode=True)
A = FuncAsm()

while True:
	data,addr = ProcCodGen.GetNextJob(job_type='Compilation.CodeGenerator')

	ProcTree=data['syntaxTree']
	ProcTree=ProcTree['procedures']
	A.ProcTree=ProcTree
	for LocVar in data['variables']:
		A.ProcVariable(A.CodeVariable, LocVar, A.Variables)
	A.ProcProcedure(A.CodeProcedure, ProcTree)
	A.CodeProcedure = A.CodeProcedure + A.WriteLn
	ProcTree=data['syntaxTree']
	A.ProcBody(A.CodeMain, ProcTree['main'], None)
	A.Variables.append(A.EndVar)
	A.CodeSeg.append(A.NameProgramm)
	A.CodeSeg = A.CodeSeg + A.CodeVariable + A.CodeMain + A.CodeEnd
	A.Code = A.StartProgr + A.Variables + A.CodeProcedure + A.CodeSeg
	data = A.Code

	ProcCodGen.PostFinalResult(content=data,
							   result_type='Compilation.CodeGenerator.Result',
							   responseAddress=addr)
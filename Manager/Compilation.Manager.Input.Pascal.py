import MicroServerAPI

serv = MicroServerAPI.MicroService(url_get='http://localhost:8080/5-semestr/compiler/get-job',
                                   url_post='http://localhost:8080/5-semestr/compiler/post-job',
                                   persistentMode=True)

while True:
    codePascal,addr = serv.GetNextJob(job_type='Compilation.Manager.Input.Pascal')
    #Begin of data processing area
    
    listOfTokens = serv.ProcessAsFunction(content=codePascal,
                           requested_function='Compilation.Lexer')

    abstractSyntaxTree = serv.ProcessAsFunction(content=listOfTokens,
                           requested_function='Compilation.Parser')

    codeAsm = serv.ProcessAsFunction(content=abstractSyntaxTree,
                           requested_function='Compilation.CodeGenerator')
    
    #End of data processing area
    serv.PostFinalResult(content=codeAsm,
                         result_type='Compilation.Manager.Output',
                         responseAddress=addr)

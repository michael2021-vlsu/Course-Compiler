import MicroServerAPI
import random
import string

serv = MicroServerAPI.MicroService(url_get='http://localhost:8080/5-semestr/compiler/get-job',
                                   url_post='http://localhost:8080/5-semestr/compiler/post-job',
                                   persistentMode=True)

while True:
    codePascal,addr = serv.GetNextJob(job_type='Compilation.Manager.Input.Pascal')
    #Begin of data processing area

    session = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase + string.digits, k = 16))
    
    serv.ProcessAsFunction(content={"session":session,"bank":None,"operation":"post","data":"Manager's Mandat: Create Session"},
                           requested_function='Compilation.Storage.Request')

    serv.ProcessAsFunction(content={"session":session,"bank":"source_raw","operation":"post","data":codePascal},
                           requested_function='Compilation.Storage.Request')
    
    listOfTokens = serv.ProcessAsFunction(content={"session":session,"source":codePascal},
                           requested_function='Compilation.Lexer')
    
    #Lower is not ready now, wait for some... If it is very necessary, tell Michael.
    abstractSyntaxTree = serv.ProcessAsFunction(content=listOfTokens,
                           requested_function='Compilation.Parser')

    codeAsm = serv.ProcessAsFunction(content=abstractSyntaxTree,
                           requested_function='Compilation.CodeGenerator')

    serv.ProcessAsFunction(content={"session":session,"bank":None,"operation":"post","data":"Manager's Mandat: Remove Session"},
                           requested_function='Compilation.Storage.Request')
    
    #End of data processing area
    serv.PostFinalResult(content=codeAsm,
                         result_type='Compilation.Manager.Output',
                         responseAddress=addr)

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

    result = { "success":False, "lines":[] }

    if "success" in listOfTokens:
        if listOfTokens["success"]:
            abstractSyntaxTree = serv.ProcessAsFunction(content={"session":session,"tokens":listOfTokens["tokens"]},
                                   requested_function='Compilation.Parser')

            if "success" in abstractSyntaxTree:
                if abstractSyntaxTree["success"]:
                    codeAsm = serv.ProcessAsFunction(content={"session":session,"variables":abstractSyntaxTree["variables"],"syntax tree":abstractSyntaxTree["syntax tree"]},
                                   requested_function='Compilation.CodeGenerator')

                    if "success" in codeAsm:
                        if codeAsm["success"]:
                            result["success"] = True
                            result["lines"] = codeAsm["asm code"]
                        else:
                            first = None
                            if "error desc" in codeAsm:
                                first = ": Генератор кода: " + codeAsm["error desc"]
                            else:
                                first = ": Генератор кода: Описание ошибки отсутствует."
                            
                            result["lines"] = [ first ]
                    else:
                        result["lines"] = ["Сервис генератора кода неисправен!"]
                else:
                    first = None
                    if "error desc" in abstractSyntaxTree:
                        first = ": Парсер: " + abstractSyntaxTree["error desc"]
                    else:
                        first = ": Парсер: Описание ошибки отсутствует."
                    
                    if "error line" in abstractSyntaxTree:
                        if "error column" in abstractSyntaxTree:
                            first = "; символ: " + abstractSyntaxTree["error column"] + first
                        first = "Строка " + abstractSyntaxTree["error line"] + first

                        result["lines"] = [ first, codePascal[abstractSyntaxTree["error line"]] ]
                    else:
                        result["lines"] = [ first ]
            else:
                result["lines"] = ["Сервис парсера неисправен!"]
        else:
            first = None
            if "error desc" in listOfTokens:
                first = ": Лексер: " + listOfTokens["error desc"]
            else:
                first = ": Лексер: Описание ошибки отсутствует."
            
            if "error line" in listOfTokens:
                if "error column" in listOfTokens:
                    first = "; символ: " + listOfTokens["error column"] + first
                first = "Строка " + listOfTokens["error line"] + first

                result["lines"] = [ first, codePascal[listOfTokens["error line"]] ]
            else:
                result["lines"] = [ first ]
    else:
        result["lines"] = ["Сервис лексера неисправен!"]

    serv.ProcessAsFunction(content={"session":session,"bank":None,"operation":"post","data":"Manager's Mandat: Remove Session"},
                           requested_function='Compilation.Storage.Request')
    
    #End of data processing area
    serv.PostFinalResult(content=result,
                         result_type='Compilation.Manager.Output',
                         responseAddress=addr)

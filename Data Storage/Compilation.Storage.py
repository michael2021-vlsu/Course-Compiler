import MicroServerAPI

serv = MicroServerAPI.MicroService(url_get='http://localhost:8080/5-semestr/compiler/get-job',
                                   url_post='http://localhost:8080/5-semestr/compiler/post-job',
                                   persistentMode=True)

storage = {}

while True:
    data,addr = serv.GetNextJob(job_type='Compilation.Storage.Request')
    #Begin of data processing area

    if 'session' in data and 'bank' in data and 'operation' in data:
        if data['operation'] == 'post':
            if 'data' in data:
                if data['data'] == "Manager's Mandat: Create Session":
                    storage[data['session']] = {}
                    data = { 'success':True }
                elif data['data'] == "Manager's Mandat: Remove Session":
                    del storage[data['session']]
                    data = { 'success':True }
                else:
                    if data['session'] in storage and data['bank'] not in storage['session']:
                        storage['session']['bank'] = data['data']
                        data = { 'success':True }
                    else:
                        data = { 'success':False }
            else:
                data = { 'success':False }
        else:
            if data['session'] in storage and data['bank'] in storage['session']:
                data = { 'success':True, 'data':storage['session']['bank'] }
            else:
                data = { 'success':False }
    else:
        data = { 'success':False }
    
    #End of data processing area
    serv.PostFinalResult(content=data,
                         result_type='Compilation.Storage.Answer',
                         responseAddress=addr)

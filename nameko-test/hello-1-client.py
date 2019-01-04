res = []
for i in range(20):
    hello_res = n.rpc.greeting_service.hello.call_async(name=str(i))
    res.append(hello_res)

for hello_res in res:
    print(hello_res.result())

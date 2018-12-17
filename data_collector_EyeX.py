#!/usr/bin/env python3.5
import asyncio
import os

#60 seconds recording... top left, top right, bottom left, botton right, every 1 second

dataList = [];

class SubprocessProtocol(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1: # got stdout data (bytes)
            print(data)
            dataList.append(data)

    def connection_lost(self, exc):
        loop.stop() # end loop.run_forever()

if os.name == 'nt':
    loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(loop.subprocess_exec(SubprocessProtocol, 
        r"C:\Users\Niteesh\source\repos\ConsoleApp1\ConsoleApp1\bin\Debug\ConsoleApp1.exe"))
    loop.run_forever()
finally:
    loop.close()
    f = open(r"C:\Users\Niteesh\Desktop\data_test.txt",'w')
    for i in dataList:
        f.writelines(i.decode("utf-8")[:-1])
    f.close()

#!/usr/bin/env python3.5
import asyncio
import os
from display_dot_EyeX import display_dot_EyeX
import msvcrt

dataList = [];

class SubprocessProtocol(asyncio.SubprocessProtocol):
    def pipe_data_received(self, fd, data):
        if fd == 1: # got stdout data (bytes)
            print(data.decode("utf-8")[:-2])
            dataList.append(data)
            dd.display_coord(data.decode("utf-8")[:-2])  
            # if msvcrt.kbhit():
                # print ("key hit")
                # if msvcrt.getch().decode == chr(27):
                    # print("key press detected",key)
#                    dd.quit_pg()
#                    loop.stop()
#                    loop.close()
#            print ("check",check)
#            if (check == False) :
#                print("time to stop")

    def connection_lost(self, exc):
        loop.stop() # end loop.run_forever()

        
dd = display_dot_EyeX(60)        
if os.name == 'nt':
    loop = asyncio.ProactorEventLoop() # for subprocess' pipes on Windows
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(loop.subprocess_exec(SubprocessProtocol, 
        r"D:\University\Sem 3\HCI lab\Code\eyeX_tracker\eyeX_tracker\bin\Debug\eyeX_tracker.exe"))
    loop.run_forever()
except Exception as e:
    print("in except : ",e)
finally:
    print("in finally")
    print("loop running : ",loop.is_running())
    if(loop.is_running()):
        print("loop is running")
        loop.stop()
    print("loop running : ",loop.is_running())
    print(loop.is_closed())
    loop.close()
    print(loop.is_closed())
    # f = open(r"D:\University\data_test.txt",'w')
    # for i in dataList:
        # f.writelines(i.decode("utf-8")[:-1])
    # f.close()
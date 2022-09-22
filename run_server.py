#runserver.py
from waitress import serve
from mysite import settings 
from mysite.wsgi import application
import os, time, random
import signal
import sys 

from multiprocessing import Pool, Process, freeze_support
import multiprocessing 

def run_server(host:str, port:int):
    serve(application, host=host, port=port)
    #exit(0)

def initializer():
    """Ignore SIGINT in child workers."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def run_server_multi(host:str, port_start:int, port_end:int):
    print( "=" * 40 )
    print('Server process id : %s.' % os.getpid())
    
    print( "=" * 40 )
    print("[INFO]Create worker-process.")
    worker_processes  = ( port_end - port_start  + 1 )
    print( "[INFO]Workers:{} / host : {} / Port Range : {}~{}".format(worker_processes, host, port_start, port_end) )
    
    original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)
    mpPool = Pool(processes=worker_processes) #initializer=initializer)
    signal.signal(signal.SIGINT, original_sigint_handler)
    try:
        #args = [(host, port,) for port in range(port_start, port_end)]
        #print ( args )
        #mpPool.map_async(run_server, args)
        for port in range(port_start, port_end+1):
           print("Add to Pool. {}:{}".format(host, port) )
           mpPool.apply_async(run_server, args=(host, port,))
           
        print( "=" * 40 )
        print('[INFO]Worker-process running')
        print('[INFO]Server Start')
        mpPool.close()    
        mpPool.join()    
    except KeyboardInterrupt:
        print ("[INFO] Riase CTRL+C 'KeyboardInterrupt', terminating workers")
        print("finally.")
        mpPool.terminate()
        print("mpPool.terminate().")
        mpPool.join()
        print("mpPool.join().")
        #sys.exit()
    #finally:

        

def main():
    host        = settings.U_HOST
    port_start  = settings.U_PORT_RANGE[0]
    port_end    = settings.U_PORT_RANGE[1]
    
    print(f"BASE_DIR={settings.BASE_DIR}")
    print(f"STATICFILES_DIRS={settings.STATICFILES_DIRS}")
    print(f"MEDIA_ROOT={settings.MEDIA_ROOT}")
    print(f"STATIC_ROOT={settings.STATIC_ROOT}")
    
    
    run_server_multi(host, port_start, port_end)
    
if __name__ == '__main__':
    freeze_support()
    main()
    #print("Starting server...")
    #serve(application, host='localhost', port='8000')
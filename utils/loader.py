import time

class Loader:
    status = 0
    prev_message = None

    def __init__(obj,status):
        obj.status = status

    def log(obj, status, message):
        time.sleep(1)
        
        obj.status = status
        loader = '[' + '#'*obj.status + '-'*(20-obj.status) + '] ' + str(obj.status*5) + '%'
        
        if obj.prev_message != None:
            print("\x1b[1A\x1b[2K", end="")
        
        if message != "":
            print(message)
        if status != 20:
            print(f"{loader}")
        else:
            print("\nCompleted successfully!")
        
        obj.prev_message = message

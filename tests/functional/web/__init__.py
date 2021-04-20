import multiprocessing
import platform

# Initialize test context for flask apps

if platform.system() == 'Darwin':
    # https://stackoverflow.com/questions/64305197/getting-a-cant-pickle-local-
    # object-liveservertestcase-error-when-trying-torm.system() == 'Darwin':
    multiprocessing.set_start_method("fork")

global_flask_port_tracker = 8000

def get_new_flask_port() -> int:
    global global_flask_port_tracker
    global_flask_port_tracker += 1
    return global_flask_port_tracker

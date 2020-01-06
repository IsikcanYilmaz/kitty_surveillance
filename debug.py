
import time

DEBUG_PRINT_ENABLE = True
DEBUG_MODULE_SERVER = 0
DEBUG_MODULE_MOTORS = 1

DEBUG_MODULES = {
        DEBUG_MODULE_SERVER : True,
        DEBUG_MODULE_MOTORS : False
    }

DEBUG_MODULE_STRINGS = {
        DEBUG_MODULE_SERVER : "SER",
        DEBUG_MODULE_MOTORS : "PWM"
    }

def debugPrint(string, module=0, level=0):
    if DEBUG_PRINT_ENABLE and DEBUG_MODULES[module]:
        print("[%s] %s" % (DEBUG_MODULE_STRINGS[module], string))

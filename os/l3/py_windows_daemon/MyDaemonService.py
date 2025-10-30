import time
import win32serviceutil
import win32service
import win32event
import servicemanager

SERVICE_NAME = "MyDaemonPython"
SERVICE_DISPLAY_NAME = "My Python Daemon"

class MyPythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = SERVICE_NAME
    _svc_display_name_ = SERVICE_DISPLAY_NAME

    def __init__(self, args):
        super().__init__(args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.running = True

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.running = False
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogInfoMsg("Служба запущена")
        while self.running:
            time.sleep(10)
            # Do periodic work here
        servicemanager.LogInfoMsg("Служба зупиняється")

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyPythonService)

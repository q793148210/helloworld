
"""Windows service wrapper for the messaging daemon."""

import threading
import win32serviceutil
import win32service
import win32event
import servicemanager


from daemon import run_daemon


class WeChatDaemonService(win32serviceutil.ServiceFramework):

    _svc_name_ = "WeChatDaemon"
    _svc_display_name_ = "WeChat Quantum Messaging Daemon"

    def __init__(self, args):
        super().__init__(args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)
        self.thread = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)
        if self.thread:
            self.thread.join()

    def SvcDoRun(self):
        self.thread = threading.Thread(target=run_daemon, args=(self.stop_event,))
        self.thread.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ""))
        win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)


if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(WeChatDaemonService)

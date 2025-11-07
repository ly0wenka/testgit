#include <windows.h>
#include <tchar.h>
#include <iostream>

SERVICE_STATUS ServiceStatus = {0};
SERVICE_STATUS_HANDLE hStatus = nullptr;
HANDLE stopEvent = nullptr;

void WriteLog(const char* msg) {
    FILE* log;
    fopen_s(&log, "C:\\Temp\\SimpleService.log", "a+");
    if (log) {
        fprintf(log, "%s\n", msg);
        fclose(log);
    }
}

void WINAPI ServiceCtrlHandler(DWORD request) {
    switch (request) {
        case SERVICE_CONTROL_STOP:
        case SERVICE_CONTROL_SHUTDOWN:
            ServiceStatus.dwCurrentState = SERVICE_STOP_PENDING;
            SetServiceStatus(hStatus, &ServiceStatus);
            SetEvent(stopEvent);
            return;
        default:
            break;
    }
    SetServiceStatus(hStatus, &ServiceStatus);
}

void WINAPI ServiceMain(DWORD argc, LPTSTR* argv) {
    ServiceStatus.dwServiceType = SERVICE_WIN32;
    ServiceStatus.dwCurrentState = SERVICE_START_PENDING;
    ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP | SERVICE_ACCEPT_SHUTDOWN;
    hStatus = RegisterServiceCtrlHandler(_T("SimpleService"), (LPHANDLER_FUNCTION)ServiceCtrlHandler);

    if (!hStatus) return;

    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    SetServiceStatus(hStatus, &ServiceStatus);

    WriteLog("Service started.");
    stopEvent = CreateEvent(NULL, TRUE, FALSE, NULL);

    while (WaitForSingleObject(stopEvent, 3000) == WAIT_TIMEOUT) {
        WriteLog("Service running...");
    }

    WriteLog("Service stopping...");
    ServiceStatus.dwCurrentState = SERVICE_STOPPED;
    SetServiceStatus(hStatus, &ServiceStatus);
}

int _tmain(int argc, TCHAR* argv[]) {
    SERVICE_TABLE_ENTRY ServiceTable[] = {
        { _T("SimpleService"), (LPSERVICE_MAIN_FUNCTION)ServiceMain },
        { NULL, NULL }
    };
    StartServiceCtrlDispatcher(ServiceTable);
    return 0;
}

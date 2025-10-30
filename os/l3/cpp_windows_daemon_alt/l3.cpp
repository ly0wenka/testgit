#define UNICODE
#define _UNICODE

#include <windows.h>
#include <string>
#include <thread>
#include <chrono>

const std::wstring SERVICE_NAME = L"MyDaemonCppService";

SERVICE_STATUS ServiceStatus = { 0 };
SERVICE_STATUS_HANDLE hStatus = NULL;
bool running = true;

void WriteEventLog(const std::wstring& message)
{
    HANDLE hEventLog = RegisterEventSource(NULL, SERVICE_NAME.c_str());
    if (hEventLog)
    {
        const wchar_t* msg = message.c_str();
        ReportEvent(hEventLog, EVENTLOG_INFORMATION_TYPE, 0, 0, NULL, 1, 0, &msg, NULL);
        DeregisterEventSource(hEventLog);
    }
}

void WINAPI ServiceCtrlHandler(DWORD ctrlCode)
{
    switch (ctrlCode)
    {
    case SERVICE_CONTROL_STOP:
        ServiceStatus.dwCurrentState = SERVICE_STOP_PENDING;
        SetServiceStatus(hStatus, &ServiceStatus);

        running = false; // stop main loop
        WriteEventLog(L"Служба отримала команду завершення.");
        ServiceStatus.dwCurrentState = SERVICE_STOPPED;
        SetServiceStatus(hStatus, &ServiceStatus);
        break;

    default:
        break;
    }
}

void WINAPI ServiceMain(DWORD argc, LPWSTR* argv)
{
    hStatus = RegisterServiceCtrlHandler(SERVICE_NAME.c_str(), ServiceCtrlHandler);
    if (!hStatus) return;

    ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    ServiceStatus.dwCurrentState = SERVICE_START_PENDING;
    SetServiceStatus(hStatus, &ServiceStatus);

    WriteEventLog(L"Служба запущена.");

    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    SetServiceStatus(hStatus, &ServiceStatus);

    // Main service loop
    while (running)
    {
        std::this_thread::sleep_for(std::chrono::seconds(10));
        // Add your periodic work here
    }

    WriteEventLog(L"Служба завершила роботу.");
    ServiceStatus.dwCurrentState = SERVICE_STOPPED;
    SetServiceStatus(hStatus, &ServiceStatus);
}

int wmain()
{
    SERVICE_TABLE_ENTRY ServiceTable[] =
    {
        { (LPWSTR)SERVICE_NAME.c_str(), (LPSERVICE_MAIN_FUNCTION)ServiceMain },
        { NULL, NULL }
    };

    if (!StartServiceCtrlDispatcher(ServiceTable))
    {
        // If run manually (not as service), just show info
        WriteEventLog(L"Служба запущена у консольному режимі.");
        ServiceMain(0, NULL);
    }

    return 0;
}

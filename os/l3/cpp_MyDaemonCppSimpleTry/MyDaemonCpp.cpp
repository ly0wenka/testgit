#define UNICODE
#define _UNICODE

#include <windows.h>
#include <string>
#include <thread>
#include <chrono>

const std::wstring SERVICE_NAME = L"MyDaemonCpp";

SERVICE_STATUS ServiceStatus = {};
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
        ServiceStatus.dwCheckPoint = 1;
        SetServiceStatus(hStatus, &ServiceStatus);

        running = false;
        WriteEventLog(L"Служба отримала команду завершення.");

        ServiceStatus.dwCurrentState = SERVICE_STOPPED;
        ServiceStatus.dwCheckPoint = 0;
        SetServiceStatus(hStatus, &ServiceStatus);
        break;

    default:
        break;
    }
}

void WINAPI ServiceMain(DWORD argc, LPWSTR* argv)
{
    hStatus = RegisterServiceCtrlHandler(SERVICE_NAME.c_str(), ServiceCtrlHandler);
    if (!hStatus)
        return;

    // Початкові параметри
    ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP;
    ServiceStatus.dwCurrentState = SERVICE_START_PENDING;
    ServiceStatus.dwWin32ExitCode = 0;
    ServiceStatus.dwServiceSpecificExitCode = 0;
    ServiceStatus.dwCheckPoint = 0;
    ServiceStatus.dwWaitHint = 5000;
    SetServiceStatus(hStatus, &ServiceStatus);

    // Ініціалізація
    // std::this_thread::sleep_for(std::chrono::seconds(1));
    WriteEventLog(L"Служба запущена.");

    // Готова до роботи
    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    ServiceStatus.dwWaitHint = 0;
    ServiceStatus.dwCheckPoint = 0;
    SetServiceStatus(hStatus, &ServiceStatus);

    // Основний цикл
    // while (running)
    // {
    //     std::this_thread::sleep_for(std::chrono::seconds(10));
    //     WriteEventLog(L"Служба працює...");
    // }
    WriteEventLog(L"Служба працює...");
    
    ServiceStatus.dwCurrentState = SERVICE_STOPPED;
    ServiceStatus.dwCheckPoint = 0;
    SetServiceStatus(hStatus, &ServiceStatus);
}

#ifdef _MSC_VER
int wmain()
#else
int WINAPI WinMain(HINSTANCE, HINSTANCE, LPSTR, int)
#endif
{
    SERVICE_TABLE_ENTRY ServiceTable[] =
    {
        { (LPWSTR)SERVICE_NAME.c_str(), (LPSERVICE_MAIN_FUNCTION)ServiceMain },
        { NULL, NULL }
    };

    if (!StartServiceCtrlDispatcher(ServiceTable))
    {
        // Якщо запущено не як службу — просто вивести повідомлення
        MessageBox(NULL, L"Цю програму потрібно запускати як службу через SC.", SERVICE_NAME.c_str(), MB_OK | MB_ICONINFORMATION);
    }

    return 0;
}

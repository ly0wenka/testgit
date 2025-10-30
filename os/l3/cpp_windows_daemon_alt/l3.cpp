#define UNICODE
#define _UNICODE

#include <windows.h>
#include <string>
#include <thread>
#include <chrono>
#include <csignal>
#include <iostream>

const std::wstring SERVICE_NAME = L"MyDaemonCpp";
bool running = true;

void SignalHandler(int signal)
{
    if (signal == SIGINT || signal == SIGTERM)
    {
        running = false;
        HANDLE hEventLog = RegisterEventSource(NULL, SERVICE_NAME.c_str());
        if (hEventLog)
        {
            const wchar_t* message = L"Демон завершив роботу через сигнал.";
            ReportEvent(hEventLog, EVENTLOG_INFORMATION_TYPE, 0, 0, NULL, 1, 0, &message, NULL);
            DeregisterEventSource(hEventLog);
        }
    }
}

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

int wmain()
{
    std::signal(SIGINT, SignalHandler);
    std::signal(SIGTERM, SignalHandler);

    WriteEventLog(L"Демон запущений.");

    while (running)
    {
        std::this_thread::sleep_for(std::chrono::seconds(10));
    }

    WriteEventLog(L"Демон завершив роботу.");
    return 0;
}

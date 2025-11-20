#include <windows.h>
#include <iostream>
#include <signal.h>
#include <fstream>

SERVICE_STATUS ServiceStatus;
SERVICE_STATUS_HANDLE hStatus;

void logMessage(const std::string& message) {
    std::ofstream logFile("S:\\Users\\L\\Downloads\\New folder(175)\\testgit\\os\\l3\\cpp_windows_daemon\\x64\\Debug\\daemon_log.txt", std::ios::app);
    logFile << message << std::endl;
}

void signalHandler(int signal) {
    if (signal == SIGINT) {
        logMessage("SIGINT received. Shutting down daemon.");
        exit(0);
    }
    else if (signal == SIGTERM) {  // Replacing SIGUSR1 with SIGTERM
        logMessage("SIGTERM received. Logging signal.");
    }
}

void ServiceMain(int argc, char** argv) {
    ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    ServiceStatus.dwCurrentState = SERVICE_RUNNING;
    ServiceStatus.dwControlsAccepted = SERVICE_ACCEPT_STOP;
    hStatus = RegisterServiceCtrlHandler(L"MyDaemon", [](DWORD control) {
        if (control == SERVICE_CONTROL_STOP) {
            ServiceStatus.dwCurrentState = SERVICE_STOPPED;
            SetServiceStatus(hStatus, &ServiceStatus);
            logMessage("Service stopped.");
            exit(0);
        }
        });

    SetServiceStatus(hStatus, &ServiceStatus);
    logMessage("Service started.");

    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);  // Handling SIGTERM instead of SIGUSR1

    while (true) {
        Sleep(1000);
    }
}

void installService() {
    SC_HANDLE schSCManager = OpenSCManager(NULL, NULL, SC_MANAGER_CREATE_SERVICE);
    if (!schSCManager) return;
    SC_HANDLE schService = CreateService(
        schSCManager, L"MyDaemon", L"MyDaemon",  // Using wide-character strings
        SERVICE_ALL_ACCESS, SERVICE_WIN32_OWN_PROCESS,
        SERVICE_AUTO_START, SERVICE_ERROR_NORMAL,
        L"S:\\Users\\L\\Downloads\\New folder(175)\\testgit\\os\\l3\\cpp_windows_daemon\\x64\\Debug\\cpp_windows_daemon.exe", NULL, NULL, NULL, NULL, NULL);  // Using wide-character strings
    CloseServiceHandle(schService);
    CloseServiceHandle(schSCManager);
}

int main(int argc, char* argv[]) {
    if (argc > 1 && std::string(argv[1]) == "install") {
        installService();
        return 0;
    }
    SERVICE_TABLE_ENTRY ServiceTable[] = {
        {LPWSTR(L"MyDaemon"), (LPSERVICE_MAIN_FUNCTION)ServiceMain},  // Using wide-character string
        {NULL, NULL}
    };
    StartServiceCtrlDispatcher(ServiceTable);
    return 0;
}

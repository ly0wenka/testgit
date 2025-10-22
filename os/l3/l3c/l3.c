#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <syslog.h>
#include <sys/types.h>
#include <sys/stat.h>

void signal_handler(int sig) {
    if (sig == SIGUSR1) {
        syslog(LOG_INFO, "Received SIGUSR1 signal");
    } else if (sig == SIGINT) {
        syslog(LOG_INFO, "Received SIGINT signal, terminating");
        closelog();
        exit(0);
    }
}

void daemonize() {
    pid_t pid = fork();
    if (pid < 0) {
        perror("Fork failed");
        exit(EXIT_FAILURE);
    }
    if (pid > 0) {
        exit(EXIT_SUCCESS);
    }

    umask(0);
    pid_t sid = setsid();
    if (sid < 0) {
        perror("setsid failed");
        exit(EXIT_FAILURE);
    }

    if ((chdir("/")) < 0) {
        perror("chdir failed");
        exit(EXIT_FAILURE);
    }

    close(STDIN_FILENO);
    close(STDOUT_FILENO);
    close(STDERR_FILENO);
}

int main() {
    printf("Starting daemon...\n");
    daemonize();
    openlog("linux_daemon", LOG_PID, LOG_DAEMON);
    syslog(LOG_INFO, "Daemon started");

    signal(SIGUSR1, signal_handler);
    signal(SIGINT, signal_handler);
    
    while (1) {
        pause();
    }
    return 0;
}
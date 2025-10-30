import time
import win32evtlogutil
import win32evtlog
import win32event
import win32api
import win32con
import sys

SERVICE_NAME = "MyDaemonPython"

def write_event(message, event_type=win32evtlog.EVENTLOG_INFORMATION_TYPE):
    """
    Write a message to the Windows Event Log under the custom source.
    """
    try:
        # Create source if it doesn't exist
        if not win32evtlogutil.QuerySourceInfo(SERVICE_NAME):
            win32evtlogutil.AddSourceToRegistry(SERVICE_NAME, "Application")

        # Write the event
        win32evtlogutil.ReportEvent(SERVICE_NAME, eventID=1, eventCategory=0,
                                    eventType=event_type, strings=[message])
    except Exception as e:
        print(f"Failed to write to Event Log: {e}")

def run_daemon():
    write_event("Демон запущений.", win32evtlog.EVENTLOG_INFORMATION_TYPE)
    
    try:
        while True:
            time.sleep(10)  # Wait 10 seconds
            # Here you can add more logic to handle tasks/events
    except KeyboardInterrupt:
        write_event("Демон завершив роботу через сигнал.", win32evtlog.EVENTLOG_INFORMATION_TYPE)
        sys.exit(0)

if __name__ == "__main__":
    run_daemon()

#include <windows.h>
#include <shellapi.h>
#include <string>
#include <fstream>
#include <ctime>

#pragma comment(lib, "user32.lib")
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "shell32.lib")

#define WM_TRAY (WM_USER + 1)
#define ID_TRAY 1

HWND hWnd;
NOTIFYICONDATA nid{};

HHOOK hKeyHook = nullptr;
HHOOK hMouseHook = nullptr;

// =====================
// Helpers
// =====================
std::wstring Now()
{
    wchar_t buf[64];
    time_t t = time(nullptr);
    tm tm{};
    localtime_s(&tm, &t);
    wcsftime(buf, 64, L"%Y-%m-%d %H:%M:%S", &tm);
    return buf;
}

std::wstring ActiveWindow()
{
    wchar_t title[256];
    HWND hwnd = GetForegroundWindow();
    GetWindowText(hwnd, title, 256);
    return title;
}

// =====================
// Clipboard
// =====================
void SetClipboard(const std::wstring& text)
{
    if (!OpenClipboard(nullptr)) return;
    EmptyClipboard();

    size_t bytes = (text.size() + 1) * sizeof(wchar_t);
    HGLOBAL hMem = GlobalAlloc(GMEM_MOVEABLE, bytes);
    if (!hMem) { CloseClipboard(); return; }

    wchar_t* ptr = (wchar_t*)GlobalLock(hMem);
    if (!ptr) { GlobalFree(hMem); CloseClipboard(); return; }

    wcscpy_s(ptr, text.size() + 1, text.c_str());
    GlobalUnlock(hMem);
    SetClipboardData(CF_UNICODETEXT, hMem);
    CloseClipboard();
}

std::wstring GetClipboard()
{
    if (!OpenClipboard(nullptr)) return L"";
    HANDLE h = GetClipboardData(CF_UNICODETEXT);
    if (!h) { CloseClipboard(); return L""; }

    wchar_t* p = (wchar_t*)GlobalLock(h);
    std::wstring s = p ? p : L"";
    GlobalUnlock(h);
    CloseClipboard();
    return s;
}

// =====================
// Keyboard hook
// =====================
LRESULT CALLBACK KeyProc(int code, WPARAM wp, LPARAM lp)
{
    if (code == HC_ACTION && wp == WM_KEYDOWN)
    {
        auto* k = (KBDLLHOOKSTRUCT*)lp;
        std::wofstream f("key_log.txt", std::ios::app);
        f << Now() << L" | VK=" << k->vkCode
            << L" | " << ActiveWindow() << L"\n";
    }
    return CallNextHookEx(hKeyHook, code, wp, lp);
}

// =====================
// Mouse hook
// =====================
LRESULT CALLBACK MouseProc(int code, WPARAM wp, LPARAM lp)
{
    if (code == HC_ACTION)
    {
        auto* m = (MSLLHOOKSTRUCT*)lp;
        std::wofstream f("mouse_log.txt", std::ios::app);
        f << Now() << L" | " << wp
            << L" (" << m->pt.x << L"," << m->pt.y << L") "
            << ActiveWindow() << L"\n";
    }
    return CallNextHookEx(hMouseHook, code, wp, lp);
}

// =====================
// Tray menu
// =====================
void TrayMenu()
{
    HMENU menu = CreatePopupMenu();
    AppendMenu(menu, MF_STRING, 1, L"Clean clipboard");
    AppendMenu(menu, MF_STRING, 2, L"Clear clipboard");
    AppendMenu(menu, MF_STRING, 3, L"Uppercase");
    AppendMenu(menu, MF_STRING, 4, L"Lowercase");
    AppendMenu(menu, MF_SEPARATOR, 0, nullptr);
    AppendMenu(menu, MF_STRING, 5, L"Start keylogger");
    AppendMenu(menu, MF_STRING, 6, L"Stop keylogger");
    AppendMenu(menu, MF_STRING, 7, L"Start mouse logger");
    AppendMenu(menu, MF_STRING, 8, L"Stop mouse logger");
    AppendMenu(menu, MF_SEPARATOR, 0, nullptr);
    AppendMenu(menu, MF_STRING, 9, L"Exit");

    POINT p;
    GetCursorPos(&p);
    SetForegroundWindow(hWnd);
    int cmd = TrackPopupMenu(menu, TPM_RETURNCMD, p.x, p.y, 0, hWnd, nullptr);

    if (cmd == 1) SetClipboard(GetClipboard());
    if (cmd == 2) SetClipboard(L"");
    if (cmd == 3) {
        auto s = GetClipboard();
        for (auto& c : s) c = towupper(c);
        SetClipboard(s);
    }
    if (cmd == 4) {
        auto s = GetClipboard();
        for (auto& c : s) c = towlower(c);
        SetClipboard(s);
    }
    if (cmd == 5 && !hKeyHook)
        hKeyHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyProc, nullptr, 0);
    if (cmd == 6 && hKeyHook)
        UnhookWindowsHookEx(hKeyHook), hKeyHook = nullptr;
    if (cmd == 7 && !hMouseHook)
        hMouseHook = SetWindowsHookEx(WH_MOUSE_LL, MouseProc, nullptr, 0);
    if (cmd == 8 && hMouseHook)
        UnhookWindowsHookEx(hMouseHook), hMouseHook = nullptr;
    if (cmd == 9)
        PostQuitMessage(0);
}

// =====================
// Window proc
// =====================
LRESULT CALLBACK WndProc(HWND hwnd, UINT msg, WPARAM wp, LPARAM lp)
{
    if (msg == WM_TRAY && lp == WM_RBUTTONUP)
        TrayMenu();

    if (msg == WM_DESTROY)
        PostQuitMessage(0);

    return DefWindowProc(hwnd, msg, wp, lp);
}

// =====================
// ENTRY POINT
// =====================
int wmain()
{
    HINSTANCE hInst = GetModuleHandle(nullptr);

    WNDCLASS wc{};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInst;
    wc.lpszClassName = L"TrayApp";
    RegisterClass(&wc);

    hWnd = CreateWindow(
        wc.lpszClassName, L"",
        WS_OVERLAPPEDWINDOW,
        0, 0, 0, 0,
        nullptr, nullptr,
        hInst, nullptr
    );

    nid.cbSize = sizeof(nid);
    nid.hWnd = hWnd;
    nid.uID = ID_TRAY;
    nid.uFlags = NIF_MESSAGE | NIF_ICON | NIF_TIP;
    nid.uCallbackMessage = WM_TRAY;
    nid.hIcon = LoadIcon(nullptr, IDI_APPLICATION);
    wcscpy_s(nid.szTip, L"Clipboard + Logger");
    Shell_NotifyIcon(NIM_ADD, &nid);

    MSG msg;
    while (GetMessage(&msg, nullptr, 0, 0))
        DispatchMessage(&msg);

    Shell_NotifyIcon(NIM_DELETE, &nid);
    return 0;
}

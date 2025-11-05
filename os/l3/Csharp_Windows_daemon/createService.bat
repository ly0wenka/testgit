sc create MyDaemonCsharp binPath= "S:\Users\L\Downloads\New folder (175)\testgit\os\l3\Csharp_Windows_daemon\MyDaemonService.exe" start= auto
chcp 65001 >nul
sc description MyDaemonCsharp "C# демон для запису подій у Windows Event Log"
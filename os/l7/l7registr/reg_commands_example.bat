@echo off
echo =========================
echo REG COMMANDS EXAMPLES
echo =========================

:: ------------------------
:: 1) QUERY - переглянути ключ
echo 1) REG QUERY
reg query "HKCU\Environment"
echo.

:: ------------------------
:: 2) ADD - додати нову змінну
echo 2) REG ADD
reg add "HKCU\Environment" /v MyVar /t REG_SZ /d HelloWorld /f
reg query "HKCU\Environment" /v MyVar
echo.

:: ------------------------
:: 3) DELETE - видалити змінну
echo 3) REG DELETE
reg delete "HKCU\Environment" /v MyVar /f
echo.

:: ------------------------
:: 4) COPY - скопіювати ключ
echo 4) REG COPY
reg add "HKCU\TestKey1" /v Value1 /t REG_SZ /d "Test1" /f
reg copy "HKCU\TestKey1" "HKCU\TestKey2" /s /f
reg query "HKCU\TestKey2"
echo.

:: ------------------------
:: 5) SAVE - зберегти ключ у файл
echo 5) REG SAVE
reg save "HKCU\TestKey1" "%temp%\TestKey1.hiv"
echo Saved to %temp%\TestKey1.hiv
echo.

:: ------------------------
:: 6) RESTORE - відновити ключ із файлу
echo 6) REG RESTORE
reg restore "HKCU\TestKey1_Restore" "%temp%\TestKey1.hiv"
reg query "HKCU\TestKey1_Restore"
echo.

:: ------------------------
:: 7) LOAD - завантажити Hive
echo 7) REG LOAD
reg load HKCU\TempHive "%temp%\TestKey1.hiv"
reg query "HKCU\TempHive"
echo.

:: ------------------------
:: 8) UNLOAD - відвантажити Hive
echo 8) REG UNLOAD
reg unload HKCU\TempHive
echo.

:: ------------------------
:: 9) COMPARE - порівняти два ключі
echo 9) REG COMPARE
reg compare "HKCU\TestKey1" "HKCU\TestKey2" /v Value1
echo.

:: ------------------------
:: 10) EXPORT - експортувати ключ у .reg файл
echo 10) REG EXPORT
reg export "HKCU\TestKey1" "%temp%\TestKey1.reg" /y
echo Exported to %temp%\TestKey1.reg
echo.

:: ------------------------
:: 11) IMPORT - імпортувати з .reg файлу
echo 11) REG IMPORT
reg import "%temp%\TestKey1.reg"
reg query "HKCU\TestKey1"
echo.

echo =========================
echo DONE
pause

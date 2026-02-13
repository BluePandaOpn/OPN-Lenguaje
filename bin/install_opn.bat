@echo off
setlocal EnableExtensions EnableDelayedExpansion
title OPN BluePanda Installer

echo ==========================================
echo   OPN BluePanda - Global Installer
echo ==========================================
echo.

set "SCRIPT_DIR=%~dp0"
set "INSTALL_ROOT=%USERPROFILE%\.opn"
set "BIN_DIR=%INSTALL_ROOT%\bin"
set "VENV_DIR=%INSTALL_ROOT%\.venv"
set "REQ_FILE=%SCRIPT_DIR%requirements_opn.txt"
set "OPN_EXE_SOURCE=%SCRIPT_DIR%opn.exe"
set "OPN_EXE_TARGET=%BIN_DIR%\opn.exe"

if not exist "%OPN_EXE_SOURCE%" (
    echo [ERROR] opn.exe was not found in:
    echo         %OPN_EXE_SOURCE%
    echo [HINT] Put this installer next to opn.exe and run again.
    echo.
    pause
    exit /b 1
)

if not exist "%INSTALL_ROOT%" mkdir "%INSTALL_ROOT%"
if not exist "%BIN_DIR%" mkdir "%BIN_DIR%"

echo [INFO] Installing opn.exe into %BIN_DIR%
copy /Y "%OPN_EXE_SOURCE%" "%OPN_EXE_TARGET%" >nul
if errorlevel 1 (
    echo [ERROR] Could not copy opn.exe to %BIN_DIR%
    pause
    exit /b 1
)

echo [INFO] Ensuring PATH contains %BIN_DIR%
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$path=[Environment]::GetEnvironmentVariable('Path','User');" ^
  "$target='%BIN_DIR%';" ^
  "if([string]::IsNullOrWhiteSpace($path)){$path=''};" ^
  "$parts=$path -split ';' | Where-Object { $_ -and $_.Trim() -ne '' };" ^
  "if($parts -notcontains $target){$newPath=($parts + $target) -join ';'; [Environment]::SetEnvironmentVariable('Path',$newPath,'User'); Write-Host '  -> PATH updated';}" ^
  "else{Write-Host '  -> PATH already configured';}"

set "PYTHON_CMD="
where py >nul 2>&1
if %errorlevel%==0 (
    set "PYTHON_CMD=py -3"
) else (
    where python >nul 2>&1
    if %errorlevel%==0 set "PYTHON_CMD=python"
)

if not defined PYTHON_CMD (
    echo [WARN] Python was not found. Skipping global venv setup.
    echo [INFO] opn command was installed, but build helpers were not prepared.
    echo [HINT] Install Python 3.10+ and rerun this installer to complete setup.
    echo.
    echo [DONE] Installation finished with warnings.
    pause
    exit /b 0
)

if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo [INFO] Creating OPN global venv: %VENV_DIR%
    call %PYTHON_CMD% -m venv "%VENV_DIR%"
    if errorlevel 1 (
        echo [ERROR] Failed to create venv at %VENV_DIR%
        echo [HINT] Verify Python installation includes venv/ensurepip.
        pause
        exit /b 1
    )
) else (
    echo [INFO] Reusing existing venv: %VENV_DIR%
)

set "VENV_PY=%VENV_DIR%\Scripts\python.exe"
echo [INFO] Updating pip toolchain in global venv...
call "%VENV_PY%" -m ensurepip --upgrade >nul 2>&1
call "%VENV_PY%" -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo [ERROR] Could not initialize pip in global venv.
    echo [HINT] Check network or Python permissions and rerun installer.
    pause
    exit /b 1
)

if exist "%REQ_FILE%" (
    echo [INFO] Installing OPN global dependencies from requirements_opn.txt...
    call "%VENV_PY%" -m pip install -r "%REQ_FILE%"
    if errorlevel 1 (
        echo [WARN] Some optional global dependencies could not be installed.
        echo [HINT] You can run manually:
        echo       "%VENV_PY%" -m pip install -r "%REQ_FILE%"
    )
) else (
    echo [INFO] requirements_opn.txt not found. Skipping optional global deps.
)

echo.
echo [DONE] OPN BluePanda installed successfully.
echo        Restart your terminal and run: opn --version
echo        Global runtime folder: %INSTALL_ROOT%
echo.
pause
exit /b 0

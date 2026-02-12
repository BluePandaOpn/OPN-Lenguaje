@echo off
setlocal
title Instalador de OPN

echo ==========================================
echo      Instalacion de OPN CLI Global
echo ==========================================
echo.

:: 1. Verificar si opn.exe existe en la carpeta del script
if not exist "%~dp0opn.exe" (
    echo [ERROR] No se encontro 'opn.exe'.
    echo Asegurate de tener el ejecutable en la misma carpeta que este script.
    echo.
    pause
    exit /b 1
)

:: 2. Crear directorio de instalacion en el perfil de usuario
set "INSTALL_DIR=%USERPROFILE%\.opn\bin"
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

:: 3. Copiar opn.exe
echo [INFO] Copiando opn.exe a %INSTALL_DIR%...
copy /Y "%~dp0opn.exe" "%INSTALL_DIR%\opn.exe" >nul

:: 4. Agregar al PATH del usuario usando PowerShell (evita duplicados y truncamiento)
echo [INFO] Configurando variables de entorno...
powershell -Command "$p=[Environment]::GetEnvironmentVariable('Path','User'); $t='%INSTALL_DIR%'; if(-not ($p.Split(';') -contains $t)) { [Environment]::SetEnvironmentVariable('Path', $p+';'+$t, 'User'); Write-Host 'Ruta agregada al PATH.' } else { Write-Host 'La ruta ya existe en el PATH.' }"

echo.
echo [EXITO] Instalacion completada. Reinicia tu terminal para usar el comando 'opn'.
pause
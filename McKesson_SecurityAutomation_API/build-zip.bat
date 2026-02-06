@echo off
REM Backend ZIP Build Script for Azure App Service
REM Creates a deployment ZIP for Azure App Service (Linux)

echo ========================================
echo Building FastAPI Backend ZIP for Azure
echo ========================================
echo.

REM Clean up old dist folder if it exists
if exist dist (
    echo Cleaning old dist folder...
    rmdir /s /q dist
)

REM Create dist folder
echo Creating dist folder...
mkdir dist

REM Copy all necessary files
echo Copying Python files...
copy *.py dist\
copy requirements.txt dist\
copy .deployment dist\
copy startup.txt dist\
copy .env.production dist\

REM Create ZIP file
echo.
echo Creating backend-deploy.zip...
cd dist
powershell -Command "Compress-Archive -Path * -DestinationPath ..\backend-deploy.zip -Force"
cd ..

echo.
echo ========================================
echo Build Complete!
echo ========================================
echo.
echo ZIP file created: backend-deploy.zip
echo.
echo To deploy to Azure:
echo az webapp deployment source config-zip --resource-group hsps-demo-rg --name mckessondemo-backend --src backend-deploy.zip
echo.
echo Target: https://mckessondemo-backend.azurewebsites.net
echo.

pause

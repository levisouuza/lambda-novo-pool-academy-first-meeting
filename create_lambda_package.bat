rmdir /s /q lambda_package
del lambda.zip
mkdir lambda_package
pip install -r ./src/requirements.txt --target lambda_package
xcopy src lambda_package /E /I
powershell -command "Compress-Archive -Path lambda_package\* -DestinationPath lambda.zip -Force"

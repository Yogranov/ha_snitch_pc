If the run.ps1 powershell does not work, you probebly have to change the execution policy. To do this, follow the steps below:
1. open powershell as administrator
2. paste and run the following
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned

To make it run automatically, you can add it to the startup folder. To do this, follow the steps below:
1. open the run window (windows key + r)
2. paste and run the following
    shell:startup
3. copy a shortcut to run.bat file to the startup folder

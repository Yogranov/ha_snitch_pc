cd ..
powershell Stop-process -name ha_snitch_pc -Force
powershell Start-Process "ha_snitch_pc.exe" -WindowStyle Hidden
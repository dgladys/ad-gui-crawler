# Write-Host "$PSScriptRoot\script.sh"
cd $PSScriptRoot
.venv/Scripts/activate
python script.py
# & 'C:\Program Files\Git\bin\bash.exe' "$PSScriptRoot\script.sh"
# Recalculate an .xlsx in desktop Excel (via COM) so formula values are cached for openpyxl/pandas.
# Usage: powershell -NoProfile -File recalc_excel.ps1 <full path to .xlsx>
param([Parameter(Mandatory = $true)][string]$Path)

$full = (Resolve-Path $Path).Path
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $wb = $excel.Workbooks.Open($full)
    $excel.CalculateFull()
    $wb.Save()
    $wb.Close($false)
    Write-Output "recalculated: $full"
}
finally {
    $excel.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($excel) | Out-Null
}

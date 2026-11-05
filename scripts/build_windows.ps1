param([string]$Version = '0.2.1')
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonExe)) { throw 'Create .venv and install requirements-build.txt first.' }
& $pythonExe -m PyInstaller --noconfirm --clean --onefile --windowed --name TouchFlow --add-data 'companion/phone.html:.' --add-data 'companion/gestures.js:.' companion/touchflow.py
if ($LASTEXITCODE -ne 0) { throw 'PyInstaller build failed.' }
$packageName = "TouchFlow-$Version-windows-x64"
$buildId = [guid]::NewGuid().ToString("N")
$stagePath = Join-Path $projectRoot "release-staging\$buildId\$packageName"
New-Item -ItemType Directory -Force -Path $stagePath | Out-Null
Copy-Item -LiteralPath 'dist\TouchFlow.exe' -Destination $stagePath
foreach ($file in @('README.md','LICENSE','PRIVACY.md','SECURITY.md','THIRD_PARTY_NOTICES.md','CHANGELOG.md','SUPPORT.md','CONTRIBUTING.md','CODE_OF_CONDUCT.md')) { Copy-Item -LiteralPath $file -Destination $stagePath }
Copy-Item -LiteralPath 'docs' -Destination $stagePath -Recurse -Force
New-Item -ItemType Directory -Force -Path (Join-Path $stagePath 'companion') | Out-Null
Copy-Item -LiteralPath 'companion\README.md' -Destination (Join-Path $stagePath 'companion')
$licenseDir = Join-Path $stagePath 'licenses'
New-Item -ItemType Directory -Force -Path $licenseDir | Out-Null
$pythonBase = & $pythonExe -c 'import sys; print(sys.base_prefix)'
Copy-Item -LiteralPath (Join-Path $pythonBase 'LICENSE.txt') -Destination (Join-Path $licenseDir 'Python-LICENSE.txt')
Copy-Item -LiteralPath (Join-Path $pythonBase 'tcl\tk8.6\license.terms') -Destination (Join-Path $licenseDir 'Tk-license.terms')
Get-ChildItem -LiteralPath 'licenses' -File | Copy-Item -Destination $licenseDir
$pyiLicense = & $pythonExe -c 'import importlib.metadata; d=importlib.metadata.distribution("pyinstaller"); print(next(d.locate_file(f) for f in d.files if str(f).endswith("COPYING.txt")))'
Copy-Item -LiteralPath $pyiLicense -Destination (Join-Path $licenseDir 'PyInstaller-COPYING.txt')
foreach ($dependency in @('qrcode','colorama')) {
    $dependencyLicense = & $pythonExe -c "import importlib.metadata; d=importlib.metadata.distribution('$dependency'); print(next(d.locate_file(f) for f in d.files if 'LICENSE' in str(f).upper() or str(f).upper().endswith('LICENCE')))"
    if ($LASTEXITCODE -ne 0) { throw "Missing license for $dependency" }
    Copy-Item -LiteralPath $dependencyLicense -Destination (Join-Path $licenseDir "$dependency-LICENSE.txt")
}
$zipPath = Join-Path $projectRoot "dist\$packageName.zip"
Compress-Archive -Path $stagePath -DestinationPath $zipPath -Force
$hash = (Get-FileHash -LiteralPath $zipPath -Algorithm SHA256).Hash.ToLowerInvariant()
Set-Content -LiteralPath 'dist\SHA256SUMS.txt' -Value "$hash  $packageName.zip" -Encoding ASCII
Write-Output $zipPath

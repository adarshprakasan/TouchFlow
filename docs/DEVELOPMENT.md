# Development and Windows builds

## Source setup

Use Windows x64 and Python 3.12 with Tk support. Clone the repository and run `python companion/touchflow.py`. The source runtime needs no packages.

## Checks

Run `python -m unittest discover -s tests -v`. Tests import the companion without starting its GUI, mock the input path and bind HTTP fixtures only to loopback. No test emits desktop input.

Run `python companion/touchflow.py --self-test smoke.json` to check the input structure, bundled phone page and Tk initialization without starting remote control. The JSON output reports success; delete it after review.

## Package

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\scriptsuild_windows.ps1
```

If local PowerShell policy prevents script execution, follow your organization's policy or run the documented PyInstaller build command manually; do not weaken machine-wide protections. The script builds a single-file windowed executable, bundles the phone page, and creates `dist/TouchFlow-0.1.0-windows-x64.zip` with documentation and third-party licenses. `dist/SHA256SUMS.txt` hashes the ZIP. Build tools are not runtime dependencies.

The executable is unsigned. Releases must disclose that fact. Build on Windows x64; cross-platform builds are not provided. Packaged code uses paths relative to `__file__`, which PyInstaller maps into its extracted bundle.

## Release validation

Use the release checklist. Passing syntax, protocol and packaged self-tests does not prove end-to-end phone or multi-device compatibility. Record actual manual coverage without overstating it.

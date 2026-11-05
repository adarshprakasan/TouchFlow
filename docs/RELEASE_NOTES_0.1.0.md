# TouchFlow 0.1.0 alpha

First public Windows x64 development release.

## Download

Download **TouchFlow-0.1.0-windows-x64.zip**, extract it and run **TouchFlow.exe**. Python is bundled; no installer or Python installation is required. The ZIP includes setup instructions, documentation and third-party license notices. SHA256SUMS.txt contains the archive checksum.

Connect your phone to the same trusted private Wi-Fi, open the address shown on the PC, enter the code and approve the phone on Windows.

## Included

- Phone browser trackpad, click, drag, two-finger scroll and text input.
- Special keys and adjustable pointer speed.
- Desktop approval, pause, disconnect and inactivity timeout.
- MIT-licensed source and reproducible build instructions with pinned build dependencies.

## Validation performed

- Seven automated validation and loopback protocol tests passed on Windows 11 x64 with Python 3.12.
- Portable executable self-test passed: bundled phone resource, 64-bit Windows input structure, command validation and Tk initialization.
- Phone JavaScript syntax checked.
- No test emitted live mouse or keyboard input.

## Known limitations

- The executable is unsigned and may show a Windows reputation warning.
- Local HTTP is unencrypted: use trusted private Wi-Fi only and avoid sensitive text. Do not expose port 8765 to the internet.
- Supports one phone at a time. Windows elevated applications and security screens are inaccessible.
- Broad real-phone and Windows-version compatibility testing remains pending; this is an alpha prerelease, not a stable release.
- No automatic updater, cloud relay, remote screen view or unattended access.

Report problems in Issues without including codes, tokens or private input. Report vulnerabilities privately through the Security tab.

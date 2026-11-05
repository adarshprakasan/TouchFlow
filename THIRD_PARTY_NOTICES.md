# Third-party notices

TouchFlow source is MIT licensed. A portable Windows build includes the Python runtime, Tcl/Tk, OpenSSL, zlib and the PyInstaller bootloader. Each component retains its own copyright and license. Their license files are copied into the release's `licenses/` directory by the packaging script.

- Python: Python Software Foundation License and accompanying notices; https://docs.python.org/3/license.html
- Tcl/Tk: upstream Tcl/Tk license terms in the bundled files; https://www.tcl-lang.org/software/tcltk/license.html
- PyInstaller bootloader: GPL with the PyInstaller distribution exception; https://pyinstaller.org/en/stable/license.html

The standalone root visual prototype loads DM Sans, DM Mono and Manrope through Google Fonts. These are distributed by their respective authors under the SIL Open Font License; fonts are fetched remotely and are not bundled in the working phone controller or executable. See https://fonts.google.com/attribution and the relevant font family pages for their current notices.

Build dependencies may carry additional licenses. They are used to produce the executable and are not all included as application runtime components. No claim of endorsement by any upstream project is made.

OpenSSL and zlib runtime license texts are also included in `licenses/`. CPython distribution notices cover additional incorporated components, including libffi.

Version 0.2.0 includes qrcode 8.2 (BSD license) for QR generation and its Windows dependency colorama 0.4.6 (BSD license). Their upstream license texts are included with the source under `licenses/` and in each portable release. No QR generation service is contacted.

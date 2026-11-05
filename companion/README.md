# Windows companion

Double-click `Start TouchFlow.cmd` in the TouchFlow folder. Python 3.12 or newer with Tk support is required; no packages are needed.

1. Keep your phone and computer on the same trusted private Wi-Fi network.
2. Open an address displayed in the companion window in your phone browser.
3. Enter the 8-character code and approve the phone request on the computer.
4. Use the trackpad, click controls, drag toggle, two-finger scroll, text box and special keys. Click the destination app on your computer before sending text.
5. Use Pause input or Disconnect phone in the desktop window whenever needed. Closing the window stops the service.

The connection uses plain HTTP, so input is not encrypted. Use only a trusted private network. This development version does not provide TLS, QR pairing, an installer, automatic updates, or internet access. Do not forward port 8765. A VPN or Wi-Fi client isolation may prevent connectivity. If Windows asks about firewall access, allow it only for your private network; no firewall settings are changed automatically.

Pairing codes expire after 2 minutes. Pending approval expires after 60 seconds; inactive connections expire after 8 seconds. Only one phone is supported. The code is never placed in the URL. Sessions use random tokens, same-origin checks, sequence checks and payload limits. Held drag buttons are released on pause, disconnect and timeout.

Input uses the Windows SendInput API. Windows blocks injection into elevated apps and secure desktop screens. Run TouchFlow as an ordinary user. Text is sent as Unicode; target application support can vary. No input is stored or logged. The original index.html remains a separate visual demo; open the address displayed by the companion for real controls.

Implementation checks: Python compilation and input-structure sizing can be checked without emitting keyboard or mouse events. End-to-end behavior must be checked using a real phone on the local network.

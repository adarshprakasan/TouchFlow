# TouchFlow

Use your phone as a wireless trackpad, keyboard, and gesture controller for a Windows PC. TouchFlow is a standalone project.

## Run on Windows

Requires Python 3.12 or newer with Tkinter. No additional packages are required.

1. Download or clone this repository.
2. Double-click **Start TouchFlow.cmd**.
3. Keep your phone and PC on the same trusted private Wi-Fi network.
4. Open the address displayed by the companion in your phone browser.
5. Enter the pairing code and approve the request on your PC.

The companion supports pointer movement, left/right click, drag, two-finger scrolling, Unicode text, and common special keys. Pause, disconnect, or close the companion to stop control.

## Development status

This is an early development build. The companion serves its phone interface from `companion/phone.html`. The root `index.html` is a separate visual prototype and does not connect to the companion.

The local connection uses unencrypted HTTP. Use a trusted private network only. No cloud service, account, or input logging is used. Windows administrator apps and security screens cannot be controlled. Phone-to-PC operation still requires real-device validation.

See [companion instructions](companion/README.md) for setup and limitations, and [feasibility plan](docs/FEASIBILITY.md) for the planned validation work.

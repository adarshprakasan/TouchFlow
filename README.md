# TouchFlow

[![Release](https://img.shields.io/github/v/release/adarshprakasan/TouchFlow?include_prereleases)](https://github.com/adarshprakasan/TouchFlow/releases)
[![License MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20x64-0078D4)](docs/GETTING_STARTED.md)

Use your phone as a wireless trackpad and keyboard for your Windows PC. Open the phone controls in a browser, pair locally, and control the active desktop application.

**Status: v0.1.0 alpha.** TouchFlow is an independent project by [Adarsh Prakasan](https://github.com/adarshprakasan). It is intended for trusted private networks and early feedback. Broad device compatibility and phone-to-PC operation have not yet been validated across a device matrix.

## Download and run

1. Go to **[Releases](https://github.com/adarshprakasan/TouchFlow/releases)** and download `TouchFlow-0.1.0-windows-x64.zip` from the alpha release assets.
2. Extract the ZIP into a folder on your Windows PC.
3. Run **TouchFlow.exe**. The portable build includes Python; you do not need to install it.
4. Connect your phone and PC to the same trusted private Wi-Fi network.
5. Enter an address shown in the companion window into your phone browser, including `http://` and `:8765`.
6. Enter the pairing code and approve your phone on the PC.

Keep the companion window open. Close it to stop the service. The executable is **unsigned**; Windows may show a reputation or publisher warning. Review the source and checksums and make your own trust decision. There is no installer or automatic updater.

**The connection uses unencrypted HTTP. Do not use public/shared Wi-Fi, forward port 8765, or send passwords or other sensitive text.** Pairing does not protect against someone who can intercept traffic on the network. See [Security](SECURITY.md).

## Controls

| Control | Action |
| --- | --- |
| Slide one finger | Move the pointer |
| Tap the pad / Left click | Left click |
| Right click | Open the context menu |
| Drag on, then slide | Hold the left button for dragging; tap Drag off to release |
| Slide two fingers vertically | Scroll |
| Pointer speed | Adjust movement sensitivity |
| Type and Send text | Send text to the active PC application |
| Special keys | Enter, Backspace, Tab, Escape and arrow keys |
| Desktop Pause / Disconnect | Stop input or revoke the phone session |

## Requirements and limitations

- Portable download: Windows 10 or 11 on x64. Other platforms are not supported in this release.
- Phone: a modern browser with JavaScript, touch/pointer events and Fetch support. iOS Safari and Android Chrome are intended targets; real-device coverage is pending.
- One phone and one PC on a reachable local network. Guest Wi-Fi isolation, VPNs or firewall rules may block the connection.
- Cannot control administrator applications, UAC dialogs, login/lock screens or the Windows security desktop.
- Backgrounding or locking the phone can suspend the connection. Return to the page and pair again if needed.
- No remote screen view, clipboard sync, file transfer, cloud relay, account or unattended access.

## Documentation

- [Getting started](docs/GETTING_STARTED.md) and [troubleshooting](docs/TROUBLESHOOTING.md)
- [Architecture and protocol](docs/ARCHITECTURE.md)
- [Build from source](docs/DEVELOPMENT.md) and [contributing](CONTRIBUTING.md)
- [Security policy](SECURITY.md), [privacy](PRIVACY.md) and [support](SUPPORT.md)
- [Changelog](CHANGELOG.md), [roadmap](docs/ROADMAP.md) and [release checks](docs/RELEASE_CHECKLIST.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## Run from source

Install Python 3.12 with Tk support on Windows, download the source ZIP and extract it, then double-click `Start TouchFlow.cmd`. No runtime packages are required. Developers can instead run `python companion/touchflow.py` from a clone.

The root `index.html` is a visual prototype only. The working phone controller is served by the Windows companion from `companion/phone.html`.

## License and feedback

TouchFlow source is licensed under the [MIT License](LICENSE). Bundled components retain their own licenses. Report reproducible problems in [Issues](https://github.com/adarshprakasan/TouchFlow/issues); follow the security policy for vulnerabilities.

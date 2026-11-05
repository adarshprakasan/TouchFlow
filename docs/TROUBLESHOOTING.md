# Troubleshooting

| Symptom | What to check |
| --- | --- |
| The phone page does not load | Keep the companion open; use the address currently displayed; include `http://` and `:8765`; put both devices on the same Wi-Fi. |
| Several PC addresses appear | Choose the real Wi-Fi adapter address. Ignore virtual-machine and VPN adapters. |
| Same Wi-Fi but no connection | Guest/client isolation or a firewall may block direct device connections. Use a trusted private network that allows local devices. Do not disable the firewall globally. |
| Windows firewall prompt | Allow only the private network if you trust the program and network. The app cannot change this permission for you. |
| Port already in use / app cannot start | Close other TouchFlow companion windows. Another program may be using port 8765. |
| Incorrect or expired code | Click New pairing code on the PC and enter the new eight-character code. |
| Too many pairing attempts | Wait one minute before trying again. |
| Another phone is connected | Disconnect phone on the PC, generate a new code and pair again. |
| Phone locks or network briefly drops | Return to the same open tab. It retries automatically; the approved session does not expire. Reloaded/closed tabs require desktop Disconnect and pairing again. |
| QR opens the wrong address | Choose the actual Wi-Fi adapter in the companion dropdown and scan its updated QR. Do not use a VM/VPN address. |
| Text selected in the mobile pad | Install 0.2.0 or newer, reopen the phone link and ensure you are using the companion-served controller. Tap then tap-and-hold to drag. Text fields remain selectable. |
| Tab/window does not drag | Move the PC pointer over its tab/title bar, tap then tap again within 350 ms, hold and move, then lift. Or use Drag on/off. |
| Pointer does not move | Resume input on the PC; check connection state; the app cannot control elevated programs or security screens. |
| Text goes to the wrong place | Text targets the active PC window and its focused field. Select the intended field before tapping Send text. |
| Text behaves differently in a specific app | Unicode input support depends on the destination app. Report the app name and a non-sensitive example. |
| Source launcher flashes or says Python not found | Install Python 3.12+ with Tk support and run `py -3 -m pip install -r requirements.txt`, or use the portable Windows release. |
| Executable warning | The alpha build is unsigned. Review the release and checksum; do not bypass security controls you do not understand. |

For bug reports, include Windows version, TouchFlow version, phone OS/browser, steps and a non-sensitive error message. Never include pairing codes, session tokens, private typed text or screenshots containing them.

If Windows blocks a button release (for example on a secure desktop), 0.2.1 keeps the release pending and retries after access returns. The desktop and phone report paused input while recovery is pending. Do not run TouchFlow as administrator to work around this restriction. An approval dialog left open beyond one minute now expires even if you later click Approve; request a new pairing.

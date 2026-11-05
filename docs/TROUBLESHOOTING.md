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
| Phone is disconnected after locking | Mobile browsers can suspend network work. Return to the page and pair again. |
| Pointer does not move | Resume input on the PC; check connection state; the app cannot control elevated programs or security screens. |
| Text goes to the wrong place | Text targets the active PC window and its focused field. Select the intended field before tapping Send text. |
| Text behaves differently in a specific app | Unicode input support depends on the destination app. Report the app name and a non-sensitive example. |
| Source launcher flashes or says Python not found | Install Python 3.12+ with Tk support or use the portable Windows release. |
| Executable warning | The alpha build is unsigned. Review the release and checksum; do not bypass security controls you do not understand. |

For bug reports, include Windows version, TouchFlow version, phone OS/browser, steps and a non-sensitive error message. Never include pairing codes, session tokens, private typed text or screenshots containing them.

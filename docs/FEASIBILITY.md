# TouchFlow feasibility spike

## Question

Can a phone browser send authenticated low-latency input to a desktop companion on a trusted local network, and can that companion reliably emit pointer and keyboard input on the first supported operating system?

## Boundaries

- The phone may use a browser as its client.
- A browser-only desktop demo may control only content inside that page.
- System-wide mouse and keyboard behavior needs a desktop companion with explicit local approval and a visible pause/quit control.
- No cloud relay, account, analytics, clipboard, or unattended access is in scope for the spike.

## Questions to answer

1. Which desktop operating system should TouchFlow support first?
2. Can a phone reach a local companion endpoint on common home and office Wi-Fi networks?
3. What OS permissions and signing requirements apply to pointer and keyboard input?
4. Does a WebSocket transport provide reliable pairing and acceptable interaction latency?
5. What behavior occurs when the phone locks, backgrounds the page, changes networks, or loses connectivity?

## Experiment plan

1. Confirm phone-to-computer reachability with both devices on the same Wi-Fi network.
2. Exchange a short-lived pairing code and require approval on the computer.
3. Send pointer deltas and text to the companion; measure visible response and recovery after disconnect.
4. Test release-all behavior so no button or modifier remains held after failure.
5. Record supported phone/browser/desktop combinations and limitations before choosing production framework and packaging.

## Exit criteria

- One phone pairs to one desktop in under one minute on the supported network.
- Approved pointer motion, click, scroll, and text entry work in at least two ordinary desktop applications.
- Rejected, expired, disconnected, and malformed sessions do not emit input.
- The user can pause and revoke the phone from the desktop.
- The supported OS and its required permissions are documented.

# Changelog

## 0.2.1 alpha — 2026-11-05

- Retry blocked mouse-button releases while keeping the input loop alive and preventing new input until release succeeds.
- Recheck approval expiry after the desktop dialog returns and enforce pending-request expiry in HTTP handlers.
- Include effective pause state in heartbeat responses and preserve the paused phone status until resumed.
- Reject extremely large movement/scroll integers without overflowing numeric validation.
- Add focused regressions for all four review findings, including failure recovery and request-handler survival.


## 0.2.0 alpha — 2026-11-05

- Added locally rendered QR codes and a network-address selector; scanning opens the phone controller.
- Added double-tap-and-hold dragging with movement delivered before mouse-button release.
- Prevented selection, touch callouts and native drag behavior inside the mobile pad, including Safari-specific handling.
- Removed the established-session inactivity expiry; temporary network failures now retry with the same authorization and discard stale input.
- Kept short-lived setup codes/approvals and a held-button safety release without expiring connected sessions.
- Added QR, idle-session, gesture, selection-handler and recovery regression tests.
- Updated portable packaging, runtime licenses, setup instructions and protocol/security documentation.


## 0.1.0 alpha — 2026-11-05

- Windows companion with phone browser controls on a local network.
- Pointer movement, clicks, drag toggle, two-finger scroll, text and special keys.
- Short-lived pairing codes, desktop approval, session timeout, pause and disconnect.
- Portable Windows x64 packaging, checksums and build instructions.
- Setup, troubleshooting, architecture, privacy, security and contribution documentation.
- MIT source license and third-party notices.

Known limitations: unencrypted HTTP on trusted networks only; unsigned executable; one phone per PC; no administrator/security-screen control; broad real-device validation pending.

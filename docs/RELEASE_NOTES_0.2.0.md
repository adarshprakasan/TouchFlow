# TouchFlow 0.2.0 alpha

QR connection links, reliable mobile dragging and sessions without an inactivity limit.

## Download and update

Download **TouchFlow-0.2.0-windows-x64.zip**, close the running older companion, extract the new ZIP and run **TouchFlow.exe**. Python is bundled. Reopen the phone controls from the new QR code, then pair again. Do not use the root visual-prototype page for remote control.

## Changes

1. **QR code:** scan the code in the Windows companion with your phone camera to open the local controller. The network-address dropdown updates the QR and visible URL. The QR is generated locally and contains no pairing secret.
2. **Double-tap dragging:** tap once, then tap again within 350 ms and hold while moving. The second touch holds the PC left mouse button and finger lift releases it. Movement is flushed before the release. Move the PC pointer over a tab/title bar before dragging. The manual drag toggle remains available.
3. **Mobile selection fix:** the pad and its text prevent native selection, drag and touch callouts, including Safari-specific CSS and non-passive touch handlers. Keyboard text fields retain normal selection/editing.
4. **No connected-session timer:** removed the eight-second inactivity disconnect. Approved sessions remain authorized until manually disconnected or the companion closes. Temporary network failures retry with the same authorization and discard stale queued commands. A separate communication-loss safety check still releases a held mouse button; it does not disconnect the session.

Pairing codes still expire after two minutes and pending approvals after one minute. These setup limits do not limit a connected session. Reloading/closing the phone tab loses its in-memory token and requires desktop Disconnect and pairing again.

## Validation

- 12 Windows Python validation, protocol, QR and session regression tests passed.
- 13 JavaScript gesture and controller tests passed, including second-tap hold/release ordering, selection event prevention, two-finger handling, network recovery and background release.
- Packaged runtime check covers the bundled phone/gesture assets, Tk and actual QR image rendering.
- No automated test emits live mouse or keyboard input. Physical camera scanning, iOS/Android gesture feel and desktop tab dragging still require real-device verification.

## Limitations

This is an unsigned alpha Windows x64 build. HTTP remains unencrypted: use trusted private Wi-Fi only, avoid sensitive text and never forward port 8765. Browser suspension and network outages can interrupt transport even though session authorization no longer expires. Administrator apps and security screens remain unsupported.

The release includes updated setup, troubleshooting, architecture, security, privacy, dependency licenses and checksums.

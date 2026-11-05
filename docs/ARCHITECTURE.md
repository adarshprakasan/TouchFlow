# Architecture and protocol

The Windows companion is a Python app with qrcode for local QR rendering. Tkinter owns desktop approval and executes queued input through Win32 SendInput. A threaded HTTP server serves the self-contained phone page and receives JSON commands. The phone batches pointer deltas and serializes requests. No database or cloud service is used.

## Components

- `companion/touchflow.py`: server, session state, validation, queue, Win32 input and desktop UI.
- `companion/gestures.js`: testable pointer/tap/drag/scroll state machine.
- `companion/phone.html`: responsive trackpad, keyboard, pairing and lifecycle UI; no external assets.
- `index.html`, `app.js`, `styles.css`: earlier visual prototype only.
- `scripts/build_windows.ps1`: portable binary and ZIP packaging.
- `tests/`: validation and HTTP protocol tests that do not emit system input.

## HTTP interface

All POST requests require JSON and a same-origin Origin header. Host must match a local IPv4 address or loopback with port 8765. No CORS permission is granted. Bodies are limited to 4096 bytes. There is no TLS in the current build.

| Route | Request | Result |
| --- | --- | --- |
| GET `/` or `/phone.html` | None | Phone interface |
| POST `/pair` | `code` | A random approval ticket; requires desktop approval |
| POST `/status` | `ticket` | Waiting state or one-time delivery of the session token |
| POST `/input` | `token`, increasing integer `seq`, `kind`, payload | Queued input or heartbeat |
| POST `/disconnect` | `token` | Session revocation |

Command kinds: `move` (x/y relative deltas), `scroll` (y wheel delta), `click` (left/right), `drag` (boolean down), `text` (up to 256 Unicode code points without lone surrogates), `key` (allowlisted special key), `release`, `heartbeat`. Numeric movement is finite and bounded. There is one session, no session expiry, two-minute pairing codes and five pairing attempts per IP per minute. Pending approval expires after 60 seconds. Version negotiation is not implemented.

The queue is bounded. Tokens are rechecked before input execution. Pause/revoke clears queued work; heartbeat remains valid while paused. An eight-second communication-loss safety check clears stale input and releases held drag without revoking the token. Temporary fetch failures preserve authorization, discard buffered work and retry on heartbeats. Desktop shutdown releases a held drag button. Input targets the active Windows application. Windows UIPI prevents ordinary processes from controlling elevated apps and secure desktops.

The companion renders a URL-only QR code in Tk using the qrcode matrix and a native PPM image. The address selector updates both QR and visible URL. No external QR endpoint or image dependency is used. The phone loads `/gestures.js` from the same server. Gesture movement is flushed before button release, preventing the final movement from being sent after the drop. Safari selection/callout prevention is scoped to the pad; keyboard fields retain normal text editing.

Version 0.2.1 rechecks pending approval age after the desktop dialog and at each request. Heartbeat responses include effective pause state. A failed button release is retained for retry at most twice per second; movement is blocked until release succeeds. The poll wrapper always schedules its next invocation, even when recovery raises. Numeric validation uses bounded comparisons without converting arbitrary JSON integers to float.

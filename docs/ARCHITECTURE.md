# Architecture and protocol

The Windows companion is a Python standard-library app. Tkinter owns desktop approval and executes queued input through Win32 SendInput. A threaded HTTP server serves the self-contained phone page and receives JSON commands. The phone batches pointer deltas and serializes requests. No database or cloud service is used.

## Components

- `companion/touchflow.py`: server, session state, validation, queue, Win32 input and desktop UI.
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

Command kinds: `move` (x/y relative deltas), `scroll` (y wheel delta), `click` (left/right), `drag` (boolean down), `text` (up to 256 Unicode code points without lone surrogates), `key` (allowlisted special key), `release`, `heartbeat`. Numeric movement is finite and bounded. There is one session, an eight-second heartbeat timeout, two-minute pairing codes and five pairing attempts per IP per minute. Pending approval expires after 60 seconds. Version negotiation is not implemented.

The queue is bounded. Tokens are rechecked before input execution. Pause/revoke clears queued work; heartbeat remains valid while paused. Desktop shutdown releases a held drag button. Input targets the active Windows application. Windows UIPI prevents ordinary processes from controlling elevated apps and secure desktops.

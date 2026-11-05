# Review and validation of 0.2.1

This patch addresses the four confirmed defects found during review of 0.2.0. It does not certify that the code has no other defects.

| Finding | Fix | Regression evidence |
| --- | --- | --- |
| Failed button release could stop input polling | Retain held state for bounded retry, block new input while recovery is pending, and always schedule the next poll | Simulated SendInput failure then successful retry; polling and recovery exceptions both preserve scheduling |
| Old approval dialog bypassed pending-request expiry | Check pending age in handlers and after the confirmation dialog returns | Boundary at 60 seconds and delayed approval at 600 seconds; rejection and replaced requests do not authorize |
| Successful heartbeat hid paused status | Return effective pause state and reset pending gestures on pause acknowledgement | Real server pause/resume responses and JavaScript status assertions; running desktop pause reflected in the browser |
| Huge integer overflowed movement validation | Compare numeric bounds without float conversion | HTTP rejection of 400-digit move/scroll values, followed by a successful heartbeat |

40 automated tests passed locally. The packaged executable self-test passed for QR rendering, Tk, Windows input structure and bundled web assets. GitHub Actions runs the same tests, builds a Windows x64 package and performs the executable self-test. No automated test emits live system input.

The user tested 0.2.0 on their own setup before this patch. The 0.2.1 browser/desktop check used a local isolated fixture with OS input stubbed out. Broad physical-device testing remains an alpha-release limitation. Screenshot provenance is recorded in [Screenshots](SCREENSHOTS.md).

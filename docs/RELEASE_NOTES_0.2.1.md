# TouchFlow 0.2.1 alpha

Patch release addressing four confirmed code-review findings.

## Download

Close older companion windows, download **TouchFlow-0.2.1-windows-x64.zip**, extract it and launch **TouchFlow.exe**. Python is bundled. Scan the QR and pair your phone again. The release is unsigned and uses unencrypted local HTTP; use trusted private Wi-Fi only.

## Fixes

1. Blocked mouse-button release no longer stops the recurring input loop. The release remains pending and is retried at a bounded rate. New movement is blocked while release is pending, and polling is rescheduled even when error recovery fails.
2. Approval expiry is checked after the desktop confirmation returns and in HTTP handlers. An old dialog cannot authorize an expired request; undelivered expired approvals cannot strand a session token.
3. Heartbeats carry effective pause state, so the phone does not falsely report active control while the PC is paused. Queued gestures and drag indicators are cleared on a pause response.
4. Movement/scroll range checks reject huge JSON integers and non-finite values without float-conversion overflow. Malformed movement receives a controlled rejection and later requests still work.

## Validation

All 40 automated tests pass: 25 Windows Python protocol/lifecycle/validation tests and 15 JavaScript gesture/controller tests, including new regressions for these four defects. Portable checks cover the bundled phone and gesture files, native Windows input structure, Tk and QR image rendering. Automated tests do not emit live desktop input. Hosted Windows build results are linked from the repository Actions tab.

These checks provide coverage for the reported defects, not a guarantee that the application contains no other bugs. Existing alpha limitations remain: Windows x64, one phone, local trusted network, no elevated/secure-screen control and no session duration limit.

The running companion and phone interface were also checked together in an isolated review instance: the real desktop Pause control produced a paused phone status through the heartbeat. Screenshots and their capture conditions are documented in [Screenshots](SCREENSHOTS.md).

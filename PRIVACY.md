# Privacy

TouchFlow sends pointer, scroll, button, key and text commands from the phone browser to the Windows companion over the local network. The companion sees the phone's local IP address for pairing approval and rate limiting.

There is no TouchFlow cloud service, account, advertising, analytics or crash-report upload. Pairing state, rate-limit entries and queued commands are kept in memory. The application does not intentionally write input content, tokens, codes or HTTP request logs to disk. Temporary packaging files and Windows security/crash records may still be produced by the runtime or operating system.

The connection is plain HTTP and is not encrypted. People able to intercept local network traffic may see typed text and session tokens. Use only a trusted private network and avoid sensitive text. Closing the companion ends its sessions. No pairing is remembered across restarts.

The root visual prototype references Google Fonts. Opening that separate prototype can contact Google. The working `companion/phone.html` interface has no external font, script or analytics requests.

GitHub downloads, issues and repository pages are governed by GitHub's own policies.

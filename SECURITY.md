# Security policy

## Supported version

Only the latest 0.1.x alpha is considered for fixes. TouchFlow is experimental and has not received an independent security audit.

## Network boundary

The companion listens on all IPv4 interfaces on port 8765. It uses plain HTTP, not TLS. Pairing provides authorization but does not encrypt traffic or resist an on-path network attacker. Use only a trusted private network. Do not expose the port to the internet, enable router forwarding, or send passwords/sensitive text. Do not run as administrator.

The current design uses short-lived random pairing codes, desktop approval, random in-memory session tokens, same-origin and Host checks, bounded command payloads, increasing sequence numbers, pairing attempt limits and an inactivity timeout. These measures are not a substitute for transport encryption. A paired device can control the foreground application, including potentially destructive actions; approve only your own phone.

One phone is supported. Pause blocks input; Disconnect revokes its token; closing stops the server. Held drag buttons are released on pause/disconnect/timeout. Physical access to the PC remains the recovery path.

## Report a vulnerability

Use GitHub's private **Report a vulnerability** option under the repository Security tab. Include the affected version, impact and minimal reproduction without real tokens or private input. Do not post exploitable details publicly before a fix can be assessed. If the private reporting option is unavailable, open an issue requesting a private reporting channel without disclosing the vulnerability.

There is no guaranteed response time or security service-level agreement. Transport encryption and further protocol hardening are roadmap items.

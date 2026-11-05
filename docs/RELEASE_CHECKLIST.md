# Release checklist

- [ ] Confirm version, changelog and known limitations.
- [ ] Run focused unit/protocol tests without emitting live input.
- [ ] Build on Windows x64 with the pinned build dependency.
- [ ] Run the packaged `--self-test` and inspect its JSON output.
- [ ] Verify portable ZIP includes executable, user documentation and bundled third-party licenses.
- [ ] Generate and verify SHA-256 checksums.
- [ ] Record real-phone coverage separately; disclose missing coverage.
- [ ] Review staged files for secrets, codes, tokens, generated artifacts and private details.
- [ ] Tag the exact commit, publish alpha release assets and disclose unsigned/unencrypted status.
- [ ] Confirm repository visibility, license, description, topics, Issues and private vulnerability reporting.

Do not mark unperformed manual checks as passed. Keep early releases flagged as prereleases until reliability and device coverage justify a stable release.

# Contributing

Open an issue before substantial changes. Keep TouchFlow independent of other projects. Use Python 3.12 on Windows; install the pinned runtime dependencies in `requirements.txt`. See [development](docs/DEVELOPMENT.md).

Use a feature branch and submit a pull request describing the behavior, reason, validation and limitations. Do not commit pairing codes, tokens, user input, generated binaries, private network addresses or credentials. Add focused tests for authentication, input validation and failure recovery changes. Never make tests emit live keyboard or mouse input.

Test changes with `.venv\Scripts\python.exe -m unittest discover -s tests -v` and `node --test tests/gestures.test.cjs tests/phone.test.cjs`. For release changes, also build and run the packaged self-test. Real-phone checks should use non-sensitive text in a disposable document and a trusted network. Record the device/browser versions you actually used.

Keep setup and security documentation aligned with behavior. Follow [Code of Conduct](CODE_OF_CONDUCT.md). Contributions are provided under the repository's MIT license.

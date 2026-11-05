# Getting started

## Portable Windows download

Download the Windows x64 ZIP from the [alpha release](https://github.com/adarshprakasan/TouchFlow/releases). Use the asset named `TouchFlow-0.1.0-windows-x64.zip`, rather than GitHub's automatic source archive, if you want the included executable. Extract the entire archive and launch `TouchFlow.exe`. Python is bundled. Keep the companion window open.

The build is unsigned. Windows may display a reputation warning; TouchFlow does not disable or bypass Windows security controls. Review the release and checksums before deciding whether to run it.

## Connect a phone

1. Put the PC and phone on the same trusted private network.
2. Read the address in the companion window. With multiple adapters, use the Wi-Fi address matching your home network. Virtual adapters and VPN addresses may be unreachable from your phone.
3. Type the full displayed address in the phone's browser address bar. Example only: `http://192.168.1.20:8765`. Your PC address will differ.
4. Enter the eight-character code from the PC. Codes expire after two minutes; click New pairing code when needed.
5. Approve only your phone in the desktop confirmation dialog. Approval requests expire after 60 seconds.
6. Use the touch controls. Before sending text, select the destination application and text field on the PC.

If Windows asks about firewall access, decide whether to allow TouchFlow on your private network. The app does not change firewall rules automatically. Do not allow access on public networks or configure router port forwarding.

## Stop and reconnect

Pause input temporarily blocks commands; Resume enables them again. Disconnect phone revokes the session. Closing the companion stops the service. Phone sessions time out after eight seconds without activity or heartbeats. Generate a new code and pair again after a timeout.

The drag toggle holds a mouse button until released. Turn it off to end a drag. Pause, disconnect and timeout also release it. One phone is supported at a time.

## Update or remove

Close the running companion before replacing its extracted folder with a newer release. To remove it, close the app and delete the extracted folder. TouchFlow adds no startup entry and intentionally stores no pairing data, input history or settings. OS-generated crash/security records and temporary files from packaging are outside this policy.

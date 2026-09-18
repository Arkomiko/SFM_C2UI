"""Example plugin - the smallest useful C2UI script."""


def register(api):
    api.log.info("Hello from example_hello (workspace=%s)", api.app.workspace.current.id if api.app.workspace.current else "?")

    def say_hello():
        api.status(api.tr("status.ready") + "  -  Hello from a C2UI plugin!")
        if api.bridge.connected:
            try:
                info = api.sfm_call("c2ui.hello", {"client": "example_hello"})
                api.log.info("SFM agent replied: %s", info)
            except Exception as exc:  # noqa: BLE001
                api.log.warning("SFM call failed: %s", exc)

    api.register_action("example_hello.say_hello", "Hello C2UI", say_hello, icon="info", shortcut="Ctrl+Alt+H")
    api.add_menu_action("Plugins", "example_hello.say_hello")
    api.events.subscribe("sfm.connected", lambda payload: api.log.info("SFM connected: %s", payload))


def unregister(api):
    api.log.info("example_hello unloaded")

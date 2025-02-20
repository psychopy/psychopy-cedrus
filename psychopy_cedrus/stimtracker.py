from .base import BaseXidDevice, BaseXidButtonGroup, BaseXidLightSensorGroup, BaseXidSoundSensorGroup


class StimTrackerDevice(BaseXidDevice):
    productId = b"S"

    def __init__(
        self, index=0, enableResponses=True
    ):
        # initialise
        BaseXidDevice.__init__(
            self, index=index
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.set_enable_usb_output(selector, True)


class StimTrackerButtonGroup(BaseXidButtonGroup):
    parentCls = StimTrackerDevice

    def __init__(
        self, pad=0, channels=8, bounce=0.005, enableResponses=True
    ):
        # initialise
        BaseXidButtonGroup.__init__(
            self, pad=pad, channels=channels, bounce=bounce
        )


class StimTrackerLightSensorGroup(BaseXidLightSensorGroup):
    parentCls = StimTrackerDevice

    def __init__(
        self, pad=0, channels=3, enableResponses=True
    ):
        # initialise
        BaseXidLightSensorGroup.__init__(
            self, pad=pad, channels=channels
        )


class StimTrackerSoundSensorGroup(BaseXidSoundSensorGroup):
    parentCls = StimTrackerDevice
    
    def __init__(
        self, pad=0, channels=3, threshold=None, enableResponses=True
    ):
        # initialise
        BaseXidSoundSensorGroup.__init__(
            self, pad=pad, channels=channels, threshold=threshold
        )
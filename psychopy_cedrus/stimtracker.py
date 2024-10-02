from .base import BaseXidDevice, BaseXidButtonGroup, BaseXidPhotodiodeGroup, BaseXidVoiceKeyGroup


class StimTrackerDevice(BaseXidDevice):
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
                self.xid.enable_usb_output(selector, True)


class StimTrackerButtonGroup(BaseXidButtonGroup):
    def __init__(
        self, pad=0, channels=8, enableResponses=True
    ):
        # initialise
        BaseXidButtonGroup.__init__(
            self, pad=pad, channels=channels
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.enable_usb_output(selector, True)


class StimTrackerPhotodiodeGroup(BaseXidPhotodiodeGroup):
    def __init__(
        self, pad=0, channels=3, enableResponses=True
    ):
        # initialise
        BaseXidPhotodiodeGroup.__init__(
            self, pad=pad, channels=channels
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.enable_usb_output(selector, True)


class StimTrackerVoiceKeyGroup(BaseXidVoiceKeyGroup):
    def __init__(
        self, index=0, channels=3, threshold=None, enableResponses=True
    ):
        # initialise
        BaseXidDevice.__init__(
            self, index=index, channels=channels, threshold=threshold
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.enable_usb_output(selector, True)
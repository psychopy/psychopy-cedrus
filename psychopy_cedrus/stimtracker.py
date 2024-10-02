from .base import BaseXidDevice, BaseXidButtonGroup, BaseXidPhotodiodeGroup, BaseXidVoicekeyGroup


class StimTracker(BaseXidDevice):
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
        self, index=0, enableResponses=True
    ):
        # initialise
        BaseXidButtonGroup.__init__(
            self, index=index
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.enable_usb_output(selector, True)


class StimTrackerPhotodiodeGroup(BaseXidPhotodiodeGroup):
    def __init__(
        self, index=0, enableResponses=True
    ):
        # initialise
        BaseXidPhotodiodeGroup.__init__(
            self, index=index
        )
        # allow USB input (it's disabled by default)
        if enableResponses:
            for selector in self.selectors:
                self.xid.enable_usb_output(selector, True)


class StimTrackerVoicekeyGroup(BaseXidVoicekeyGroup):
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
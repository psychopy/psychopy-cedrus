from psychopy_cedrus.base import BaseXidDevice, BaseXidButtonGroup, BaseXidPhotodiodeGroup, BaseXidVoiceKeyGroup


class RBDevice(BaseXidDevice):
    productId = b"2"


class RBButtonGroup(BaseXidButtonGroup):
    parentCls = RBDevice


class RBPhotodiodeGroup(BaseXidPhotodiodeGroup):
    parentCls = RBDevice


class RBVoiceKeyGroup(BaseXidVoiceKeyGroup):
    parentCls = RBDevice

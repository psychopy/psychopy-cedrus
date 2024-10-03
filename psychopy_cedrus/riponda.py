from .base import BaseXidDevice, BaseXidButtonGroup, BaseXidPhotodiodeGroup, BaseXidVoiceKeyGroup


class RipondaDevice(BaseXidDevice):
    productId = b"5"


class RipondaButtonGroup(BaseXidButtonGroup):
    parentCls = RipondaDevice


class RipondaPhotodiodeGroup(BaseXidPhotodiodeGroup):
    parentCls = RipondaDevice


class RipondaVoiceKeyGroup(BaseXidVoiceKeyGroup):
    parentCls = RipondaDevice

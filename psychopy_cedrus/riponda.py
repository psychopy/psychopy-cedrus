from .base import BaseXidDevice, BaseXidButtonGroup, BaseXidLightSensorGroup, BaseXidSoundSensorGroup


class RipondaDevice(BaseXidDevice):
    productId = b"5"


class RipondaButtonGroup(BaseXidButtonGroup):
    parentCls = RipondaDevice


class RipondaLightSensorGroup(BaseXidLightSensorGroup):
    parentCls = RipondaDevice


class RipondaSoundSensorGroup(BaseXidSoundSensorGroup):
    parentCls = RipondaDevice

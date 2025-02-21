from psychopy_cedrus.base import BaseXidDevice, BaseXidButtonGroup, BaseXidLightSensorGroup, BaseXidSoundSensorGroup


class LuminaDevice(BaseXidDevice):
    productId = b"0"


class LuminaButtonGroup(BaseXidButtonGroup):
    parentCls = LuminaDevice

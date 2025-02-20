from psychopy_cedrus.base import BaseXidDevice, BaseXidButtonGroup, BaseXidLightSensorGroup, BaseXidSoundSensorGroup


class RBDevice(BaseXidDevice):
    productId = b"2"


class RBButtonGroup(BaseXidButtonGroup):
    parentCls = RBDevice


class RBLightSensorGroup(BaseXidLightSensorGroup):
    parentCls = RBDevice


class RBSoundSensorGroup(BaseXidSoundSensorGroup):
    parentCls = RBDevice

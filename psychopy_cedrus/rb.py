from psychopy_cedrus import riponda
from psychopy.hardware.manager import deviceManager, DeviceManager, ManagedDeviceError
from psychopy import logging, layout
import pyxid2


class RBPhotodiodeGroup(riponda.RipondaPhotodiodeGroup):
    pass


class RBButtonGroup(riponda.RipondaButtonGroup):
    pass


class RBVoicekeyGroup(riponda.RipondaVoicekeyGroup):
    pass


class RB(riponda.Riponda):
    pass

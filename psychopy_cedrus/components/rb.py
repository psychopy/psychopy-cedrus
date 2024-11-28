from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.photodiodeValidator import PhotodiodeValidatorRoutine
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class RBPhotodiodeValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = PhotodiodeValidatorRoutine
    # what value should Builder use for this backend?
    key = "rb"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus RB Series")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.rb.RBPhotodiodeGroup"]

    def getParams(self):
        return util.getXidPhotodiodeParams(key="rb")
    
    def writeDeviceCode(self, buff):
        return util.writeXidPhotodiodeCode(
            self,
            buff,
            cls="psychopy_cedrus.rb.RBPhotodiodeGroup",
            key="rb"
        )


class RBButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "rb"
    label = _translate("Cedrus RB Series")
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.rb.RBButtonGroup"]

    def getParams(self):
        return util.getXidButtonBoxParams(key="rb")
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self,
            buff,
            cls="psychopy_cedrus.rb.RBButtonGroup",
            key="rb"
        )
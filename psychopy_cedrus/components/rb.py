from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.visualValidator import VisualValidatorRoutine
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class RBPhotodiodeValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = VisualValidatorRoutine
    # what value should Builder use for this backend?
    key = "rb"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus RB Series")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.rb.RBPhotodiodeGroup"]

    def getParams(self):
        return util.getXidPhotodiodeParams(key="rb")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
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

    def addRequirements(self: ButtonBoxComponent):
        self.exp.requireImport(
            importName="rb", 
            importFrom="psychopy_cedrus"
        )
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self,
            buff,
            cls="psychopy_cedrus.rb.RBButtonGroup",
            key="rb"
        )
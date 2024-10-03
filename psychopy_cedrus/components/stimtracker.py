from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.photodiodeValidator import PhotodiodeValidatorRoutine
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class StimTrackerPhotodiodeValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = PhotodiodeValidatorRoutine
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerPhotodiodeGroup"]

    def getParams(self):
        return util.getXidPhotodiodeParams(key="stimtracker")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        self.exp.requireImport(
            importName="stimtracker",
            importFrom="psychopy_cedrus"
        )
    
    def writeDeviceCode(self, buff):
        return util.writeXidPhotodiodeCode(
            self, 
            buff, 
            cls="psychopy_cedrus.stimtracker.StimTrackerPhotodiodeGroup",
            key="stimtracker"
        )



class StimTrackerButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "stimtracker"
    label = _translate("Cedrus StimTracker")
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerButtonGroup"]

    def getParams(self):
        return util.getXidButtonBoxParams(key="stimtracker")
    
    def addRequirements(self: ButtonBoxComponent):
        self.exp.requireImport(
            importName="stimtracker", 
            importFrom="psychopy_cedrus"
        )
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self, 
            buff, 
            cls="psychopy_cedrus.stimtracker.StimTrackerButtonGroup",
            key="stimtracker"
        )

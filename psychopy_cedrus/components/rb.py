from psychopy.experiment.plugins import PluginDevicesMixin
from psychopy.experiment.devices import DeviceBackend
from psychopy.localization import _translate
from . import util

# import Component/Routine classes in a version-safe way
try:
    from psychopy.experiment.components.buttonBox import ButtonBoxComponent
except ImportError:
    ButtonBoxComponent = PluginDevicesMixin
try:
    from psychopy.experiment.routines.visualValidator import VisualValidatorRoutine
except ImportError:
    VisualValidatorRoutine = PluginDevicesMixin
try:
    from psychopy.experiment.routines.audioValidator import AudioValidatorRoutine
except ImportError:
    AudioValidatorRoutine = PluginDevicesMixin
try:
    from psychopy.experiment.components.soundsensor import SoundSensorComponent
except ImportError:
    SoundSensorComponent = PluginDevicesMixin


class RBLightSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "rb"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus RB Series Light Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.rb.RBLightSensorGroup"

    def getParams(self):
        return util.getXidLightSensorParams(key="rb")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidLightSensorCode(
            self,
            buff,
            cls="psychopy_cedrus.rb.RBLightSensorGroup",
            key="rb"
        )


class RBSoundSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "rb"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus RB Series Sound Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.rb.RBSoundSensorGroup"

    def getParams(self):
        return util.getXidSoundSensorParams(key="rb")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidSoundSensorCode(
            self, 
            buff, 
            cls="psychopy_cedrus.rb.RBSoundSensorGroup",
            key="rb"
        )


class RBButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "rb"
    label = _translate("Cedrus RB Series Button Box")
    deviceClass = "psychopy_cedrus.rb.RBButtonGroup"

    def getParams(self):
        return util.getXidButtonBoxParams(key="rb")

    def addRequirements(self):
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


# register backends with Components
VisualValidatorRoutine.registerBackend(RBLightSensorBackend)
SoundSensorComponent.registerBackend(RBSoundSensorBackend)
AudioValidatorRoutine.registerBackend(RBSoundSensorBackend)
ButtonBoxComponent.registerBackend(RBButtonBoxBackend)

# add legacy params
SoundSensorComponent.legacyParams += util.getXidSoundSensorParams("rb")[1]
AudioValidatorRoutine.legacyParams += util.getXidSoundSensorParams("rb")[1]
VisualValidatorRoutine.legacyParams += util.getXidLightSensorParams("rb")[1]
ButtonBoxComponent.legacyParams += util.getXidButtonBoxParams("rb")[1]

# alias legacy class names
RBVisualValidatorBackend = RBLightSensorBackend
RBAudioValidatorBackend = RBSoundSensorBackend
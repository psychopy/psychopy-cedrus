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


class RipondaLightSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "riponda"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus Riponda Light Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.riponda.RipondaLightSensorGroup"

    def getParams(self):
        return util.getXidLightSensorParams(key="riponda")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidLightSensorCode(
            self,
            buff,
            cls="psychopy_cedrus.riponda.RipondaLightSensorGroup",
            key="riponda"
        )


class RipondaSoundSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "riponda"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus Riponda Sound Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.riponda.RipondaSoundSensorGroup"

    def getParams(self):
        return util.getXidSoundSensorParams(key="riponda")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidSoundSensorCode(
            self,
            buff,
            cls="psychopy_cedrus.riponda.RipondaSoundSensorGroup",
            key="riponda"
        )


class RipondaButtonBoxBackend(DeviceBackend):
    """
    Adds support for the Cedrus Riponda button box.
    """
    key = "riponda"
    label = _translate("Cedrus Riponda Button Box")
    deviceClass = "psychopy_cedrus.riponda.RipondaButtonGroup"

    def getParams(self):
        return util.getXidButtonBoxParams(key="riponda")

    def addRequirements(self):
        self.exp.requireImport(
            importName="riponda", 
            importFrom="psychopy_cedrus"
        )
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self,
            buff,
            cls="psychopy_cedrus.riponda.RipondaButtonGroup",
            key="riponda"
        )


# register backends with Components
VisualValidatorRoutine.registerBackend(RipondaLightSensorBackend)
AudioValidatorRoutine.registerBackend(RipondaSoundSensorBackend)
SoundSensorComponent.registerBackend(RipondaSoundSensorBackend)
ButtonBoxComponent.registerBackend(RipondaButtonBoxBackend)

# add legacy params
SoundSensorComponent.legacyParams += util.getXidSoundSensorParams("riponda")[1]
AudioValidatorRoutine.legacyParams += util.getXidSoundSensorParams("riponda")[1]
VisualValidatorRoutine.legacyParams += util.getXidLightSensorParams("riponda")[1]
ButtonBoxComponent.legacyParams += util.getXidButtonBoxParams("riponda")[1]

# alias legacy class names
RipondaVisualValidatorBackend = RipondaLightSensorBackend
RipondaAudioValidatorBackend = RipondaSoundSensorBackend
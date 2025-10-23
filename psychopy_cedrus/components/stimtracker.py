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


class StimTrackerLightSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker Light Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.stimtracker.StimTrackerLightSensorGroup"

    def getParams(self):
        return util.getXidLightSensorParams(key="stimtracker")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidLightSensorCode(
            self, 
            buff, 
            cls="psychopy_cedrus.stimtracker.StimTrackerLightSensorGroup",
            key="stimtracker"
        )


class StimTrackerSoundSensorBackend(DeviceBackend):
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker Sound Sensor")
    # what hardware classes are relevant to this backend?
    deviceClass = "psychopy_cedrus.stimtracker.StimTrackerSoundSensorGroup"

    def getParams(self):
        return util.getXidSoundSensorParams(key="stimtracker")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidSoundSensorCode(
            self, 
            buff, 
            cls="psychopy_cedrus.stimtracker.StimTrackerSoundSensorGroup",
            key="stimtracker"
        )


class StimTrackerButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "stimtracker"
    label = _translate("Cedrus StimTracker Button Box")
    deviceClass = "psychopy_cedrus.stimtracker.StimTrackerButtonGroup"

    def getParams(self):
        return util.getXidButtonBoxParams(key="stimtracker")
    
    def addRequirements(self):
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


# register backends with Components
VisualValidatorRoutine.registerBackend(StimTrackerLightSensorBackend)
SoundSensorComponent.registerBackend(StimTrackerSoundSensorBackend)
AudioValidatorRoutine.registerBackend(StimTrackerSoundSensorBackend)
ButtonBoxComponent.registerBackend(StimTrackerButtonBoxBackend)

# add legacy params
SoundSensorComponent.legacyParams += util.getXidSoundSensorParams("stimtracker")[1]
AudioValidatorRoutine.legacyParams += util.getXidSoundSensorParams("stimtracker")[1]
VisualValidatorRoutine.legacyParams += util.getXidLightSensorParams("stimtracker")[1]
ButtonBoxComponent.legacyParams += util.getXidButtonBoxParams("stimtracker")[1]

# alias legacy class names
SoundSensorVisualValidatorBackend = SoundSensorLightSensorBackend
SoundSensorAudioValidatorBackend = SoundSensorSoundSensorBackend
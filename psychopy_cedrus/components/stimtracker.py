from psychopy.experiment.plugins import DeviceBackend, PluginDevicesMixin
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


class StimTrackerVisualValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = VisualValidatorRoutine
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker Light Sensor")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerLightSensorGroup"]

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


class StimTrackerAudioValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = AudioValidatorRoutine
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker Sound Sensor")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerSoundSensorGroup"]

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
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerButtonGroup"]

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


class RipondaSoundSensorBackend(DeviceBackend):
    """
    Implements StimTracker for the SoundSensor Component
    """

    key = "stimtracker"
    label = _translate("Cedrus StimTracker")
    component = SoundSensorComponent
    deviceClasses = ["psychopy_cedrus.stimtracker.StimTrackerSoundSensorGroup"]

    def getParams(self):
        return util.getXidSoundSensorParams("stimtracker")

    def addRequirements(self):
        self.exp.requireImport(
            importName="stimtracker", importFrom="psychopy_cedrus"
        )

    def writeDeviceCode(self, buff):
        return util.writeXidSoundSensorCode(
            self, 
            buff, 
            cls="psychopy_cedrus.stimtracker.StimTrackerSoundSensorGroup",
            key="stimtracker"
        )

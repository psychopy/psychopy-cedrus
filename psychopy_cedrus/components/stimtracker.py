from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.visualValidator import VisualValidatorRoutine
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class StimTrackerVisualValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = VisualValidatorRoutine
    # what value should Builder use for this backend?
    key = "stimtracker"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus StimTracker")
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


if Version(ppyVersion) >= Version("2025.1.0"):
    # base sound sensor support was only added in 2025.1, so this is necessary to handle older versions
    from psychopy.experiment.components.soundsensor import SoundSensorComponent

    class RipondaSoundSensorBackend(DeviceBackend):
        """
        Implements Riponda for the SoundSensor Component
        """

        key = "riponda"
        label = _translate("Cedrus Riponda")
        component = SoundSensorComponent
        deviceClasses = ['psychopy.hardware.soundsensor.MicrophoneSoundSensor']

        def getParams(self: SoundSensorComponent):
            # define order
            order = [
                "ripondaIndex",
                "ripondaChannels",
                "ripondaThreshold",
            ]
            # define params
            params = {}       
            params['ripondaIndex'] = Param(
                0, valType='int', inputType="single", categ='Device',
                label=_translate("Device number"),
                hint=_translate(
                    "Device number, if you have multiple devices which one do you want (0, 1, 2...)"
                )
            )
            params['ripondaChannels'] = Param(
                7, valType="code", inputType="single", categ="Device",
                label=_translate("Num. channels"),
                hint=_translate(
                    "How many microphones are plugged into this Riponda?"
                )
            )
            params['ripondaThreshold'] = Param(
                0, valType='code', inputType="single", categ='Device',
                label=_translate("Threshold"),
                hint=_translate(
                    "Threshold volume (0 for min, 255 for max) above which to register a voicekey "
                    "response"
                )
            )

            return params, order

        def addRequirements(self):
            self.exp.requireImport(
                importName="riponda", importFrom="psychopy_cedrus"
            )

        def writeDeviceCode(self: SoundSensorComponent, buff):
            # get inits
            inits = getInitVals(self.params)
            # make ButtonGroup object
            code = (
                "deviceManager.addDevice(\n"
                "    deviceClass='psychopy_cedrus.riponda.RipondaSoundSensorGroup',\n"
                "    deviceName=%(deviceLabel)s,\n"
                "    pad=%(ripondaIndex)s,\n"
                "    channels=%(ripondaChannels)s\n"
                "    threshold=%(ripondaThreshold)s,\n"
                ")\n"
            )
            buff.writeIndentedLines(code % inits)

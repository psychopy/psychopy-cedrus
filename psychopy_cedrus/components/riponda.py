from packaging.version import Version
from psychopy import __version__ as ppyVersion
from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.visualValidator import VisualValidatorRoutine
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class RipondaPhotodiodeValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = VisualValidatorRoutine
    # what value should Builder use for this backend?
    key = "riponda"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus Riponda")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.riponda.RipondaPhotodiodeGroup"]

    def getParams(self):
        return util.getXidPhotodiodeParams(key="riponda")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidPhotodiodeCode(
            self,
            buff,
            cls="psychopy_cedrus.riponda.RipondaPhotodiodeGroup",
            key="riponda"
        )


class RipondaButtonBoxBackend(DeviceBackend):
    """
    Adds support for the Cedrus Riponda button box.
    """
    key = "riponda"
    label = _translate("Cedrus Riponda")
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.riponda.RipondaButtonGroup"]

    def getParams(self):
        return util.getXidButtonBoxParams(key="riponda")

    def addRequirements(self: ButtonBoxComponent):
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

if Version(ppyVersion) >= Version("2025.1.0"):
    # base voicekey support was only added in 2025.1, so this is necessary to handle older versions
    from psychopy.experiment.components.voicekey import VoiceKeyComponent

    class RipondaVoiceKeyBackend(DeviceBackend):
        """
        Implements Riponda for the VoiceKey Component
        """

        key = "riponda"
        label = _translate("Cedrus Riponda")
        component = VoiceKeyComponent
        deviceClasses = ['psychopy.hardware.voicekey.MicrophoneVoiceKeyEmulator']

        def getParams(self: VoiceKeyComponent):
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

        def writeDeviceCode(self: VoiceKeyComponent, buff):
            # get inits
            inits = getInitVals(self.params)
            # make ButtonGroup object
            code = (
                "deviceManager.addDevice(\n"
                "    deviceClass='psychopy_cedrus.riponda.RipondaVoiceKeyGroup',\n"
                "    deviceName=%(deviceLabel)s,\n"
                "    pad=%(ripondaIndex)s,\n"
                "    channels=%(ripondaChannels)s\n"
                "    threshold=%(ripondaThreshold)s,\n"
                ")\n"
            )

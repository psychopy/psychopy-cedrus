from packaging.version import Version
from psychopy import __version__ as ppyVersion
from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.photodiodeValidator import PhotodiodeValidatorRoutine
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate


class RipondaPhotodiodeValidatorBackend(DeviceBackend):
    # which component is this backend for?
    component = PhotodiodeValidatorRoutine
    # what value should Builder use for this backend?
    key = "riponda"
    # what label should be displayed by Builder for this backend?
    label = _translate("Cedrus Riponda")
    # what hardware classes are relevant to this backend?
    deviceClasses = ["psychopy_cedrus.riponda.RipondaPhotodiodeGroup"]

    def getParams(self):
        """
        Get parameters from this backend to add to each new instance of ButtonBoxComponent

        Returns
        -------
        dict[str:Param]
            Dict of Param objects, which will be added to any Button Box Component's params, along with a dependency
            to only show them when this backend is selected
        list[str]
            List of param names, defining the order in which params should appear
        """
        # define order
        order = [
            "ripondaDeviceNo",
            "ripondaNChannels"
        ]
        # define params
        params = {}

        params['ripondaDeviceNo'] = Param(
            "0", valType="code", inputType="single", categ="Device",
            label=_translate("Device number"),
            hint=_translate(
                "Number of the device to connect to (starts at 0)"
            )
        )
        params['ripondaNChannels'] = Param(
            2, valType="code", inputType="single", categ="Device",
            label=_translate("Num. diodes"),
            hint=_translate(
                "How many diodes this device has."
            )
        )

        return params, order

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        self.exp.requireImport(
            importName="riponda",
            importFrom="psychopy_cedrus"
        )

    def writeDeviceCode(self, buff):
        # get inits
        inits = getInitVals(self.params)
        # make ButtonGroup object
        code = (
            "deviceManager.addDevice(\n"
            "    deviceClass='psychopy_cedrus.riponda.RipondaPhotodiodeGroup',\n"
            "    deviceName=%(deviceLabel)s,\n"
            "    pad=%(ripondaDeviceNo)s,\n"
            "    channels=%(ripondaNChannels)s,\n"
            ")\n"
        )
        buff.writeOnceIndentedLines(code % inits)


class RipondaButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "riponda"
    label = "Cedrus Riponda"
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.riponda.RipondaButtonGroup"]

    def getParams(self: ButtonBoxComponent):
        # define order
        order = [
            "ripondaIndex",
            "ripondaNButtons"
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
        params['ripondaNButtons'] = Param(
            7, valType="code", inputType="single", categ="Device",
            label=_translate("Num. buttons"),
            hint=_translate(
                "How many buttons this button box has."
            )
        )

        return params, order

    def addRequirements(self: ButtonBoxComponent):
        self.exp.requireImport(
            importName="riponda", importFrom="psychopy_cedrus"
        )

    def writeDeviceCode(self, buff):
        # get inits
        inits = getInitVals(self.params)
        # make ButtonGroup object
        code = (
            "deviceManager.addDevice(\n"
            "    deviceClass='psychopy_cedrus.riponda.RipondaButtonGroup',\n"
            "    deviceName=%(deviceLabel)s,\n"
            "    pad=%(ripondaIndex)s,\n"
            "    channels=%(ripondaNButtons)s\n"
            ")\n"
        )
        buff.writeOnceIndentedLines(code % inits)

if Version(ppyVersion) >= "2025.1.0":
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
            buff.writeOnceIndentedLines(code % inits)

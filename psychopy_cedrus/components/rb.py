from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.routines.photodiodeValidator import PhotodiodeValidatorRoutine
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate


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
            "rbDeviceNo",
            "rbNChannels"
        ]
        # define params
        params = {}

        params['rbDeviceNo'] = Param(
            "", valType="str", inputType="single", categ="Device",
            label=_translate("Device number"),
            hint=_translate(
                "Number of the device to connect to (starts at 0)"
            )
        )
        params['rbNChannels'] = Param(
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
            importName="rb",
            importFrom="psychopy_cedrus"
        )

    def writeDeviceCode(self, buff):
        # get inits
        inits = getInitVals(self.params)
        # make ButtonGroup object
        code = (
            "deviceManager.addDevice(\n"
            "    deviceClass='psychopy_cedrus.rb.RBPhotodiodeGroup',\n"
            "    deviceName=%(deviceLabel)s,\n"
            "    pad=%(rbDeviceNo)s,\n"
            "    channels=%(rbNChannels)s,\n"
            ")\n"
        )
        buff.writeOnceIndentedLines(code % inits)


class RBButtonBoxBackend(DeviceBackend):
    """
    Adds a basic serial connection backend for ButtonBoxComponent, as well as acting as an example for implementing
    other ButtonBoxBackends.
    """
    key = "rb"
    label = "Cedrus RB Series"
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.rb.RBButtonGroup"]

    def getParams(self: ButtonBoxComponent):
        # define order
        order = [
            "rbIndex",
            "rbNButtons"
        ]
        # define params
        params = {}
        params['rbIndex'] = Param(
            0, valType='int', inputType="single", categ='Device',
            label=_translate("Device number"),
            hint=_translate(
                "Device number, if you have multiple devices which one do you want (0, 1, 2...)"
            )
        )
        params['rbNButtons'] = Param(
            7, valType="code", inputType="single", categ="Device",
            label=_translate("Num. buttons"),
            hint=_translate(
                "How many buttons this button box has."
            )
        )

        return params, order

    def addRequirements(self: ButtonBoxComponent):
        self.exp.requireImport(
            importName="rb", importFrom="psychopy_cedrus"
        )

    def writeDeviceCode(self, buff):
        # get inits
        inits = getInitVals(self.params)
        # make ButtonGroup object
        code = (
            "deviceManager.addDevice(\n"
            "    deviceClass='psychopy_cedrus.rb.RBButtonGroup',\n"
            "    deviceName=%(deviceLabel)s,\n"
            "    pad=%(rbIndex)s,\n"
            "    channels=%(rbNButtons)s\n"
            ")\n"
        )
        buff.writeOnceIndentedLines(code % inits)

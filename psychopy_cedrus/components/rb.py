from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment import getInitVals, Param
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate


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

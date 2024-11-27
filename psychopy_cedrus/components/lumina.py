from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment.plugins import DeviceBackend
from psychopy.localization import _translate
from . import util


class LuminaButtonBoxBackend(DeviceBackend):
    key = "lumina"
    label = _translate("Cedrus Lumina Series")
    component = ButtonBoxComponent
    deviceClasses = ["psychopy_cedrus.lumina.LuminaButtonGroup"]

    def getParams(self):
        return util.getXidButtonBoxParams(key="lumina")

    def addRequirements(self: ButtonBoxComponent):
        self.exp.requireImport(
            importName="lumina", 
            importFrom="psychopy_cedrus"
        )
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self,
            buff,
            cls="psychopy_cedrus.lumina.LuminaButtonGroup",
            key="lumina"
        )
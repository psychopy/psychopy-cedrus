from psychopy.experiment.plugins import PluginDevicesMixin
from psychopy.experiment.devices import DeviceBackend
from psychopy.localization import _translate
from . import util

try:
    from psychopy.experiment.components.buttonBox import ButtonBoxComponent
except ImportError:
    ButtonBoxComponent = PluginDevicesMixin


class LuminaButtonBoxBackend(DeviceBackend):
    key = "lumina"
    label = _translate("Cedrus Lumina Series Button Box")
    deviceClass = "psychopy_cedrus.lumina.LuminaButtonGroup"

    def getParams(self):
        return util.getXidButtonBoxParams(key="lumina")

    def addRequirements(self):
        """
        Add any required module/package imports for this backend
        """
        return
    
    def writeDeviceCode(self, buff):
        return util.writeXidButtonBoxCode(
            self,
            buff,
            cls="psychopy_cedrus.lumina.LuminaButtonGroup",
            key="lumina"
        )


# register backends with Components
ButtonBoxComponent.registerBackend(LuminaButtonBoxBackend)

# add legacy params
ButtonBoxComponent.legacyParams += util.getXidButtonBoxParams("lumina")[1]

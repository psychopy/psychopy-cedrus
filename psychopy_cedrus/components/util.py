from psychopy.experiment.components.buttonBox import ButtonBoxComponent
from psychopy.experiment import getInitVals, Param
from psychopy.localization import _translate


def getXidButtonBoxParams(key):
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
        f"{key}Index",
        f"{key}ripondaNButtons"
    ]
    # define params
    params = {}
    params[f'{key}Index'] = Param(
        0, valType='int', inputType="single", categ='Device',
        label=_translate("Device number"),
        hint=_translate(
            "Device number, if you have multiple devices which one do you want (0, 1, 2...)"
        )
    )
    params[f'{key}NButtons'] = Param(
        7, valType="code", inputType="single", categ="Device",
        label=_translate("Num. buttons"),
        hint=_translate(
            "How many buttons this button box has."
        )
    )

    return params, order


def writeXidButtonBoxCode(self, buff, cls, key):
    # get inits
    inits = getInitVals(self.params)
    # make ButtonGroup object
    code = (
        f"deviceManager.addDevice(\n"
        f"    deviceClass='{cls}',\n"
        f"    deviceName=%(deviceLabel)s,\n"
        f"    pad=%({key}Index)s,\n"
        f"    channels=%({key}NButtons)s,\n"
        f")\n"
    )
    buff.writeOnceIndentedLines(code % inits)


def getXidLightSensorParams(key):
    # define order
    order = [
        f"{key}DeviceNo",
        f"{key}NChannels"
    ]
    # define params
    params = {}

    params[f'{key}DeviceNo'] = Param(
        "0", valType="code", inputType="single", categ="Device",
        label=_translate("Device number"),
        hint=_translate(
            "Number of the device to connect to (starts at 0)"
        )
    )
    params[f'{key}NChannels'] = Param(
        2, valType="code", inputType="single", categ="Device",
        label=_translate("Num. diodes"),
        hint=_translate(
            "How many sensors this device has."
        )
    )

    return params, order


def writeXidLightSensorCode(self, buff, cls, key):
    # get inits
    inits = getInitVals(self.params)
    # make ButtonGroup object
    code = (
        f"deviceManager.addDevice(\n"
        f"    deviceClass='{cls}',\n"
        f"    deviceName=%(deviceLabel)s,\n"
        f"    pad=%({key}DeviceNo)s,\n"
        f"    channels=%({key}NChannels)s,\n"
        f")\n"
    )
    buff.writeOnceIndentedLines(code % inits)


def getXidSoundSensorParams(key):
    # define order
    order = [
        f"{key}Index",
        f"{key}Channels",
        f"{key}Threshold",
    ]
    # define params
    params = {}       
    params[f'{key}Index'] = Param(
        0, valType='int', inputType="single", categ='Device',
        label=_translate("Device number"),
        hint=_translate(
            "Device number, if you have multiple devices which one do you want (0, 1, 2...)"
        )
    )
    params[f'{key}Channels'] = Param(
        7, valType="code", inputType="single", categ="Device",
        label=_translate("Num. channels"),
        hint=_translate(
            "How many microphones are plugged into this device?"
        )
    )
    params[f'{key}Threshold'] = Param(
        0.5, valType='code', inputType="single", categ='Device',
        label=_translate("Threshold"),
        hint=_translate(
            "Threshold volume (0 for min, 1 for max) above which to register a response"
        )
    )

    return params, order


def writeXidSoundSensorCode(self, buff, cls, key):
    # get inits
    inits = getInitVals(self.params)
    # make SoundSensor object
    code = (
        f"deviceManager.addDevice(\n"
        f"    deviceClass='{cls}',\n"
        f"    deviceName=%(deviceLabel)s,\n"
        f"    pad=%({key}Index)s,\n"
        f"    channels=%({key}Channels)s,\n"
        f"    threshold=%({key}Threshold)s,\n"
        f")\n"
    )
    buff.writeIndentedLines(code % inits)

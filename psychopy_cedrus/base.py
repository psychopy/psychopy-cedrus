from psychopy.hardware import base, photodiode, button
from psychopy.hardware.manager import deviceManager, DeviceManager, ManagedDeviceError
from psychopy import logging, layout, __version__ as ppyVersion
import pyxid2
from packaging.version import Version


class BaseXidPhotodiodeGroup(photodiode.BasePhotodiodeGroup):
    """
    Base class for all Cedrus XID photodiode devices.
    """
    # all selectors for XID photodiode nodes
    selectors = (
        # photodiodes
        "A", "B", "C", "D", 
    )

    def __init__(self, pad, channels=1):
        # get parent
        self.parent = BaseXidDevice.resolve(pad)
        # reference self in parent
        self.parent.nodes.append(self)
        # Xid photodiode should be key 3, but this attribute can be changed if needed
        self.keys = [3]
        # initialise base class
        photodiode.BasePhotodiodeGroup.__init__(self, channels=channels)

    def isSameDevice(self, other):
        """
        Determine whether this object represents the same physical device as a given other
        object.

        Parameters
        ----------
        other : BaseXidPhotodiodeGroup, dict
            Other BaseXidPhotodiodeGroup to compare against, or a dict of params (which must include
            `index` as a key)

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        if isinstance(other, type(self)):
            # if given another BaseXidPhotodiodeGroup, compare parent boxes
            other = other.parent
        elif isinstance(other, dict) and "pad" in other:
            # if given a dict, make sure we have a `port` rather than a `pad`
            other['port'] = other['pad']
        # use parent's comparison method
        return self.parent.isSameDevice(other)

    @staticmethod
    def getAvailableDevices():
        devices = []
        # iterate through profiles of all serial port devices
        for profile in BaseXidDevice.getAvailableDevices():
            devices.append({
                'deviceName': profile['deviceName'] + "_photodiodes",
                'pad': profile['deviceName'],
                'channels': 1,
            })

        return devices

    def _setThreshold(self, threshold, channel=0):
        if threshold is None:
            return
        # store value
        self._threshold = threshold
        # convert from base 16
        thr = threshold / 255 * 100
        # get channel selector
        selector = ["A", "B", "C", "D"][channel]
        # send command
        self.parent.xid.con.send_xid_command(f"it{selector}{thr}")
        # dispatch
        self.dispatchMessages()
        # return True/False according to state
        return self.getState(channel)

    def resetTimer(self, clock=logging.defaultClock):
        self.parent.resetTimer(clock=clock)

    def dispatchMessages(self):
        """
        Dispatch messages from parent BaseXid to this photodiode group

        Returns
        -------
        bool
            True if request sent successfully
        """
        self.parent.dispatchMessages()

    def parseMessage(self, message):
        # work out channel from key
        channel = 0
        if message['key'] in self.keys:
            channel = self.keys.index(message['key'])
        # create PhotodiodeResponse object
        resp = photodiode.PhotodiodeResponse(
            t=message['time'], channel=channel, value=message['pressed'], 
            threshold=self.getThreshold(channel)
        )

        return resp


class BaseXidButtonGroup(button.BaseButtonGroup):
    # all selectors for XID button nodes
    selectors = (
        # response keys
        "K", 
    )
    def __init__(self, pad=0, channels=7):
        # get parent
        self.parent = BaseXidDevice.resolve(pad)
        # reference self in parent
        self.parent.nodes.append(self)
        # initialise base class
        button.BaseButtonGroup.__init__(self, channels=channels)

    def isSameDevice(self, other):
        """
        Determine whether this object represents the same physical device as a given other
        object.

        Parameters
        ----------
        other : BaseXidButtonGroup, dict
            Other BaseXidButtonGroup to compare against, or a dict of params (which must include
            `index` as a key)

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        if isinstance(other, type(self)):
            # if given another BaseXidButtonGroup, compare parent boxes
            other = other.parent
        elif isinstance(other, dict) and "pad" in other:
            # if given a dict, make sure we have a `port` rather than a `pad`
            other['port'] = other['pad']
        # use parent's comparison method
        return self.parent.isSameDevice(other)

    def dispatchMessages(self):
        """
        Dispatch messages from parent BaseXid to this button group

        Returns
        -------
        bool
            True if request sent successfully
        """
        self.parent.dispatchMessages()

    def parseMessage(self, message):
        resp = button.ButtonResponse(
            t=message['time'], channel=message['key'], value=message['pressed']
        )

        return resp

    def resetTimer(self, clock=logging.defaultClock):
        self.parent.resetTimer(clock=clock)

    @staticmethod
    def getAvailableDevices():
        devices = []
        # iterate through profiles of all serial port devices
        for profile in BaseXidDevice.getAvailableDevices():
            devices.append({
                'deviceName': profile['deviceName'] + "_buttons",
                'pad': profile['deviceName'],
                'index': profile['index'],
                'channels': 7,
            })

        return devices

if Version(ppyVersion) >= Version("2025.1.0"):
    # base voicekey support was only added in 2025.1, so this is necessary to handle older versions
    from psychopy.hardware import voicekey

    class BaseXidVoicekeyGroup(voicekey.BaseVoiceKeyGroup):
        # all selectors for XID voicekey nodes
        selectors = (
            # microphone
            "M", 
            # audio (left and right)
            "L", "R", 
        )
        def __init__(self, pad=0, channels=1, threshold=None):
            # get parent
            self.parent = BaseXidDevice.resolve(pad)
            # reference self in parent
            self.parent.nodes.append(self)
            # BaseXid voicekey should be key 2, but this attribute can be changed if needed
            self.keys = [2]
            # initialise base class
            voicekey.BaseVoiceKeyGroup.__init__(self, channels=channels, threshold=threshold)
        
        def parseMessage(self, message):
            # work out channel from key
            channel = 0
            if message['key'] in self.keys:
                channel = self.keys.index(message['key'])
            # create voicekey resp
            resp = voicekey.VoiceKeyResponse(
                t=message['time'], channel=message['key']-1, value=message['pressed'], 
                threshold=self.getThreshold(channel), device=self
            )

            return resp

        def resetTimer(self, clock=logging.defaultClock):
            self.parent.resetTimer(clock=clock)
        
        def _setThreshold(self, threshold, channel=None):
            if threshold is None:
                return
            # store value
            self._threshold = threshold
            # convert from base 16
            thr = int(threshold / 255 * 100)
            # send command
            self.parent.xid.con.send_xid_command(f"itM{thr}")
            # dispatch
            self.dispatchMessages()
            # return True/False according to state
            return self.getState(channel)

        def isSameDevice(self, other):
            if isinstance(other, type(self)):
                # if given another BaseXidVoiceKeyGroup, compare parent boxes
                other = other.parent
            elif isinstance(other, dict) and "pad" in other:
                # if given a dict, make sure we have a `port` rather than a `pad`
                other['port'] = other['pad']
            # use parent's comparison method
            return self.parent.isSameDevice(other)
        
        @staticmethod
        def getAvailableDevices():
            devices = []
            # iterate through profiles of all serial port devices
            for profile in BaseXidDevice.getAvailableDevices():
                devices.append({
                    'deviceName': profile['deviceName'] + "_voicekey",
                    'pad': profile['deviceName'],
                    'index': profile['index'],
                    'channels': 1,
                })

            return devices
else:
    class BaseXidVoicekeyGroup(base.BaseResponseDevice):
        # all selectors for XID voicekey nodes
        selectors = (
            # microphone
            "M", 
            # audio (left and right)
            "L", "R", 
        )


class BaseXidDevice(base.BaseDevice):
    """
    Base class for all Cedrus XID devices.
    """

    # all selectors for XID nodes
    selectors = (
        # photodiodes
        "A", "B", "C", "D", 
        # microphone
        "M", 
        # audio (left and right)
        "L", "R", 
        # response keys
        "K", 
        # scanner triggers
        "T"
    )

    def __init__(
            self, index=0
    ):
        # give error if no device connected
        if not len(self.getAvailableDevices()):
            raise ConnectionError("No Cedrus device is connected.")
        # get xid device
        self.index = index
        self.xid = pyxid2.get_xid_device(index)
        # nodes
        self.nodes = []
        # dict of responses by timestamp
        self.messages = {}
        # reset timer
        self._lastTimerReset = None
        self.resetTimer()
    
    @classmethod
    def resolve(cls, requested):
        """
        Take a value given to a device which has a BaseXidDevice as its parent and, from it, 
        find/make the associated BaseXidDevice object.

        Parameters
        ----------
        requested : str, int or BaseXidDevice
            Value to resolve
        """
        # if requested is already a handle, return as is
        if isinstance(requested, cls):
            return requested
        # try to get by name
        if isinstance(requested, str):
            pad = DeviceManager.getDevice(requested)
            # if found, return
            if pad is not None:
                return pad
        # try to get by index
        if isinstance(requested, int):
            pad = DeviceManager.getDeviceBy("index", requested, deviceClass="psychopy_cedrus.base.BaseXidDevice")
            # if found, return
            if pad is not None:
                return pad
        # if given an index of a not-yet setup device, set one up
        if requested is None or isinstance(requested, int):
            return DeviceManager.addDevice(
                deviceClass="psychopy_cedrus.base.BaseXidDevice",
                deviceName=f"XidDevice@{requested}",
                index=requested
            )
        # if still not found, raise error
        raise ManagedDeviceError(f"Could not find/create any BaseXidDevice object from the value {requested}")

    def isSameDevice(self, other):
        """
        Determine whether this object represents the same physical button box as a given other
        object.

        Parameters
        ----------
        other : BaseXidDevice, dict
            Other BaseXidDevice to compare against, or a dict of params (which much include
            `index` as a key)

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        if isinstance(other, type(self)):
            # if given another object, get index
            index = other.index
        elif isinstance(other, dict) and "index" in other:
            # if given a dict, get index from key
            index = other['index']
        else:
            # if the other object is the wrong type or doesn't have an index, it's not this
            return False

        return self.index == index

    @staticmethod
    def getAvailableDevices():
        # list devices
        devices = []
        # iterate through profiles of all serial port devices
        for i, profile in enumerate(pyxid2.get_xid_devices()):
            devices.append({
                'deviceName': profile.device_name,
                'index': i,
            })

        return devices

    def addListener(self, listener):
        """
        Add a listener, which will receive all the messages dispatched by this BaseXidDevice.

        Parameters
        ----------
        listener : hardware.listener.BaseListener
            Object to duplicate messages to when dispatched by this BaseXidDevice.
        """
        # add listener to all nodes
        for node in self.nodes:
            node.addListener(listener)

    def dispatchMessages(self):
        # poll device for messages
        self.xid.poll_for_response()
        # get all messages
        while self.xid.has_response():
            # get response
            resp = self.xid.get_next_response()
            # get time in s using defaultClock units
            resp['time'] = float(resp['time']) / 1000 + self._lastTimerReset
            # store message
            self.messages[resp['time']] = resp
            # choose object to dispatch to
            for node in self.nodes:
                # if device is 0, dispatch only to buttons
                if resp['port'] == 0 and not isinstance(node, BaseXidButtonGroup):
                    continue
                # if device is 2, it could be a photodiode or a voice key
                if resp['port'] == 2:
                    if not isinstance(node, (BaseXidPhotodiodeGroup, BaseXidVoicekeyGroup)):
                        continue
                    # these we need to distinguish from keys
                    if resp['key'] not in node.keys:
                        continue
                # dispatch to node
                message = node.parseMessage(resp)
                node.receiveMessage(message)

    def resetTimer(self, clock=logging.defaultClock):
        # send reset command
        self.xid.reset_timer()
        # store time
        self._lastTimerReset = clock.getTime(format=float)

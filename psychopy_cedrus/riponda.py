from psychopy.hardware import base, photodiode, button
from psychopy.hardware.manager import deviceManager, DeviceManager, ManagedDeviceError
from psychopy import logging, layout
import pyxid2


class RipondaPhotodiodeGroup(photodiode.BasePhotodiodeGroup):
    def __init__(self, pad, channels=1):
        # get parent
        self.parent = Riponda.resolve(pad)
        # reference self in parent
        self.parent.nodes.append(self)
        # initialise base class
        photodiode.BasePhotodiodeGroup.__init__(self, channels=channels)

    def isSameDevice(self, other):
        """
        Determine whether this object represents the same physical device as a given other
        object.

        Parameters
        ----------
        other : RipondaPhotodiodeGroup, dict
            Other RipondaPhotodiodeGroup to compare against, or a dict of params (which must include
            `index` as a key)

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        if isinstance(other, type(self)):
            # if given another RipondaPhotodiodeGroup, compare parent boxes
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
        for profile in Riponda.getAvailableDevices():
            devices.append({
                'deviceName': profile['deviceName'] + "_photodiodes",
                'pad': profile['deviceName'],
                'index': profile['index'],
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
        # send command
        self.parent.xid.con.send_xid_command(f"it{channel}{thr}")
        # dispatch
        self.dispatchMessages()
        # return True/False according to state
        return self.getState(channel)

    def resetTimer(self, clock=logging.defaultClock):
        self.parent.resetTimer(clock=clock)

    def dispatchMessages(self):
        """
        Dispatch messages from parent Riponda to this photodiode group

        Returns
        -------
        bool
            True if request sent successfully
        """
        self.parent.dispatchMessages()

    def parseMessage(self, message):
        # create PhotodiodeResponse object
        resp = photodiode.PhotodiodeResponse(
            t=message['time'], channel=message['key'], value=message['pressed'], threshold=self.getThreshold()
        )

        return resp


class RipondaButtonGroup(button.BaseButtonGroup):
    def __init__(self, pad=0, channels=7):
        # get parent
        self.parent = Riponda.resolve(pad)
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
        other : RipondaButtonGroup, dict
            Other RipondaButtonGroup to compare against, or a dict of params (which must include
            `index` as a key)

        Returns
        -------
        bool
            True if the two objects represent the same physical device
        """
        if isinstance(other, type(self)):
            # if given another RipondaButtonGroup, compare parent boxes
            other = other.parent
        elif isinstance(other, dict) and "pad" in other:
            # if given a dict, make sure we have a `port` rather than a `pad`
            other['port'] = other['pad']
        # use parent's comparison method
        return self.parent.isSameDevice(other)

    def dispatchMessages(self):
        """
        Dispatch messages from parent Riponda to this button group

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
        for profile in Riponda.getAvailableDevices():
            devices.append({
                'deviceName': profile['deviceName'] + "_buttons",
                'pad': profile['deviceName'],
                'index': profile['index'],
                'channels': 7,
            })

        return devices


class RipondaVoicekey:
    def __init__(self, *args, **kwargs):
        pass


class Riponda(base.BaseDevice):
    def __init__(
            self, index=0
    ):
        # give error if no device connected
        if not len(self.getAvailableDevices()):
            raise ConnectionError("No Cedrus Riponda response pad is connected.")
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
        Take a value given to a device which has a Riponda as its parent and, from it, 
        find/make the associated Riponda object.

        Parameters
        ----------
        requested : str, int or Riponda
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
            pad = DeviceManager.getDeviceBy("index", requested, deviceClass="psychopy_cedrus.riponda.Riponda")
            # if found, return
            if pad is not None:
                return pad
        # if given an index of a not-yet setup device, set one up
        if requested is None or isinstance(requested, int):
            return DeviceManager.addDevice(
                deviceClass="psychopy_cedrus.riponda.Riponda",
                deviceName=f"Riponda@{requested}",
                index=requested
            )
        # if still not found, raise error
        raise ManagedDeviceError(f"Could not find/create any Riponda object from the value {requested}")

    def isSameDevice(self, other):
        """
        Determine whether this object represents the same physical button box as a given other
        object.

        Parameters
        ----------
        other : Riponda, dict
            Other Riponda to compare against, or a dict of params (which much include
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
        Add a listener, which will receive all the messages dispatched by this Riponda.

        Parameters
        ----------
        listener : hardware.listener.BaseListener
            Object to duplicate messages to when dispatched by this Riponda.
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
                if resp['port'] == 0 and not isinstance(node, RipondaButtonGroup):
                    continue
                # if device is 3, dispatch only to photodiodes
                if resp['port'] == 3 and not isinstance(node, RipondaPhotodiodeGroup):
                    continue
                # if device is 2, dispatch only to voice keys
                if resp['port'] == 2 and not isinstance(node, RipondaVoicekey):
                    continue
                # dispatch to node
                message = node.parseMessage(resp)
                node.receiveMessage(message)

    def resetTimer(self, clock=logging.defaultClock):
        # send reset command
        self.xid.reset_timer()
        # store time
        self._lastTimerReset = clock.getTime(format=float)

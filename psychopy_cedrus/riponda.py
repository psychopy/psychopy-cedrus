from psychopy.hardware import base, photodiode, button
from psychopy.hardware.manager import deviceManager, DeviceManager
from psychopy import logging, layout
import pyxid2


class RipondaPhotodiodeGroup(photodiode.BasePhotodiodeGroup):
    def __init__(self, pad, channels=1):
        _requestedPad = pad
        # try to get associated riponda
        if isinstance(_requestedPad, str):
            # try getting by name
            pad = DeviceManager.getDevice(pad)
        # if still failed, make one
        if pad is None or isinstance(pad, int):
            pad = DeviceManager.addDevice(
                deviceClass="psychopy_cedrus.riponda.Riponda",
                deviceName=_requestedPad,
                index=_requestedPad
            )
        # reference self in pad
        pad.nodes.append(self)
        # initialise base class
        photodiode.BasePhotodiodeGroup.__init__(self, channels=channels)
        self.parent = pad

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

    def setThreshold(self, threshold, channels=(1, 2)):
        # store value
        self._threshold = threshold
        # convert from base 16
        thr = threshold / 255 * 100
        # send commands
        for n in channels:
            self.parent.xid.con.send_xid_command(f"it{n}{thr}")

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
        _requestedPad = pad
        # try to get associated riponda
        if isinstance(_requestedPad, str):
            # try getting by name
            pad = DeviceManager.getDevice(pad)
        # if still failed, make one
        if pad is None or isinstance(pad, int):
            pad = DeviceManager.addDevice(
                deviceClass="psychopy_cedrus.riponda.Riponda",
                deviceName=_requestedPad,
                index=_requestedPad
            )

        # reference self in pad
        pad.nodes.append(self)
        # initialise base class
        button.BaseButtonGroup.__init__(self, channels=channels)
        self.parent = pad

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
        # get xid device
        self.xid = pyxid2.get_xid_device(index)
        # nodes
        self.nodes = []
        # dict of responses by timestamp
        self.messages = {}
        # reset timer
        self._lastTimerReset = None
        self.resetTimer()

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
            time = float(resp['time']) / 1000 + self._lastTimerReset
            # store message
            self.messages[time] = resp
            print(resp)
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

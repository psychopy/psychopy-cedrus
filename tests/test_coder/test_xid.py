"""
Tests for the XID device classes, run against a fake pyxid2 device so that no Cedrus hardware is
needed. The fake device queues responses in the same form as pyxid2 does after parsing an XID
packet: a dict with `port`, `key`, `pressed` and `time` (in ms).
"""

import sys
import types

import pytest
from psychopy.hardware.manager import DeviceManager

from psychopy_cedrus import base


class FakeXid:
    """
    Stands in for a pyxid2.XidDevice.
    """
    def __init__(self, productId, deviceName):
        self.product_id = productId
        self.device_name = deviceName
        # responses which the device has sent but which haven't been polled yet
        self.incoming = []
        # responses which have been polled
        self.response_queue = []
        # commands sent to the device
        self.commands = []
        self.con = types.SimpleNamespace(send_xid_command=self._sendCommand)

    def _sendCommand(self, command, bytesExpected=0):
        self.commands.append(command)

    def send(self, port, key, pressed, time):
        """
        Simulate the device sending a response, with `time` in ms.
        """
        self.incoming.append({'port': port, 'key': key, 'pressed': pressed, 'time': time})

    def reset_timer(self):
        pass

    def query_timer(self):
        return 0

    def set_signal_filter(self, selector, holdOn, holdOff):
        pass

    def poll_for_response(self):
        self.response_queue += self.incoming
        self.incoming = []

    def has_response(self):
        return len(self.response_queue) > 0

    def get_next_response(self):
        return self.response_queue.pop(0)


# Riponda and RB both send XID packets: buttons on port 0 (with pyxid2's keymap applied), and the
# voice key and light sensor on port 2 as keys 2 and 3 (with no keymap applied)
DEVICES = {
    'riponda': {
        'productId': b"5",
        'deviceName': "Riponda Model L",
        'buttons': "psychopy_cedrus.riponda.RipondaButtonGroup",
        'voicekey': "psychopy_cedrus.riponda.RipondaSoundSensorGroup",
        'lightsensor': "psychopy_cedrus.riponda.RipondaLightSensorGroup",
    },
    'rb': {
        'productId': b"2",
        'deviceName': "Cedrus RB-740",
        'buttons': "psychopy_cedrus.rb.RBButtonGroup",
        'voicekey': "psychopy_cedrus.rb.RBSoundSensorGroup",
        'lightsensor': "psychopy_cedrus.rb.RBLightSensorGroup",
    },
}


@pytest.fixture(params=list(DEVICES))
def device(request, monkeypatch):
    """
    Connect a fake XID device, and yield its profile along with the fake pyxid2 device.
    """
    profile = DEVICES[request.param]
    xid = FakeXid(profile['productId'], profile['deviceName'])
    # make the plugin use the fake device
    fakePyxid2 = types.ModuleType("pyxid2")
    fakePyxid2.get_xid_devices = lambda: [xid]
    monkeypatch.setitem(sys.modules, "pyxid2", fakePyxid2)
    monkeypatch.setattr(base, "hasDriver", True)
    monkeypatch.setattr(base.BaseXidDevice, "_deviceCache", None)
    # don't leave the fake devices in DeviceManager for other tests
    monkeypatch.setattr(DeviceManager, "devices", {})

    yield dict(profile, xid=xid)


def addDevices(device, *kinds):
    """
    Add one device of each given kind, the same way Builder does.
    """
    return [
        DeviceManager.addDevice(
            deviceClass=device[kind], deviceName=f"test_{kind}", pad=0, channels=1
        )
        for kind in kinds
    ]

``
def test_voicekey_channel(device):
    """
    The voice key is the only channel in its group, so its responses should be on channel 0.
    """
    voicekey, = addDevices(device, 'voicekey')

    device['xid'].send(port=2, key=2, pressed=True, time=1000)
    assert voicekey.getState(0) is True
    resps = voicekey.getResponses(channel=0)
    assert len(resps) == 1
    assert resps[0].channel == 0
    assert resps[0].value is True

    device['xid'].send(port=2, key=2, pressed=False, time=1500)
    assert voicekey.getState(0) is False
    resps = voicekey.getResponses(channel=0)
    assert [resp.value for resp in resps] == [False]
    # receiving responses shouldn't create channels the group doesn't have
    assert len(voicekey.state) == 1


def test_responses_go_to_correct_group(device):
    """
    Buttons, voice key and light sensor share one device; each response should reach only its own
    group, on the right channel.
    """
    buttons, voicekey, lightSensor = addDevices(device, 'buttons', 'voicekey', 'lightsensor')

    device['xid'].send(port=0, key=0, pressed=True, time=100)
    device['xid'].send(port=2, key=2, pressed=True, time=200)
    device['xid'].send(port=2, key=3, pressed=True, time=300)

    buttonResps = buttons.getResponses()
    voicekeyResps = voicekey.getResponses()
    lightResps = lightSensor.getResponses()

    assert [(resp.channel, resp.value) for resp in buttonResps] == [(0, True)]
    assert [(resp.channel, resp.value) for resp in voicekeyResps] == [(0, True)]
    assert [(resp.channel, resp.value) for resp in lightResps] == [(0, True)]
    # device times are in ms, responses in s
    assert buttonResps[0].t == pytest.approx(0.1)
    assert voicekeyResps[0].t == pytest.approx(0.2)
    assert lightResps[0].t == pytest.approx(0.3)


def test_is_same_device(device):
    """
    The parent device should recognise each of its groups as the same physical device.
    """
    buttons, voicekey, lightSensor = addDevices(device, 'buttons', 'voicekey', 'lightsensor')
    # all groups share one parent
    assert buttons.parent is voicekey.parent is lightSensor.parent

    for group in (buttons, voicekey, lightSensor):
        assert group.parent.isSameDevice(group), type(group).__name__

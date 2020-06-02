# MS2131.py - Hologram Python SDK Huawei MS2131 modem interface
#
# Author: Hologram <support@hologram.io>
#
# Copyright 2016 - Hologram (Konekt, Inc.)
#
#
# LICENSE: Distributed under the terms of the MIT License
#

from Hologram.Network.Modem import Modem
from Hologram.Event import Event

DEFAULT_HUAWEI_TIMEOUT = 200

class Huawei_default(Modem):

    usb_ids = [('12d1', '1001'),('12d1','1003'),('12d1','101e'),('12d1','1414'),('12d1','14c6'),('12d1','1520'),('12d1','1521'),('12d1','1557')]

    def __init__(self, device_name=None, baud_rate='9600',
                 chatscript_file=None, event=Event()):

        super().__init__(device_name=device_name, baud_rate=baud_rate,
                                     chatscript_file=chatscript_file, event=event)

    def connect(self, timeout = DEFAULT_HUAWEI_TIMEOUT):
        return super().connect(timeout)

    def init_serial_commands(self):
        self.command("E0") #echo off
        self.command("+CMEE", "2") #set verbose error codes
        self.command("+CPIN?")
        self.command("+CTZU", "1") #time/zone sync
        self.command("+CTZR", "1") #time/zone URC
        #self.command("+CPIN", "") #set SIM PIN
        self.command("+CPMS", "\"ME\",\"ME\",\"ME\"")
        self.set_sms_configs()
        self.command("+CREG", "2")
        self.command("+CGREG", "2")
        self.command("+CREG?")

    # AT sockets mode is always disabled for MS2131.
    def disable_at_sockets_mode(self):
        pass

    @property
    def iccid(self):
        return self._basic_command('^ICCID?').lstrip('^ICCID: ')[:-1]

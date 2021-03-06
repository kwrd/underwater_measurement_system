from pybleno import Characteristic
import array
import struct
import sys
import traceback

from googledrive import *

from wf_receiver import receiver_run

class ReceiverCharacteristic(Characteristic):
    
    def __init__(self, uuid):
        Characteristic.__init__(self, {
            'uuid': uuid,
            'properties': ['read', 'write', 'notify'],
            'value': None
          })
          
        self._value = array.array('B', [0] * 0)
        self._updateValueCallback = None
          
    def onReadRequest(self, offset, callback):
        print('ReceiverCharacteristic - %s - onReadRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        callback(Characteristic.RESULT_SUCCESS, self._value[offset:])
    
    def onWriteRequest(self, data, offset, withoutResponse, callback):
        self._value = data
        print(data)
        if data.decode() == "save":
            save()
            print("save.....")
        else:
            receiver_run(int(data.decode()), 2.0)
        print('ReceiverCharacteristic - %s - onWriteRequest: value = %s' % (self['uuid'], [hex(c) for c in self._value]))
        print('ReceiverCharacteristic - onWriteRequest: string value = %s' % data.decode())

        if self._updateValueCallback:
            print('ReceiverCharacteristic - onWriteRequest: notifying');
            
            self._updateValueCallback(self._value)
        
        callback(Characteristic.RESULT_SUCCESS)
        
    def onSubscribe(self, maxValueSize, updateValueCallback):
        print('ReceiverCharacteristic - onSubscribe')
        
        self._updateValueCallback = updateValueCallback

    def onUnsubscribe(self):
        print('ReceiverCharacteristic - onUnsubscribe');
        
        self._updateValueCallback = None

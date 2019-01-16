import atexit

from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from renogy_rover import config


class _MockDriver:
    def __init__(self, unit):
        self.data = {
            0x107: 127,
            0x108: 2000,
            0x102: 3000,
        }
        self.unit = unit

    def read(self, address, size):
        return [self.data.get(address, 0)] * size


class _ModusDriver:
    def __init__(self, unit):
        self.client = ModbusClient(**config.serial)
        self.client.connect()
        self.unit = unit

        # Disconnect on program's exit
        atexit.register(self.client.close)

    def read(self, address, size):
        resp = self.client.read_holding_registers(address, size, unit=self.unit)
        return resp.registers


def _get_driver():
    if config.driver == 'mock':
        return _MockDriver(config.unit)
    elif config.driver == 'renogy':
        return _ModusDriver(config.unit)
    raise RuntimeError("Invalid Driver Selected")


client = _get_driver()

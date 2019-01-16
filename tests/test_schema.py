from renogy_rover.schema import Schema, Numeric


class Power(Schema):
    """Test Class"""
    battery_voltage = Numeric(0x107, 1, 0.1, unit='M')


def test_simple():
    """Basic Test"""
    simple = Power()
    assert simple.battery_voltage == 12.7
    assert simple.dump() == {'battery_voltage': 12.7}

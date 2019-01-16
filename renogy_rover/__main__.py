from renogy_rover.schema import Schema, Numeric, Property


class Power(Schema):
    battery_voltage = Numeric(0x101, 1, 0.1, unit='V')
    current_to_battery = Numeric(0x0102, 1, 0.01, unit='A')
    panel_voltage = Numeric(0x0107, 1, 0.1, unit='V')
    panel_current = Numeric(0x0108, 1, 0.01, unit='A')
    charging_power = Numeric(0x0108, 1, unit='W')
    min_volt_day = Numeric(0x010B, 1, 0.1, unit='V')
    max_volt_day = Numeric(0x010C, 1, 0.1, unit='V')

    batter_type = Property(0xE004, 1)


def main():
    foo = Power()
    # Verify read support
    # print(foo.panel_voltage, foo.panel_current, foo.current_to_battery)
    # print(foo.panel_voltage, foo.panel_current, foo.current_to_battery)
    # Verify Cache times out
    # time.sleep(11)
    # print(foo.panel_voltage, foo.panel_current, foo.current_to_battery)
    # # This is not supported, just verifying it crashes
    # foo.panel_voltage = 15
    print(foo.dump())


if __name__ == "__main__":
    main()

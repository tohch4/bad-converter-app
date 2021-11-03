#!/usr/bin/env python3

import pint

def run(temp, from_unit='', to_unit=''):
    """Convert temperatures between units.
    """
    try:
        ureg = pint.UnitRegistry() 
        original = ureg.Quantity(temp, getattr(ureg, from_unit))
        return original.to(to_unit)

    except Exception as err:
        print(err)
        return None

if __name__ == '__main__':
    print(run(25.4, 'degC', 'degF'))
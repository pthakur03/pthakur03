import sys
import time

"""
Class initialization to standardize volume elements and create OOP attributes.
"""


class volElement:
    def __init__(self, volume, pressure):
        self.volume = volume
        self.pressure = pressure

    """
    Euler's integration built off of passing in references to helper methods on object attributes.
    """

    def updatePressure(self, roc):
        self.pressure = self.pressure + (0.001 * roc)  # Change in t is 0.001 for this simulation


"""
Class initialization to standardize orifice elements and create OOP attributes.
"""


class orifice:
    def __init__(self, start, end, g):
        self.event_name = None
        self.start = start
        self.end = end
        if (g == 0) or (g == 1):
            self.g = g

    """
    Setter method for updating G (conductance) value attribute for orifice.
    """

    def setConductance(self, event_name, new):
        self.event_name = event_name
        if (new != self.g) and (new == 0 or new == 1):
            self.g = new


"""
Method to calculate mass flow rate based on staring and ending pressure elements of two volElements 
along with conductance value of respective orifice. 
"""


def massFlowRate(valve):
    return valve.g * (valve.start.pressure - valve.end.pressure)


"""
Method to calculate rate of change in pressure based on passed in volume element 
and open valves with at least one laminar flow element.
Arguments designed to fit specifications for given simulation but can 
easily be modified to become universally standardized.
"""


def rocPressure(vol, valve1, valve2):
    beta = 10
    if valve1 is None:
        return (beta / vol.volume) * massFlowRate(valve2) * -1
    elif valve2 is None:
        return (beta / vol.volume) * massFlowRate(valve1)
    else:
        return (beta / vol.volume) * (massFlowRate(valve1) - massFlowRate(valve2))


"""
Method to start timer with simulation specific event and print settings. 
Driver for objects and methods throughout entire file. 
!!! Timer settings beyond capabilities of Python interpreter using only standard libraries
Not realistic in terms of time but realistic in simulation -> Running on CPU with C rather than
interpreter or VM in Python resolves issue. 
"""


def timer(sim):
    for i in range(sim * 1000 + 1):
        s, ms = divmod(i, 1000)
        s_ms_format = '{:02d}:{:03d}'.format(s, ms)
        if s == 1:
            if ms == 0:
                fillValve.setConductance("fill_on", 1)
                print("{0}: event {1}\n".format(s_ms_format, fillValve.event_name))
                continue
            accumulator.updatePressure(rocPressure(accumulator, None, fillValve))
            cylinder.updatePressure(rocPressure(cylinder, fillValve, None))
            print("{0}: accumulator {1:.5f} cylinder {2:.5f}\n".format(s_ms_format, accumulator.pressure,
                                                                       cylinder.pressure))
            continue
        elif s == 4:
            if ms == 0:
                fillValve.setConductance("fill_off", 0)
                print("{0}: {1}\n".format(s_ms_format, fillValve.event_name))
                continue
            print("{0}: accumulator {1:.5f} cylinder {2:.5f}\n".format(s_ms_format, accumulator.pressure,
                                                                       cylinder.pressure))
            continue
        elif s == 8:
            if ms == 0:
                drainValve.setConductance("drain_on", 1)
                print("{0}: {1}\n".format(s_ms_format, drainValve.event_name))
                continue
            cylinder.updatePressure(rocPressure(cylinder, None, drainValve))
            print("{0}: accumulator {1:.5f} cylinder {2:.5f}\n".format(s_ms_format, accumulator.pressure,
                                                                       cylinder.pressure))
        else:
            print("{0}: accumulator {1:.5f} cylinder {2:.5f}\n".format(s_ms_format, accumulator.pressure,
                                                                       cylinder.pressure))
        time.sleep(1 / 1000)
        i += 1
    print("Simulation Complete.")


"""
Main method and launch file with object initialization based on given parameters.
"""


def main():
    inp = input("Initialize and run simulation for ___ seconds: ")
    x = int(inp)
    timer(x)


if __name__ == "__main__":
    accumulator = volElement(100, 1000.0)
    cylinder = volElement(1, 0.0)
    tank = volElement(sys.float_info.max, 0.0)
    fillValve = orifice(accumulator, cylinder, 0)
    drainValve = orifice(cylinder, tank, 0)
    main()

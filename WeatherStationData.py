import datetime
import math


# Class blueprint 'WsData' is created 
class WsData:

    # Initialization is defined, with parameters for other methods
    def __init__(self, day, month, year, h_temp, l_temp, precip, station):
        self.h_temp = float(h_temp)
        self.l_temp = float(l_temp)
        self.precip = float(precip)
        self.dt = self.__create_date__(day, month, year)
        self.station = station

    # Create data method defines and type casts the day, month, and year as attributes
    # This is helpful when the "day of year" is needed in the exoatmospheric radiation calculation
    def __create_date__(self, day, month, year):
        d = int(day)
        m = int(month)
        y = int(year)

        return datetime.date(y, m, d)

    # Mean temp is required for the hargreaves equation. (High temp + Low temp) / 2
    # The "convert_celsius" method is applied here as well.
    def mean_temp(self):
        return (self.convert_celsius(self.h_temp) + self.convert_celsius(self.l_temp)) / 2

    # Main equation. Takes the station latitude as a required parameter.
    def hargreaves(self, lat):
        k1 = 0.0023  # First constant
        k2 = 17.8  # Second constant
        eto = (k1 * (self.convert_celsius(self.h_temp) - self.convert_celsius(self.l_temp)) ** .5 * (
                    (self.mean_temp()) + k2) * self.__ra__(lat)) / 2.45  # Exoatmospheric radiation constant.
        return eto * .03937  # mm to inches conversion

    # Exoatmospheric radiation equation, sub equation needed for hargreaves.
    def __ra__(self, lat):
        k3 = 24 / math.pi # equation constant
        gsc = 4.92  # solar constant
        dr = 1 + 0.033 * math.cos((2 * math.pi / 365) * self.dt.timetuple().tm_yday)  # Inverse relative distance factor
        sol_dec = 0.409 * math.sin(
            (2 * math.pi / 365) * self.dt.timetuple().tm_yday - 1.39)  # Solar declination, radians
        fi = lat * math.pi / 180  # convert degrees to radians for equation
        ws_sha_rads = math.acos(-math.tan(fi) * math.tan(sol_dec))  # Sunset hour angle, radians
        return k3 * gsc * dr * (
                    ws_sha_rads * math.sin(fi) * math.sin(sol_dec) + math.cos(fi) * math.cos(sol_dec) * math.sin(
                ws_sha_rads))

    # Equation to convert station output of fahrenheit to celsius
    def convert_celsius(self, fahrenheit):
        celsius = (fahrenheit - 32) * (5 / 9)
        return celsius

    # main method to print out correct data
    def text_line(self, lat):
        try:
            rslt = f'{self.dt.timetuple().tm_yday}, {self.h_temp}, {self.l_temp}, {self.precip}, -99.00, {round(self.hargreaves(lat), 2)}\n'
        except TypeError:
            print(f'Error in {self.station} on {self.dt}')
            exit()

        return rslt

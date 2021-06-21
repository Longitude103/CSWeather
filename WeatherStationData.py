import datetime
import math




class WsData:
    def __init__(self, day, month, year, h_temp, l_temp, precip, station):
        self.h_temp = float(h_temp)
        self.l_temp = float(l_temp)
        self.precip = float(precip)
        self.dt = self.__create_date__(day, month, year)
        self.station = station

    def __create_date__(self, day, month, year):
        d = int(day)
        m = int(month)
        y = int(year)

        return datetime.date(y, m, d)

    def mean_temp(self):
        return (self.convert_celsius(self.h_temp) + self.convert_celsius(self.l_temp)) / 2


    def hargraves(self, lat):
        k1 = 0.0023  # First constant
        k2 = 17.8  # Second constant
        eto = (k1 * (self.convert_celsius(self.h_temp) - self.convert_celsius(self.l_temp)) ** .5 * ((self.mean_temp()) + k2) * self.__ra__(lat)) / 2.45  # Exoatmospheric radiation
        return eto * .03937 # mm to inches conversion

    def __ra__(self, lat):
        k3 = 24 / math.pi
        gsc = 4.92  # solar constant
        dr = 1 + 0.033 * math.cos((2 * math.pi / 365) * self.dt.timetuple().tm_yday)  # Inverse relative distance factor
        sol_dec = 0.409 * math.sin((2 * math.pi / 365) * self.dt.timetuple().tm_yday - 1.39)  # Solar declination, radians
        fi = lat * math.pi / 180 # convert degrees to radians for equation
        ws_sha_rads = math.acos(-math.tan(fi) * math.tan(sol_dec))  # Sunset hour angle, radians
        return k3 * gsc * dr * (ws_sha_rads * math.sin(fi) * math.sin(sol_dec) + math.cos(fi) * math.cos(sol_dec) * math.sin(ws_sha_rads))

    def convert_celsius(self, fahrenheit):
        celsius = (fahrenheit - 32) * (5 / 9)
        return celsius

    def text_line(self, lat):
        try:
            rslt = f'{self.dt.timetuple().tm_yday}, {self.h_temp}, {self.l_temp}, {self.precip}, -99.00, {round(self.hargraves(lat),2)}\n'
        except TypeError:
            print(f'Error in {self.station} on {self.dt}')
            exit()

        return rslt

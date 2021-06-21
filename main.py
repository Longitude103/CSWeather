import calendar
import os

from WeatherStationData import WsData


# Station Info below as follows position 0 = lat, 1 = long, 2 = elevation (ft), 3 = NWScode, 4 = station_code
station_info = {'agate': [42.42, -103.73, 4669, 'c250030', 'AGAT'], 'akron': [40.15, -103.15, 4541, 'c050109', 'AKRN'],
                'alliance': [42.1, -102.88, 3993, 'c250130', 'ALI1'], 'big_springs': [41.05, -102.13, 3678, 'c250865', 'BIGS'],
                'bridgeport': [41.67, -103.1, 3665, 'c251145', 'BRDG'], 'chadron': [42.82, -103.0, 3510, 'c251575', 'CHAD'],
                'curtis': [40.67, -100.48, 2719, 'c252100', 'CURT'], 'gordon': [42.88, -102.2, 3701, 'c253355', 'GORD'],
                'harrisburg': [41.63, -103.95, 4550, 'c253605', 'HRSB'], 'harrison': [42.68, -103.88, 4849, 'c253615', 'HARR'],
                'kimball': [41.27, -103.65, 4760, 'c254440', 'KMBL'], 'oshkosh': [41.42, -102.33, 3379, 'c256385', 'OSHK'],
                'scottsbluff': [41.87, -103.6, 3944, 'c257665', 'SCTB'], 'sidney': [41.2, -103.02, 4321, 'c257830', 'SDN2']}


# Main function that loads and formats raw .csv file
def cs_weather():
    file_path = "C:/Users/Jason/Desktop/weather_data_master/"
    raw_list = os.listdir(file_path)
    file_list = []
    for item in raw_list:
        if item[-3:] == 'csv':
            file_list.append(item)

    for fl in file_list:
        yr_counter = 1953

        with open(os.path.join(file_path, fl), 'r') as f:
            f.readline()
            f.readline()

            annual_data_list = []
            for line in f:
                raw_line_parts = line.split(',')

                line_parts = []
                for p in raw_line_parts:
                    line_parts.append(p.strip())

                if int(line_parts[2]) != yr_counter:
                    save_file(annual_data_list,yr_counter,fl[:-4], file_path)
                    yr_counter += 1
                    annual_data_list = []

                annual_data_list.append(
                    WsData(line_parts[1], line_parts[0], line_parts[2], line_parts[4], line_parts[5], line_parts[6], fl[:-4]))

            save_file(annual_data_list, yr_counter, fl[:-4], file_path)


# Function that takes four parameters and outputs the text_line for each year per station
def save_file(data_list, yr, station, file_path):
    if calendar.isleap(yr):
        dc = 366
    else:
        dc = 365
    if station == 'akron':
        state = "CO"
    else:
        state = "NE"

    header = f'{station.upper()}                   {state}  {station_info[station][3]}   {yr}\n' \
             f'  1  1   {dc}   LAT=  {station_info[station][0]}   LONG=  {station_info[station][1]}   ELEV(ft)=   {station_info[station][2]}.\n' \
             f'DOY,    TMAX,    TMIN,  PRECIP,    EVAP,   ETRGH\n'

    with open(os.path.join(file_path, "results", f'{station_info[station][4]}{yr}.WEA'), 'w') as f:
        f.write(header)

        for d in data_list:
            f.write(d.text_line(station_info[station][0]))


if __name__ == '__main__':
    cs_weather()

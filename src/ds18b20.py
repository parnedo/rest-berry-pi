from glob import glob
import re

class DS18B20:
    def __init__(self):
        self.path='/sys/bus/w1/devices/'
        self.sensors = [d for d in glob(self.path+"/*") if '28' in d]
        self.temp_rexp = re.compile('.*YES.*t=(\d+)')

    def read(self):
        result = []
        for s in self.sensors:
            sensor_value = {'name':s.split('/')[-1], 'temperature': None}
            f = open(s+'/w1_slave', 'r')
            lines = f.readlines()
            f.close()
            one_line = ''.join(lines).replace('\n','')
            match = self.temp_rexp.match(one_line)
            if match != None:
                temp_string = match.groups(0)[0]  
                sensor_value['temperature'] = float(temp_string) / 1000.0
            result.append(sensor_value)
        return result

if __name__ == "__main__":
    print DS18B20().read()


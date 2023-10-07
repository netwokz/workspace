import clr  # package pythonnet, not clr
import shutil

# openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
openhardwaremonitor_hwtypes = ['Mainboard', 'SuperIO', 'CPU',
                               'RAM', 'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']
cputhermometer_hwtypes = ['Mainboard', 'SuperIO', 'CPU',
                          'GpuNvidia', 'GpuAti', 'TBalancer', 'Heatmaster', 'HDD']
openhardwaremonitor_sensortypes = ['Voltage', 'Clock', 'Temperature', 'Load',
                                   'Fan', 'Flow', 'Control', 'Level', 'Factor', 'Power', 'Data', 'SmallData']
cputhermometer_sensortypes = [
    'Voltage', 'Clock', 'Temperature', 'Load', 'Fan', 'Flow', 'Control', 'Level']


def initialize_openhardwaremonitor():
    file = 'C:\\Users\\netwokz\\Documents\\CODE\\workspace\\python\\statistics\\OpenHardwareMonitorLib.dll'
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    handle.MainboardEnabled = True
    handle.CPUEnabled = True
    handle.RAMEnabled = True
    handle.GPUEnabled = True
    handle.HDDEnabled = True
    handle.Open()
    return handle


def fetch_stats(handle):
    for i in handle.Hardware:
        i.Update()
        for sensor in i.Sensors:
            parse_sensor(sensor)
            print(f"Sensor: {sensor.Name}")
        for j in i.SubHardware:
            j.Update()
            for subsensor in j.Sensors:
                parse_sensor(subsensor)
                print(subsensor)


def parse_sensor(sensor):
    if sensor.Value is not None:
        if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
            sensortypes = openhardwaremonitor_sensortypes
            hardwaretypes = openhardwaremonitor_hwtypes
            hardwaretypes = openhardwaremonitor_hwtypes
        else:
            return

        if sensor.SensorType == sensortypes.index('Temperature'):
            print(u"%s %s Temperature Sensor #%i %s - %s\u00B0C" %
                  (hardwaretypes[sensor.Hardware.HardwareType], sensor.Hardware.Name, sensor.Index, sensor.Name, sensor.Value))


if __name__ == "__main__":

    HardwareHandle = initialize_openhardwaremonitor()
    fetch_stats(HardwareHandle)

from influxdb_client import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException
from datetime import datetime, timezone

"""
Define credentials
"""
my_url = "https://influx.computeerror.com/"
my_token = "Pt7t1hM2DfVtaa0yXGWZpD6vImylaJC8aIFUEYOC6ISVJeDRlw4Luvq2gqLDu-1vVft_GGe1_J2xToWkuhVRxg=="
my_org = "home-server"
my_bucket = "bucket01"

dt_format = "%m/%d/%Y %I:%M%p"

error_permissions = f"The specified token doesn't have sufficient credentials to read from '{my_bucket}' or specified bucket doesn't exists."


def check_connection():
    """Check that the InfluxDB is running."""
    print("> Checking connection ...", end=" ")
    client.api_client.call_api('/ping', 'GET')
    print("ok")


def check_query():
    """Check that the credentials has permission to query from the Bucket"""
    print("> Checking credentials for query ...", end=" ")
    try:
        client.query_api().query(
            f"from(bucket:\"{my_bucket}\") |> range(start: -1m) |> limit(n:1)", my_org)
        print()

        """
        Query: using Table structure
        """
        tables = client.query_api().query('from(bucket:"bucket01") |> range(start: -10m) |> filter(fn: (r) => r["_measurement"] == "sensors")\
                                           |> filter(fn: (r) => r["_field"] == "temp_input")\
                                           |> filter(fn: (r) => r["chip"] == "coretemp-isa-0000")\
                                           |> filter(fn: (r) => r["feature"] == "package_id_0")\
                                           |> filter(fn: (r) => r["host"] == "pve")\
                                           |> last()')

        for table in tables:
            count = 0
            # print(table)
            for record in table.records:
                # print(record.values)
                print(record["_time"])
                print(record["feature"])
                print(record["_value"])
                # print(type(record))
                count += 1
                # for item in record:
                #     print(item)
    except ApiException as e:
        # missing credentials
        if e.status == 404:
            raise Exception(error_permissions) from e
        raise
    # print("ok")


def get_cpu_temp():
    try:
        tables = client.query_api().query('from(bucket:"bucket01")\
                                           |> range(start: -10m)\
                                           |> filter(fn: (r) => r["_measurement"] == "sensors")\
                                           |> filter(fn: (r) => r["_field"] == "temp_input")\
                                           |> filter(fn: (r) => r["host"] == "pve")\
                                           |> last()')

        count = 0
        for table in tables:
            for record in table.records:
                if (record["feature"] == "package_id_0"):
                    time = format_datetime(record["_time"])
                    print(
                        f'{time}: Proxmox CPU0 - {format_temp(record["_value"])}')
                if (record["feature"] == "package_id_1"):
                    time = format_datetime(record["_time"])
                    print(
                        f'{time}: Proxmox CPU1 - {format_temp(record["_value"])}')
    except ApiException as e:
        # missing credentials
        if e.status == 404:
            raise Exception(error_permissions) from e
        raise


def get_outside_temp():
    try:
        tables = client.query_api().query('from(bucket:"home_assistant")\
                                           |> range(start: -10m)\
                                           |> filter(fn: (r) => r["friendly_name"] == "Outside Temperature")\
                                           |> filter(fn: (r) => r["_field"] == "value")\
                                           |> filter(fn: (r) => r["_measurement"] == "°F")\
                                           |> last()')

        for table in tables:
            for record in table.records:
                time = format_datetime(record["_time"])
                print(
                    f'{time}: Outside Temp - {format_temp(record["_value"])}')
    except ApiException as e:
        # missing credentials
        if e.status == 404:
            raise Exception(error_permissions) from e
        raise


def get_openweather_temp():
    try:
        tables = client.query_api().query('from(bucket:"home_assistant")\
                                           |> range(start: -15m)\
                                           |> filter(fn: (r) => r["friendly_name"] == "OpenWeatherMap Temperature")\
                                           |> filter(fn: (r) => r["_field"] == "value") \
                                           |> filter(fn: (r) => r["_measurement"] == "°F")\
                                           |> last()')

        for table in tables:
            for record in table.records:
                # print(record)
                time = format_datetime(record["_time"])
                print(
                    f'{time}: Openweather Temp - {format_temp(record["_value"])}')
    except ApiException as e:
        # missing credentials
        if e.status == 404:
            raise Exception(error_permissions) from e
        raise


def check_write():
    """Check that the credentials has permission to write into the Bucket"""
    print("> Checking credentials for write ...", end=" ")
    try:
        client.write_api(write_options=SYNCHRONOUS).write(
            my_bucket, my_org, b"")
    except ApiException as e:
        # bucket does not exist
        if e.status == 404:
            raise Exception(f"The specified bucket does not exist.") from e
        # insufficient permissions
        if e.status == 403:
            raise Exception(
                f"The specified token does not have sufficient credentials to write to '{my_bucket}'.") from e
        # 400 (BadRequest) caused by empty LineProtocol
        if e.status != 400:
            raise
    print("ok")


def format_datetime(utc_dt):
    local_time = utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=None)
    # return datetime.strptime(local_time,dt_string)
    return datetime.strftime(local_time, dt_format)


def format_temp(temp):
    return f"{temp:.0f}"


with InfluxDBClient(url=my_url, token=my_token, org=my_org) as client:
    check_connection()
    get_cpu_temp()
    get_outside_temp()
    get_openweather_temp()
    # check_write()
    pass

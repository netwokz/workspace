import speedtest

test = speedtest.Speedtest()

print('Loading server list')
test.get_servers()

print('Choosing best server')
best_server = test.get_best_server()

print(f"Found: {best_server['host']} located in {best_server['name']}")
print('Performing download test...')
download_result = test.download()

print('Performing upload test...')
upload_result = test.upload()
ping_result = test.results.ping

print(f'Download: {download_result / 1024 /1024:.2f} Mbps')
print(f'Upload: {upload_result / 1024 /1024:.2f} Mbps')
print(f'Ping: {ping_result:.0f} ms')
from dotenv import dotenv_values


config = dotenv_values(
    "C:\\Users\\deanejst\\Documents\\CODE\\workspace\\temp\\.env")

print(config.get('username'), config.get('password'))

from environs import Env

env = Env()

env.read_env()

CLIENT_ID = env('CLIENT_ID')
CLIENT_SECRET = env('CLIENT_SECRET')
DOMAIN = env('DOMAIN')

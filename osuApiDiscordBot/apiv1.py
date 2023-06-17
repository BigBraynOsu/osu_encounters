from ossapi import OssapiV1
from decouple import config

apikey = OssapiV1(config('OSU_API_KEY'))
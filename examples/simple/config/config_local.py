enable_calllimit = False

PORT = 8000

workers = 1
# max_requests = 2
# max_requests_jitter = 1
# preload_app = False

# keepalive = 2

timeout = 100

# accesslog='logs/access.log'
# errorlog='logs/error.log'

# accesslog='logs/faccess.log'
# errorlog='logs/ferror.log'
APP_NAME = 'simple'
# REGISTER_AT_EUREKA = True
# EUREKA_SERVER = "http://127.0.0.1:7001/eureka/"

preload_app = True

ENABLE_LIVENESS_PROB = False
LIVENESS_PROB = {
    "initialDelaySeconds": 2,
    "periodSeconds": 5,
    "timeoutSeconds": 1,
    "failureThreshold": 3,
}

# REDIS = {
#     'host': 'localhost',
#     'port': 6379,
# }

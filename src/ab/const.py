
class ErrorCode:
    # 定义错误码和对应的错误描述
    ERRORS = {
        5000: "lack of API definition for: ",
        5001: "lack of parameters: ",
        5002: "file doesn't exist: ",
        5003: "file size is too large: ",
        5004: "exceed the request limit: ",
        5005: "the server is overloaded, please try again later.",
    }

    @classmethod
    def get_description(cls, code):
        """根据错误码获取错误描述"""
        return cls.ERRORS.get(code, "unknown error.")


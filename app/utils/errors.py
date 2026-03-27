class AppError(Exception):
    def __init__(self, message, status_code=400, code="app_error", details=None):
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details
        super().__init__(message)

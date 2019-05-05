class Error(Exception):
    """Base class for other exceptions"""
    pass


class BackupExecutionError(Error):
    """Raised when the SCP backup failed"""
    pass

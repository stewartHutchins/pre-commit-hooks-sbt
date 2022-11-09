class FailedCommandError(ValueError):
    pass


class LspRunnerError(FailedCommandError):
    pass


class ShellRunnerError(FailedCommandError):
    pass

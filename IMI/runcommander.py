from ast import match_case
from .imimessage import JOB, ExecJob, RunCmd


def commandSetter(ejob:ExecJob) -> list[RunCmd]:
    if ejob.Job == JOB.TM_STRAIGHT:
        runcmds = [RunCmd.STRAIGHT] * ejob.Argn
    elif ejob.Job == JOB.TEST_SENSORS:
        runcmds = [RunCmd.CHECK_SNSR, RunCmd.ENDLESS]
    else:
        runcmds = [RunCmd.STOP, RunCmd.ENDLESS]
    return runcmds

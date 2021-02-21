import subprocess, time


def runNebula(threadName, lineCallback, executable, config):

    shell = True

    count = 0
    popen = subprocess.Popen([executable, "--config", config], shell=shell, stdout=subprocess.PIPE)
    for line in iter(popen.stdout.readline, ''):
            lineCallback(line)
    popen.wait()
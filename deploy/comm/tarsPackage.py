#!/usr/bin/python
# encoding: utf-8
import tarsLog
import shutil
import os
import tarfile
import sys
import stat
from tarsUtil import *
log = tarsLog.getLogger()
tarsDeploy = "/usr/local/app/tars"
tarsDeployFrameBasicServerList = ["tarsregistry", "tarsnode", "tarsAdminRegistry", "tarspatch","tarsconfig"]
tarsDeployFrameCommServerList = ["tarsnotify", "tarsstat", "tarsproperty", "tarsquerystat", "tarsqueryproperty", "tarslog", "tarsauth"]
baseDir = getBaseDir()
def do():
    log.infoPrint("package tarsnode start ...")
    packageNodeServer()
    log.infoPrint("package tarsnode success ")

    return

def getDBDir():
    dbDir = baseDir+"/framework/sql/"
    return dbDir

def tar(fname):
    t = tarfile.open(fname + ".tar.gz", "w:gz")
    for root, dir, files in os.walk(fname):
        print root, dir, files
        for file in files:
            fullpath = os.path.join(root, file)
            t.add(fullpath)
    t.close()

def packageNodeServer():
    server = "tarsnode"
    srcDir = "{}/framework/build/deploy/{}".format(baseDir,server)
    confDir = "{}/framework/deploy/{}".format(baseDir,server)    
    dstDir = "{}/framework/build/tmp/{}".format(baseDir,server)
    log.infoPrint(" deploy {} start srcDir is {} , confDir is {} , dstDir is {}  ".format(server,srcDir,confDir,dstDir))
    copytree(srcDir,dstDir)
    copytree(confDir,dstDir)
    updateNodeConf(dstDir,server)
    os.chmod(dstDir+"/util/start.sh",stat.S_IXGRP)
    tar(dstDir)
    log.infoPrint(" package {}  sucess".format(server))
    return

def updateNodeConf(dstDir,server):
    localIp = getLocalIp()
    replaceConf("{}/conf/tars.{}.config.conf".format(dstDir, server), "192.168.2.131", localIp)
    replaceConf("{}/util/execute.sh".format(dstDir, server), "registry.tars.com", localIp)
    return

def packageFrameServer():
    buildDir = "{}/framework/build".format(baseDir)
    return

def updateConf(server):
    mysqlHost = getCommProperties("mysql.host")
    localIp = getLocalIp()
    replaceConf("/usr/local/app/tars/{}/conf/tars.{}.config.conf".format(server,server),"localip.tars.com",localIp)
    replaceConf("/usr/local/app/tars/{}/conf/tars.{}.config.conf".format(server, server), "192.168.2.131", localIp)
    replaceConf("/usr/local/app/tars/{}/conf/tars.{}.config.conf".format(server, server), "db.tars.com", mysqlHost)
    replaceConf("/usr/local/app/tars/{}/conf/tars.{}.config.conf".format(server, server), "registry.tars.com", localIp)
    replaceConf("/usr/local/app/tars/{}/conf/tars.{}.config.conf".format(server, server), "10.120.129.226", localIp)
    if "tarsnode" == server:
        replaceConf("/usr/local/app/tars/{}/util/execute.sh".format(server, server), "registry.tars.com", localIp)
    return

if __name__ == '__main__':
    pass
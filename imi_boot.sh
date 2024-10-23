#!/usr/bin/env bash

# TODO:mainを抜けてもbootからやり直せるようにしたい。daemonモードでもmainを拔けたらもう一度続けるのかbootに戻るのか選べるようにしたい。
#### LOCKING START ####
# LOCK SETTING 
LOCKFILE_NAME="imi_main.lock"
LOCKFILE_DIR="/run/lock/imai"
LOCKFILE_PATH="${LOCKFILE_DIR}/${LOCKFILE_NAME}"
DAEMON_NAME="imi_main.daemon"
DAEMONFILE_DIR="/run/lock/imai"
DAEMONFILE_PATH="${DAEMONFILE_DIR}/${DAEMON_NAME}"

# LOCK DIR and FILE CREATE
if [ ! -d $LOCKFILE_DIR ]; then
    mkdir $LOCKFILE_DIR
fi
if [ ! -f $LOCKFILE_PATH ]; then
    touch $LOCKFILE_PATH
fi 
#
# DAEMON DIR and FILE CREATE
if [ ! -d $DAEMONFILE_DIR ]; then
    mkdir $DAEMONFILE_DIR
fi
if [ ! -f $DAEMONFILE_PATH ]; then
    touch $DAEMONFILE_PATH
fi 

SCRIPT_DIR=$(cd $(dirname $0); pwd)

#### LOG SETTING START
LOGFILE_NAME="imilog.txt"
LOGDIR_NAME="log"
LOGFILE_PATH="${SCRIPT_DIR}/${LOGDIR_NAME}/${LOGFILE_NAME}"
TIMESTMPS=$(date "+%Y/%m/%d-%H:%M:%S")
LOGSTART="${TIMESTMPS} #### BOOT UP START ####"
#### LOG SETTING END

#### BOOT PY SETTING
BOOTPY_NAME="imi_boot.py"
BOOTPY_PATH="${SCRIPT_DIR}/${BOOTPY_NAME}"
PYTHON_BIN="${SCRIPT_DIR}/.venv/bin/python"

#### MAIN PY SETTING
MAIN_PY_USER='imai'
MAINPY_NAME="imi_main.py"
MAINPY_PATH="${SCRIPT_DIR}/${MAINPY_NAME}"

#### BOOT SCRIPT EXEC START ####
if [ ! -f $LOGFILE_PATH ]; then
    touch $LOGFILE_PATH
fi
echo $LOGSTART >> $LOGFILE_PATH

# EXEC
while true
do
    echo "#### EXEC BOOT PY ####" >> $LOGFILE_PATH
    $PYTHON_BIN $BOOTPY_PATH
    return_boot_py=$?

    # LOG BOOT PY
    TIMESTMPE=$(date "+%Y/%m/%d-%H:%M:%S")
    LOGEND="${TIMESTMPE}: #### BOOT UP END ####"
    echo $LOGEND >> $LOGFILE_PATH

    ## LOCK FILE DELETE
    if [ -f $LOCKFILE_PATH ]; then
        rm $LOCKFILE_PATH
    fi 
    #### LOCK END ####
    if [ $return_boot_py -ne 0 ]; then
        # EXEC 
        echo "#### EXIT ALL ####" >> $LOGFILE_PATH
        # LOG EXIT 
        TIMESTMPE=$(date "+%Y/%m/%d-%H:%M:%S")
        EXEITLOG="${TIMESTMPE}: #### IMI SERVICE END ####"
        echo $EXEITLOG >> $LOGFILE_PATH
        ## DAEMON FILE DELETE
        if [ -f $DAEMONFILE_PATH ]; then
            rm $DAEMONFILE_PATH
        fi 
    else
        echo "#### EXEC MAIN ####" >> $LOGFILE_PATH
        sudo -u $MAIN_PY_USER $PYTHON_BIN $MAINPY_PATH
        return_main_py=$?
        TIMESTMPE=$(date "+%Y/%m/%d-%H:%M:%S")
        MNEXEITLOG="${TIMESTMPE}: #### IMI SERVICE END ####"
        echo $MNEXEITLOG>> $LOGFILE_PATH
        # force end
        if [ $return_main_py -ne 0 ]; then
            break
        fi
    fi
done
echo "EXIT LOOP"


# imi_boot.pyを実行
# imi_boot.pyはipアドレスとLEDとディスプレイを制御。次に移行
# imi_boot.pyが成功したら、ロックを解除してimi_main.pyを実行
# imi_boot.pyが失敗したら、ロックを解除して終了
# 
# 

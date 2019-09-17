#!/bin/bash
list="auth autotest extention flow interface message public tcdevices project jobs"

declare -A map=(["auth"]="9020" ["autotest"]="9022" ["extention"]="9024" ["flow"]="9026" ["interface"]="9028" ["message"]="9030" ["public"]="9034" ["tcdevices"]="9036" ["project"]="9032" ["jobs"]="9038")

start_apps(){
    echo Start all apps of tcloud !
    for key in ${!map[@]} ;
    do
        echo start $key : ${map[$key]}
        nohup python  -m apps.$key.run >logs/$key.log 2>&1 &
    done
}

stop_apps(){
    echo Stop all apps of tcloud !
    for key in ${!map[@]} ;
    do
        echo stop $key : ${map[$key]}
        pid_app=$(netstat -alnp | grep ${map[$key]} | awk '{print $7}' | awk -F '/' '{print $1}')
        if [[ $pid_app != '' ]] ; then
            echo stop $key with pid : $pid_app
            kill -9 $pid_app
        fi
    done
}

if [[ $1 = "stop" ]] ; then
    stop_apps
else
    start_apps
fi

# ************************************************************************
#    > File Name: log_handler.sh
#    > Author: LinuxStudy
#    > Mail: 15829237116@163.com 
#    > Created Time: Wed 30 Oct 2019 07:43:24 AM PDT
# ************************************************************************
#!/bin/bash 
set -x
log_array=($(ls -t `find /var/log/tmp_test -name '*log*'`))
log_len=$((${#log_array[@]}-1))
log_index=0
for log in ${log_array[@]}
    do
       log_mtime=`stat -c %Y $log`
       last_time=`date -d $1 +%s`
       echo $last_time
       if (($log_mtime-$last_time<0));then
           echo $log_index
           del_array=${log_array[@]:$log_index:$log_len}
           echo "log is old!"
           break 
       fi
       log_index=$((log_index+1))
    done
rm -fr $del_array
echo $?

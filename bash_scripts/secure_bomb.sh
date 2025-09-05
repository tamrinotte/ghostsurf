#!/bin/bash

set -euo pipefail # Add -x option to enable execution tracking (good for debugging).

main () {
    drop_caches
    wipe_memory
}

drop_caches() {
	swapoff -a 
	swapon -a 

    # Drop caches
    echo 1024 > /proc/sys/vm/min_free_kbytes
    echo 3  > /proc/sys/vm/drop_caches
    echo 1  > /proc/sys/vm/oom_kill_allocating_task
    echo 1  > /proc/sys/vm/overcommit_memory
    echo 0  > /proc/sys/vm/oom_dump_tasks
}

wipe_memory() {
    sdmem -fv
}

main
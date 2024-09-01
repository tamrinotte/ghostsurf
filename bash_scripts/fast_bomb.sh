#!/bin/bash

main () {
    # The function which runs the entire script. Hint: This scripts protects the user from cold boot attacks.

    drop_caches  
    wipe_memory
}

drop_caches() {
    # A function which drops caches
    
    # Disabling all devices and files for paging and swapping 
	swapoff -a 

    # Enabling all devices and files for paging and swapping
	swapon -a 

    # Dropping caches
    echo 1024 > /proc/sys/vm/min_free_kbytes
    echo 3  > /proc/sys/vm/drop_caches
    echo 1  > /proc/sys/vm/oom_kill_allocating_task
    echo 1  > /proc/sys/vm/overcommit_memory
    echo 0  > /proc/sys/vm/oom_dump_tasks
}

wipe_memory() {
    # A function which wipes the memory securely

    # Wiping memory securely
    sdmem -fllv
}

main
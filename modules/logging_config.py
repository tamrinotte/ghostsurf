# This Python file uses the following encoding: utf-8

# MODULES AND LIBRARIES
from logging import (
    basicConfig,
    DEBUG,
    disable,
    CRITICAL,
    debug, 
    info,
    warning,
    error,
    critical, 
)

# Doing the basic configuration for the debugging feature
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
disable(CRITICAL)
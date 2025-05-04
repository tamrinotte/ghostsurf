# MODULES AND LIBRARIES
from logging import (
    basicConfig,
    DEBUG,
    disable,
    CRITICAL,
    debug, # To log internal processes like the URL for a deal or the number of deals awaiting payment.
    info, # To inform developers about what just happened. Ex: "User has been registered successfully!"
    warning, # To inform developers about where something isn't ideal. Ex: email duplication, or a user already registered with a customer ID
    error, # To log errors and critical issues such as exceptions that may arise during the registration process or form validation failures.
    critical, 
)

# Doing the basic configuration for the debugging feature
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
# disable(CRITICAL)
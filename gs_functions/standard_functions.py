# This Python file uses the following encoding: utf-8

# MODULES AND/OR LIBRARIES
from subprocess import run
from logging import basicConfig, DEBUG, debug, disable, CRITICAL



# Configuring debugging feature code
basicConfig(level=DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Disabling the debugging feature. Hint: Comment out this line to enable debugging.
# disable(CRITICAL)



##############################

# STANDARD FUNCTIONS

##############################

def manage_netfilter_service(user_pwd):
    """A function which starts and enables netfilter service if it's not"""

    netfilter_persistent_status = run(["sudo", "-S", "bash", "-c", "systemctl status netfilter-persistent"], input=user_pwd, text=True, capture_output=True).stdout.strip()

    if 'inactive' in netfilter_persistent_status:

        run(["sudo", "-S", "bash", "-c", "systemctl start netfilter-persistent"], input=user_pwd, text=True, capture_output=True)

        debug("Starting netfilter-persistent.service")

    if 'disabled' in netfilter_persistent_status:

        run(["sudo", "-S", "bash", "-c", "systemctl enable netfilter-persistent"], input=user_pwd, text=True, capture_output=True)

        debug("Enabling netfilter-persistent.service")

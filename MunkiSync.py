#!/usr/bin/python
# MunkiSync
# Runs as a LaunchAgent and syncs everything from a master repo to a drive

# Libraries
import subprocess
import os
import datetime
from mount_shares_better import mount_share

# Variables
MASTER_MOUNT_PT = "/Volumes/Munki"
MASTER_MOUNT_IP = "smb://username:password@ip/Munki"
MUNKI_MASTER = "/Volumes/Munki/munki_repo/"
MUNKI_LOCAL = "/Volumes/Munki HD/munki_repo"
DATE = datetime.datetime.now().date();
# Functions


def UnmountServer():
    if (os.path.isdir(MASTER_MOUNT_PT)):
        unmount = subprocess.check_call(["/sbin/umount", MASTER_MOUNT_PT])
        print "{0} unmounted".format(MASTER_MOUNT_PT)


def SyncEverything():
    if (os.path.isdir(MUNKI_LOCAL)):
        sync = subprocess.check_call(['/usr/bin/rsync', '--exclude=\".*\"', '-r', '-az', '--size-only', '--progress', '--delete-after', MUNKI_MASTER, MUNKI_LOCAL])
        print "Syncing Repos"
    else:
        print "{0} is not available to sync too.".format(MUNKI_LOCAL)
        exit()


def UpdatePermissions():
    perms = subprocess.check_call(["/bin/chmod", "-R", "755", MUNKI_LOCAL])
    print "Updating Permissions."
# Main


def main():
    print "MunkiSync run at {0}".format(datetime.datetime.now())
    print "Mounting Share at {0} ".format(MASTER_MOUNT_PT)
    if (os.path.isdir(MASTER_MOUNT_PT)):
        print "Already Mounted Munki Master at {0}".format(MASTER_MOUNT_PT)
    else:
        mount_share(MASTER_MOUNT_IP)
        print "Mounted Munki Master ({0}) at {1}".format(MASTER_MOUNT_IP, MASTER_MOUNT_PT)
    SyncEverything()
    UpdatePermissions()
    UnmountServer()
    print "MunkiSync run completed at {0}".format(datetime.datetime.now())
    exit()

main()

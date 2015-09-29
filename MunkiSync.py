#!/usr/bin/python
# MunkiSync
# Runs as a LaunchAgent and syncs everything from a master repo to a drive

# Libraries
import subprocess
import os
from mount_shares_better import mount_share

# Variables
MASTER_MOUNT_PT = "/Volumes/Munki"
MASTER_MOUNT_IP = "smb://username:password@ip/Munki"
MUNKI_MASTER = "/Volumes/Munki/munki_repo/"
MUNKI_LOCAL = "/Volumes/Munki HD/munki_repo"

# Functions


def UnmountServer():
    if (os.path.isdir(MASTER_MOUNT_PT)):
        unmount = subprocess.check_call(["/sbin/umount", MASTER_MOUNT_PT])


def SyncEverything():
    if (os.path.isdir(MUNKI_LOCAL)):
        sync = subprocess.check_call(['/usr/local/bin/rsync', '--exclude=\".*\"', '-r', '--perms', '--times', '--progress', '--delete-after', MUNKI_MASTER, MUNKI_LOCAL])
    else:
        print "{0} is not available to sync too.".format(MUNKI_LOCAL)
        exit()


def UpdatePermissions():
    print "Updating Permissions."
    perms = subprocess.check_call(["/bin/chmod", "-R", "755", MUNKI_LOCAL])

# Main


def main():
    print "Mounting Share at {0} ".format(MASTER_MOUNT_PT)
    if (os.path.isdir(MASTER_MOUNT_PT)):
        print "Already Mounted Munki Master at {0}".format(MASTER_MOUNT_PT)
    else:
        mount_share(MASTER_MOUNT_IP)
        print "Mounted Munki Master ({0}) at {1}".format(MASTER_MOUNT_IP, MASTER_MOUNT_PT)
    SyncEverything()
    UpdatePermissions()
    UnmountServer()

main()

#!/usr/bin/python
# MunkiSync
# Runs as a LaunchAgent and syncs everything from a master repo to a drive

# Libraries
import subprocess
import os
import logging
from mount_shares_better import mount_share

# Variables
MASTER_MOUNT_PT = "/Volumes/Munki"
MASTER_MOUNT_IP = "smb://192.168.145.26/Munki"
MUNKI_MASTER = "/Volumes/Munki/munki_repo/"
MUNKI_LOCAL = "/Volumes/Munki HD/munki_repo"

# Functions


def UnmountServer():
    if (os.path.isdir(MASTER_MOUNT_PT)):
        unmount = subprocess.check_call(["/sbin/umount", MASTER_MOUNT_PT])


def SyncEverything():
    if (os.path.isdir(MUNKI_LOCAL)):
        sync = subprocess.check_call(["/usr/local/bin/rsync", "--exclude=\".*\"", "-r", "--perms", "--times", "--progress", "--delete-after", MUNKI_MASTER, MUNKI_LOCAL])
    else:
        print("%s is not available to sync too." % MUNKI_LOCAL)
        exit()


def UpdatePermissions():
    print("Updating Permissions.")
    perms = subprocess.check_call(["/bin/chmod", "-R", "755", MUNKI_LOCAL])

# Main


def main():
    if not(os.path.isdir(MASTER_MOUNT_PT)):
        print("Ok to mount at %s" % MASTER_MOUNT_PT)
        mount_share(MASTER_MOUNT_IP)
        print("Mounted Munki Master (%s) at %s".format(MASTER_MOUNT_IP, MASTER_MOUNT_PT))
    SyncEverything()
    UpdatePermissions()
    UnmountServer()

main()

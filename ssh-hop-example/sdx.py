#!/usr/bin/python
#
# Simple factory reset/upgrade of Netscalar SDX
#
# Date: Jan 2015 by Shankar Krishnamurthy
#

import sys, os
import getpass
import telnetlib
import re
import optparse
import traceback
import time
import subprocess
import paramiko as ssh

sys.path.insert(0,os.path.dirname(os.path.realpath(__file__))) #Location of ssh_hop
from ssh_hop import ssh_hop

# Hardcoded - can be moved to cfg if needed
timeout = 15  # in seconds
svmlogin = "nsroot" # Used for/by NITRO
svmpasswd = "nsroot"
svminternalip = "169.254.0.10"
sshport = 22

sdx = {}     # sdx info
def get_sdx():
    if not options.file:
        print ("")
        parser.error("File mandatory")
    f = open(options.file, 'r')
    try:
        for line in f:
            if not ":" in line:
                continue
            (key, val) = line.split( ' : ', 1)
            val = val.rstrip('\n')
            sdx[key] = val
    finally:
        f.close()
    return sdx

def Read_Until(tn, str):
    obj = tn.read_until(str,timeout)
    if not re.search(re.escape(str), obj):
        traceback.print_stack()
        sys.exit()
    return obj

def do_telnet():
    return telnetlib.Telnet(sdx["Console IP"], sdx["Console Port"], timeout)

def try_login(tn):
    tn.write("\n")
    alist = [ 'login: ', "\]\# $", "1 - Initiate a regular session" ]
    [ a,b,str ] = tn.expect(alist, timeout)
    match = re.search(r".*1 - Initiate.*", str)
    if match:
        tn.write("1\n")
        alist = [ 'login: ', "\]\# $" ]
        [ a,b,str ] = tn.expect(alist, timeout)
    match = re.search(r".* login: ", str)
    return match

def do_poll_sdx(tn, initial, interval, count, wait_for_svm):
    print "\nWaiting for sdx system to come up\n"
    time.sleep(initial) # Wait for system to go down
    cnt=count
    trytime=interval
    retry=wait_for_svm
    while(cnt > 0):
        match = try_login(tn)
        if match:
            if not retry:
                print "sdx is up. waiting for svm to come up"
                retry=1
            else:
                return 0
        time.sleep(trytime)
        cnt -= 1
        print "trying sdx (if its up)..."

    # If it comes here, sdx is not up
    print "SDX is not up. Aborting"
    sys.exit(1)

def poll_sdx(tn):
    do_poll_sdx(tn, 600, 180, 10, 0)

def quick_poll_sdx(tn):
    do_poll_sdx(tn, 180, 30, 10, 1)

def do_login(tn):
    match = try_login(tn)
    if match:
        tn.write(sdx["Username"] + "\n")
        if sdx["Password"]:
            Read_Until(tn, "Password: ")
            tn.write(sdx["Password"] + "\n")
    #else assumed to be in shell (already logged-in)

def do_reboot():
    do_cmd("\nreboot\n")

    quick_poll_sdx(tn)

def do_factory():
    primary='/dev/md_d0'
    rc=do_cmd_and_return_code("\nls %s\n" % primary)
    if (rc!=0):
        primary='/dev/sda'
    cmds = [ 
        "\nfdisk %s\n" % primary, "a\n" , "1\n", "a\n", "2\n" ,"t\n", "1\n", "c\n", 
           ]
    for cmd in cmds:
        tn.write(cmd)
        Read_Until(tn, "): ")

    if (options.verbose == True):
        tn.write("p\n")
        fdiskout=Read_Until(tn, "): ")
        print fdiskout

        yes = set(['yes','y', 'ye', ''])
        choice = raw_input("Reading to factory reset. Do you want to proceed(yes/no): ").lower()
        if choice not in yes:
            print "reboot process aborted"
            tn.write("q\n")
            sys.exit()

    tn.write("w\n")
    Read_Until(tn, "]# ")

    tn.write("reboot\n")

    poll_sdx(tn)

def do_cmd(cmd):
    alist = [ "\]\# $" ]
    tn.write(cmd)
    [ a,b,str ] = tn.expect(alist, timeout)
    return str

def do_cmd_and_return_code(cmd):
    alist = [ "\]\# $" ]
    tn.write("\n")
    [ a,b,str ] = tn.expect(alist, timeout)
    tn.write(cmd)
    [ a,b,str ] = tn.expect(alist, timeout)
    tn.write("echo $?\n")
    [ a,b,str ] = tn.expect(alist, timeout)
    arrint=[int(s) for s in str.split() if s.isdigit()]
    return arrint[0]

def do_dom0_ip():
    # get uuid for eth device
    str = do_cmd ("\nxe pif-list params=uuid device="+ sdx["DOM0 device"] + "\n")
    m = re.search(' : (.{37})', str)
    if m:
        uuid=m.group(1)
    else:
        print "No Match found for pif-device \n", str, "\n"
        sys.exit()

    do_cmd ("\nxe pool-disable-redo-log\n")
    # write IP for this uuid
    str = do_cmd ("xe pif-reconfigure-ip IP=" + sdx["DOM0 Mgmt IP"] + " netmask=" + sdx["DOM0 Netmask"] + " gateway=" +  sdx["NS GW IP"]  + " mode=static uuid=" + uuid + "\n")

    #set name 
    try:
        sdx["Device Name"]
        str = do_cmd ("\nxe host-list params=uuid\n")
        m = re.search(' : (.{37})', str)
        if m:
            hostuuid=m.group(1)
            cmd = "\nxe host-set-hostname-live host-name="+sdx["Device Name"]+" host-uuid=" + hostuuid + "\n"
        do_cmd(cmd)
    except:
        cmd="\n"

    #enable xencenter
    do_cmd ( "\nxe host-management-reconfigure pif-uuid=" + uuid + "\n")

def do_svm_ip():
    host = (svminternalip,sshport)
    via = (sdx["DOM0 Mgmt IP"],sshport)

    try:
        ssht = ssh_hop(host, "nsrecover", sdx["Password"], via, sdx["Username"], sdx["Password"] )
    except ssh.BadAuthenticationType as e:
        ssht = ssh_hop(host, sdx["Username"], sdx["Password"], via, sdx["Username"], sdx["Password"] )

    cmds = [ "ifconfig 0/1 " + sdx["NS Mapped IP"] + " netmask " + sdx["DOM0 Netmask"], \
            "route add default " + sdx["NS GW IP"] ]

    for cmd in cmds:
        (buf, rc) = ssht.Send("echo \"" + cmd + "\" >> " + '/mpsconfig/svm.conf\n')
        (buf, rc) = ssht.Send(cmd + '\n')
        if (int(rc) != 0):
            print "Remote command failed %s %d\n" % (buf,rc)
            sys.exit()
    ssht.Close()

def do_transfer(str, src, dest):
    fpath, fname = os.path.split(src)

    if options.skiptransfer:
        print "Skipping Transfer. Using file in appliance with same name"
        return fname
        
    sys.stdout.write("\nTransferring "+ str +"...")
    sys.stdout.flush()
    try:
        ssht = ssh_hop(sdx["NS Mapped IP"], sdx["Username"], sdx["Password"] , None, None, None)
    except ssh.BadAuthenticationType, e:
        ssht = ssh_hop(sdx["NS Mapped IP"], "nsrecover", sdx["Password"], None, None, None )
    sftp = ssht.get_sftp()
    sftp.put(src, dest+fname)
    print " done"

    if options.onlytransfer:
        print "Only Transfer requested. So, Exiting now."
        sys.exit(0)

    return fname

def do_call(execfile, extraarg):
    sys.stdout.write("starting exec ...")
    cmd = execfile +" "+sdx["NS Mapped IP"] +" " + svmlogin + " " + svmpasswd + " " + extraarg + " \n"
    rc=0
    try:
        rc = subprocess.call(cmd, shell=True)
    finally:
        print " done"
    return rc

def do_svm_upgrade():
    if not options.svmimage:
        return

    if not os.path.isfile(options.svmimage):
        print("svm image wrong/absent. skipping")
        return

    fname = do_transfer(" svm tgz ", options.svmimage, "/var/mps/mps_images/")

    rc = do_call("sdx_svm_upgrade.py", fname)

    if rc!=0:
        print "Upgrading svm manually ..."
        ssht = ssh_hop(sdx["NS Mapped IP"], sdx["Username"], sdx["Password"] , None, None, None)
        ssht.run("cd /var/mps/mps_images/;tar -xzvf %s; ./installsvm" % fname);

    print "waiting for 2 mins for SVM to comeup"
    time.sleep(120)

def do_xen_upgrade():
    if not options.xenimage:
        return

    if not os.path.isfile(options.xenimage):
        print("xen image wrong/absent. skipping")
        return

    fname = do_transfer(" xen iso ", options.xenimage, "/var/mps/xen_images/")

    do_call("sdx_xen_upgrade.py", fname)

    poll_sdx(tn)

def do_sbu():
    if not options.sbu:
        return

    if not os.path.isfile(options.sbu):
        print("sbi image wrong/absent. skipping")
        return

    fname = do_transfer(" sdx SBU ", options.sbu, "/var/mps/cb_sb_images/")

    do_call("sdx-sbu.py", fname)

    poll_sdx(tn)

def do_clean_install():
    if not options.ci:
        return

    if not os.path.isfile(options.ci):
        print("sbi image wrong/absent. skipping")
        return

    fname = do_transfer(" sdx ci ", options.ci, "/var/mps/cb_sb_images/")

    do_call("sdx-ci.py", fname)

    poll_sdx(tn)

def do_xen_hotfix():
    if not options.hotfix:
        return

    for eachfile in options.hotfix:
        if not os.path.isfile(eachfile):
            print "image ", eachfile, "not present. skipping"
            continue

        fname = do_transfer(" hot fix ", eachfile, "/var/mps/xen_hotfixes/")

        # xe patch-apply uuid= uuid= host-uuid=
        do_call("sdx_hotfixes.py", fname)

def do_xen_supppack():
    if not options.supppack:
        return

    if not os.path.isfile(options.supppack):
        print("iso image wrong/absent. skipping")
        return

    fname = do_transfer(" supppack iso ", options.supppack, "/var/mps/xen_supplemental_packs/")

    do_call("sdx_supppack_install.py", fname)

    #poll sdx?

def do_exec_dom0_cmd():
    if not options.execdom0:
        return
    host = (sdx["DOM0 Mgmt IP"],sshport)

    ssht = ssh_hop(host, sdx["Username"], sdx["Password"], None, None,None)

    for cmd in options.execdom0:

        print "Executing ", cmd
        (buf, rc) = ssht.run(cmd + '\n')
        if (int(rc) != 0):
            print "dom0 command failed %s %d\n" % (buf,rc)
            sys.exit()
        print buf
        print "Status ", rc
    ssht.Close()

def do_license():
    if not options.license:
        return

    if not os.path.isfile(options.license):
        print("license wrong/absent. skipping")
        return

    fname = do_transfer(" license ", options.license, "/flash/mpsconfig/license/")

    #Apply license
    do_call("sdx_license.py", fname)

def do_lom_ip():
    if not options.lomip:
        return

    EXECUTE (do_login, "Telnet login to console ", tn)
    # load required drivers for running ipmitool
    do_cmd ("\nmodprobe ipmi_devintf\n")
    do_cmd ("\nmodprobe ipmi_msghandler\n")
    do_cmd ("\nmodprobe ipmi_si\n")

    # configure LOM ip
    if not sdx.has_key("LOM NETMASK"):
        sdx["LOM NETMASK"] = sdx["DOM0 Netmask"]
    if not sdx.has_key("LOM DEFGW"):
        sdx["LOM DEFGW"] = sdx["NS GW IP"]

    do_cmd ("\nipmitool lan set 1 ipaddr " + sdx["LOM IP"] + "\n")
    do_cmd ("\nipmitool lan set 1 netmask " + sdx["LOM NETMASK"] + "\n")
    do_cmd ("\nipmitool lan set 1 defgw ipaddr " + sdx["LOM DEFGW"] + "\n")

def post_reboot():

    print "Starting post-reboot operations:"

    if not options.skipdom0ip:
        EXECUTE (do_login, "Telnet login to console ", tn)
        # Apply IP address for XenServer Persistently
        EXECUTE (do_dom0_ip, "Assigning DOM0 ip persistently ")

    if not options.skipsvmip:
        # Apply IP address for SVM Persistently
        EXECUTE (do_svm_ip, "Assigning SVM ip persistently ")

    # update SVM Image
    EXECUTE (do_svm_upgrade, "Upgrading SVM tarball ", None, "Upgrading SVM tarball ")

    # updade XenServer Image
    EXECUTE (do_xen_upgrade, "Upgrading XEN iso " , None, "Upgrading XEN tarball ")

    # Apply Hot Fixes
    EXECUTE (do_xen_hotfix, "Apply Xen HotFix ", None, "Xen HotFix ")

    # Apply Supplemental Pack
    EXECUTE (do_xen_supppack, "Apply NS supplemental pack ", None, "NS supplemental pack")

    # Apply License file to SVM
    EXECUTE (do_license, "Apply VPX License ", None, "VPX License " )

    # Configure LOM ip address
    EXECUTE (do_lom_ip, "Assigning LOM ip ")

    # Clean Install SBI
    EXECUTE (do_clean_install, "Clean Install SBI " , None, "Clean Install SDX SBI ")

    # Upgrade SBI
    EXECUTE (do_sbu, "SBI Upgrade " , None, "SDX SBI Upgrade ")

    # Run arbitrary DOM0 cmd
    EXECUTE (do_exec_dom0_cmd, "Run DOM0 cmd", None, "Run DOM0 bash cmd")

def EXECUTE (fn, banner, arg1=None, endbanner=None):
    sys.stdout.write(banner+'...')
    sys.stdout.flush()
    if not arg1:
        rc = fn()
    else:
        rc = fn(arg1)
    if endbanner:
        sys.stdout.write(endbanner+'...')
    print(" done")
    return rc

#
# __ Main__ Routine
#

# reconciling program options
parser = optparse.OptionParser()
parser.add_option('--file', help="mangatory field to identify sdx" )
parser.add_option('--svmimage', help="svm image to upgrade")
parser.add_option('--xenimage', help="xen image to upgrade")
parser.add_option('--hotfix', action="append" , help="hotfixes to apply")
parser.add_option('--supppack', help="upgrade supplemental pack")
parser.add_option('--license',  help="upgrade license")
parser.add_option('-e','--execdom0', action="append",  help="exec dom0 cmd")
parser.add_option('--ci', help="perform clean install")
parser.add_option('--sbu', help="perform SB Upgrade")
parser.add_option('-v', '--verbose', default=False, action="store_true",)
parser.add_option('--factoryreset', default=False, action="store_true", help="Do Factory reset")
parser.add_option('--reboot', default=False, action="store_true", help="Do Appliance reboot")
parser.add_option('-d', '--skipdom0ip', default=False, action="store_true", help="skip dom0 ip settings")
parser.add_option('-b', '--lomip', default=False, action="store_true",)
parser.add_option('-s', '--skipsvmip', default=False, action="store_true", help="skip svm ip settings")
parser.add_option('-t', '--skiptransfer', default=False, action="store_true", help="skip transfer and directly perform operation (only applicable to certain options)")
parser.add_option('-o', '--onlytransfer', default=False, action="store_true", help="only to transfer and not upgrade (applicable to only some options)")
parser.add_option('--version', default=1.0, type="float", )
options, remainder = parser.parse_args()

# Read the SDX Config File
sdx = EXECUTE(get_sdx, "Getting SDX info ")

# get telnet object
tn = EXECUTE(do_telnet, "Get Telnet info ")
if tn is None:
    print "telnet failed ", sdx["Console IP"], ":", sdx["Console Port"]
    sys.exit()

# reset to factory
if options.factoryreset: 
    EXECUTE(do_login, "Telnet login to console ", tn)
    EXECUTE(do_factory, "Performing factory reset ", None, "\nFactory reset ")
else: print "Skipping factory reset process.\n"

# reboot sdx
if options.reboot: 
    EXECUTE(do_login, "Telnet login to console ", tn)
    EXECUTE(do_reboot, "Performing normal reboot ", None, "\nAppliance reboot ")
else: print "Skipping reboot process.\n"

# Upgrade images
post_reboot()


#!/usr/bin/python
#
# Pulling binaries from netscaler build m/c
#
# Date: Mar 2015 by Shankar Krishnamurthy
#

import sys, os
import re
import optparse
import ftplib
import paramiko
from datetime import datetime
from pprint import pprint
import multiprocessing as mp
import time

# Build Server info - Default
BSERVER_FAST="10.217.5.148"
BSERVER="10.217.120.27"
BUSER='build'
BPASS='nsBuild3217'

# License server info - Default
LSERVER="10.217.15.6"
LUSER='nsroot'
LPASS='nsroot'
LDIR='/home/nsroot/license/2017'

# Common mapping
release = { 'ion' : 'builds_ion', 
            'tagma' : 'builds_tagma', 
            'kopis' : 'builds_kopis', 
            'oban' : 'builds_oban', 
            'kamet' : 'builds_kamet' , 
            'mana' : 'builds_mana' , 
            'dara' : 'builds_dara' }
relnum = {  'ion' : '11.0', 
            'tagma' : '10.5' , 
            'kopis' : '11.1' , 
            'oban' : '12.0' , 
            'kamet' : '12.1' , 
            'mana' : '13.0' , 
            'dara' : '10.1' }

def get_name(bld, rel):
    if not rel:
        return None

    try:
        release[rel]
    except KeyError:
        print "Please provide: ", release.keys()
        return None

    if not bld:
        return '/'+release[rel];

    bld1 = re.sub('\.', '_', bld)
    
    return '/'+release[rel]+'/build_'+rel+'_'+bld1

# original : not used
#def _traverse(ftp, depth=0):
    #if depth > 10:
        #return ['depth > 10']
    #level = {}
    #for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        #try:
            #ftp.cwd(entry)
            #level[entry] = _traverse(ftp, depth+1)
            #ftp.cwd('..')
        #except ftplib.error_perm:
            #level[entry] = None
    #return level

def do_filter(path, pattern):
    mylist = ftp.nlst(path)
    for f in mylist:
        ftp.sendcmd("TYPE i")
        size = ftp.size(path+'/'+f)
        if size==0:
            continue

        if not pattern:
            print path+'/'+f, " (",size,")"
            continue

        m = re.search(r'%s'%pattern, path + '/' + f, re.I)
        if m:
            print path+'/'+f, " (",size,")"

def traverse(ftp, dir, depth=0):
    if depth > 10:
        return
    do_filter(dir, options.traverse)
    for entry in (path for path in ftp.nlst() if path not in ('.', '..')):
        try:
            ftp.cwd(entry)
            newpath = dir + '/' + entry
            traverse(ftp, newpath, depth+1)
            ftp.cwd('..')
        except ftplib.error_perm:
            pass
    return


def do_traverse():
    path = get_name(options.build, options.release)
    if not path:
        print("invalid format build or release\n")
        return None
    try:
        ftp.cwd(path)
    except:
        print "release dir", path, "doesn't exists"
        return None

    traverse(ftp, path, 0)

def do_search():
    path = get_name(options.build, options.release)
    if not path:
        print("invalid format build or release\n")
        return None

    paths = []
    paths.append(path)
    bld = 'build_'+options.release+'_'+re.sub('\.', '_', options.build)
    if relnum.has_key(options.release):
        paths.append("/RELEASE/%s/%s"% (relnum[options.release],bld) )

    for p in paths:
        try:
            ftp.cwd(p)
        except:
            print "release dir", p, "doesn't exists"
            continue
    
        #pprint(traverse(ftp))
        do_filter(p, options.search)
        break

def progress(src,dst):
    mydst = open(dst.name, "wb") # Have to open again. Now option out
    # Not needed (optional) - Lets also open ftp to fast server here
    fobj = ftplib.FTP(BSERVER_FAST) 
    fobj.login(BUSER, BPASS) 
    fobj.retrbinary("RETR " + src ,mydst.write)
    fobj.close()

def _getfile(remotefile, localout):
    try:
        tsz = ftp.size(remotefile)
        #ftp.retrbinary("RETR " + remotefile ,localout.write)
        p = mp.Process(target=progress, args=(remotefile, localout,))
        p.start()
        while p.is_alive(): 
            time.sleep(1)
            csz = os.stat(localout.name).st_size
            sys.stdout.write('\rCompleted : %f %% '%(float(csz)/float(tsz)*100.0))
            sys.stdout.flush()

        p.join()
        print
            
    except Exception as e:
        print "     Error getting " + remotefile + ":" + str(e)
 
def do_fileget(file):
    fname = os.path.basename(file)
    fw = do_open('.', fname)
    if not fw:
        return
    _getfile(file, fw)

def do_vb():
    files =[]
    if not options.vb:
        return files
    path = get_name(options.build, options.release)
    if not path:
        print("invalid format build or release\n")
    else:
        ftp.cwd(path)
        xen = 'SDX/XS-'+options.vb+'.0/virtual-bundle'
        mylist = ftp.nlst(path+'/'+xen)
        for i in mylist:
            files.append(path+'/'+xen + '/' +i)
            print "%s" % (path+'/'+xen + '/' +i)
    return files

def do_findfiles():
    if not options.xen:
        return

    if not options.traverse:
        options.traverse=options.xen

    dir = [ "/builds_xs", "/NSSDX_images"]
    for entry in dir:
        ftp.cwd(entry)
        traverse(ftp, entry, 0)
    return None

def do_open(localdir, localfile):
    try:
        if not os.path.exists(localdir):
            os.mkdir(localdir)
        localfile = localdir+'/'+localfile
        if os.path.exists(localfile):
            print "     Already ", localfile, " exists. skipping"
            return None
        fw = open(localfile,"wb")
    except Exception as e:
        print str(e)
        return None
    return fw

def do_getfiles(remotefiles, localdir):
    for fullname in remotefiles:
        f = os.path.basename(fullname)

        try:
            ftp.sendcmd("TYPE i")
            size = ftp.size(fullname)
        except Exception as e:
            print f+ ":" +str(e)
            continue

        print("getting file " + f + " size "+ str(size) + " bytes")
    
        fw = do_open(localdir, f)
        if not fw:
            continue
        
        _getfile(fullname, fw)

def do_findlicenses(rdir):
    mylist = []
    mylist = ftp.listdir(path = rdir)
    return mylist

def do_licfiles(rdir, remotefiles, localdir):
    if not os.path.exists(localdir):
        os.mkdir(localdir)

    fcnt=0
    for f in remotefiles:
        fw = do_open(localdir, f)
        if not fw:
            continue
        try:
            ftp.get(rdir+'/'+f, localdir+'/'+f)
        except Exception as e:
            continue
        fcnt += 1
    print "Total license files ", fcnt

def do_list_builds():
    if not options.list:
        return

    path = get_name(options.build, options.release)
    paths = []
    paths.append(path)
    if relnum.has_key(options.release):
        paths.append("/RELEASE/%s"% relnum[options.release])

    for p in paths:
        try:
            ftp.cwd(p)
        except:
            print "release dir", path, "doesn't exists"
            return None
    
        ls = ftp.sendcmd("MLST")
        lines = ls.split('\n')
        for l in lines:
            # MLST Format: 250- size=0;type=dir;modify=20160312095502; build_tagma_59_398
            m = re.search('type=dir;modify=(.*?); (.*?)$', l)
            t = f = None
            if m:
                t = m.groups()[0]
                f = m.groups()[1]
    
            if not f or not t:
                continue
            
            print datetime.strptime(t, "%Y%m%d%H%M%S"), " ", f #, l
            
#
# __Main__ Routine
#

# Parse command line options
parser = optparse.OptionParser()
parser.add_option('-v', '--verbose', default=False, action="store_true",)
parser.add_option('--license',default=False, action="store_true", help=" pulling all license files")
parser.add_option('-l', '--list',default=False, action="store_true", help=" Listing Builds for particular release")
parser.add_option('-b', '--build', help="build number eg. 58.4.e" )
parser.add_option('-r', '--release', help="release . Namely, ion, dara, tagma" )
parser.add_option('-x', '--xen', help="Looks in /NSSDX_images, /builds_xs (can use with -t)")
parser.add_option('--vb', help="downloads virtual bundle. either 6.1, 6.5, 6.0")
parser.add_option('-s', '--search' , help="search 'pattern' on in top directory")
parser.add_option('-t', '--traverse' , help="recursively search 'pattern'")
parser.add_option('-f', '--file',action="append", help="download file - absolute path")

options, remainder = parser.parse_args()

#Environment Variable - If any
if os.getenv('BSERVER'): BSERVER = os.getenv('BSERVER')
if os.getenv('BUSER'): BSERVER = os.getenv('BUSER')
if os.getenv('BPASS'): BSERVER = os.getenv('BPASS')

if os.getenv('LSERVER'): BSERVER = os.getenv('LSERVER')
if os.getenv('LUSER'): BSERVER = os.getenv('LUSER')
if os.getenv('LPASS'): BSERVER = os.getenv('LPASS')
if os.getenv('LDIR'): BSERVER = os.getenv('LDIR')

# connect/login ftp server
ftp = ftplib.FTP(BSERVER) 
ftp.login(BUSER, BPASS) 

if options.file:
    for f in options.file:
        do_fileget(f)

if options.release and not options.build:
    do_list_builds()

if options.release and options.build:
    if options.search:
        do_search()

    if options.traverse:
        do_traverse()

    files=do_vb()
    if files:
        do_getfiles(files, options.release+'-'+options.build)
    
# Find all other files that are interesting
do_findfiles()

ftp.quit()

if options.license:
    transport = paramiko.Transport((LSERVER, 22))
    transport.connect(username = LUSER, password =LPASS)
    ftp = paramiko.SFTPClient.from_transport(transport)

    # Find all the files that are interesting
    files = do_findlicenses(LDIR)
    # We found all files that are interesting. Now go get them
    do_licfiles(LDIR, files, 'license-2017')
    ftp.close()
    transport.close()
    

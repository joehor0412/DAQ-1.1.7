"""Upload the contents of data folder to Dropbox.
This is a script written using Dropbox API v2.
Modified from updown.py in Dropbox API v2 Github
"""

from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import socket
import logging

# logging config
logging.basicConfig(format='%(asctime)s %(message)s',filename='/home/pi/Serial/events/dropbox_events.log',level=logging.DEBUG)

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox

# OAuth2 access token.  TODO: login etc.
TOKEN = 'sl.BoGicyX55tsemhY-OQg3EKt2tvQedd0FO5Cr4YB3Fv8jDyC_cfoVCbuXiTM7FRCBL7e049vQy0sUFk9ZmT5m-5845U3sWmpernAJojKIgOtwkc2T2HmOxxhEepqGtvveth_ItLmlj1noiM0mdALYK7Q'

# Device hostname
hostname = socket.gethostname()
folder_path_to_dropbox = str(hostname)

parser = argparse.ArgumentParser(description='Sync ~/Downloads to Dropbox')
parser.add_argument('folder', nargs='?', default=folder_path_to_dropbox,
                    help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~/Serial/data',
                    help='Local directory to upload')
parser.add_argument('--token', default=TOKEN,
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

def main():
    """Main program.
    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    logging.debug('==================  New Entry  ==================')

    args = parser.parse_args()
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        logging.debug('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    if not args.token:
        logging.debug('--token is mandatory')
        sys.exit(2)

    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    logging.debug('Dropbox folder name:'+ folder)
    logging.debug('Local directory:'+ rootdir)
    if not os.path.exists(rootdir):
        logging.debug(rootdir + 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        logging.debug(rootdir + 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(args.token)

    for dn, dirs, files in os.walk(rootdir):
        subfolder = dn[len(rootdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        logging.debug('Descending into '+ subfolder + '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            if not isinstance(name, six.text_type):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                logging.debug('Skipping dot file:' + name)
            elif name.startswith('@') or name.endswith('~'):
                logging.debug('Skipping temporary file:' + name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                logging.debug('Skipping generated file:' + name)
            elif nname in listing:
                md = listing[nname]
                mtime = os.path.getmtime(fullname)
                mtime_dt = datetime.datetime(*time.gmtime(mtime)[:6])
                size = os.path.getsize(fullname)
                if (isinstance(md, dropbox.files.FileMetadata) and
                        mtime_dt == md.client_modified and size == md.size):
                    logging.debug(name + ' is already synced [stats match]')
                else:
                    logging.debug(name + ' exists with different stats, downloading')
                    res = download(dbx, folder, subfolder, name)
                    with open(fullname) as f:
                        data = f.read()
                    if res == data:
                        logging.debug(name + ' is already synced [content match]')
                    else:
                        logging.debug(name + ' has changed since last sync')
                        if yesno('Refresh %s' % name, False, args):
                            upload(dbx, fullname, folder, subfolder, name,
                                   overwrite=True)
            elif yesno('Upload %s' % name, True, args):
                upload(dbx, fullname, folder, subfolder, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                logging.debug('Skipping dot directory:' + name)
            elif name.startswith('@') or name.endswith('~'):
                logging.debug('Skipping temporary directory:' + name)
            elif name == '__pycache__':
                logging.debug('Skipping generated directory:' + name)
            elif yesno('Descend into %s' % name, True, args):
                logging.debug('Keeping directory:' + name)
                keep.append(name)
            else:
                logging.debug('OK, skipping directory:' + name)
        dirs[:] = keep

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        logging.debug('Folder listing failed for'  + str(path)  + '-- assumed empty:'  + str(err))
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            logging.debug('*** HTTP error', err)
            return None
    data = res.content
    logging.debug(len(data), 'bytes; md:', md)
    return data

def upload(dbx, fullname, folder, subfolder, name, overwrite=False):
    """Upload a file.
    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(fullname)
    with open(fullname, 'rb') as f:
        data = f.read()
    with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            logging.debug('*** API error', err)
            return None
    logging.debug('uploaded as' + str(res.name.encode('utf8')))
    return res

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.
    Command line arguments --yes or --no force the answer;
    --default to force the default answer.
    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.
    Retry on unrecognized answer.
    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if args.default:
        logging.debug(message + '? [auto]' + 'Y' if default else 'N')
        return default
    if args.yes:
        logging.debug(message + '? [auto] YES')
        return True
    if args.no:
        logging.debug(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            logging.debug('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        logging.debug('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to logging.debug how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        time_taken = t1-t0
        logging.debug('Total elapsed time for '+ message + ':' + str(time_taken))

if __name__ == '__main__':
    main()

#!/usr/bin/python

import os
import sys
import subprocess
import tempfile

def execute(cmd, cwd = None):
  subprocess.Popen(cmd, cwd=cwd).communicate()

def cvs2git(cvs_path, git_path):
  temp_blob_path = tempfile.mkstemp('-blob.dat')[1]
  temp_dump_path = tempfile.mkstemp('-dump.dat')[1]

  print 'Removing Attic duplicates'
  files = []
  for (dirpath, dirnames, filenames) in os.walk(cvs_path):
    files.extend(map(lambda x: os.path.join(dirpath, x), filenames))

  for f in files:
    if os.path.basename(os.path.dirname(f)) != 'Attic':
      original = f
      attic = os.path.join(os.path.dirname(f), 'Attic', os.path.basename(f))
      if os.path.exists(original) and os.path.exists(attic):
        print 'Removing %s' % attic
        os.remove(attic)

  print 'Running cvs2git'
  execute([
    'cvs2git',
    '--blobfile', temp_blob_path,
    '--dumpfile', temp_dump_path,
    '--username', 'chhoffme',
    '--encoding', 'windows-1252',
    cvs_path])

  print 'Importing to GIT repository'
  os.makedirs(git_path)
  execute(["git", "init"], cwd = git_path)
  p1 = subprocess.Popen(["cat", temp_blob_path, temp_dump_path], stdout=subprocess.PIPE)
  p2 = subprocess.Popen(["git", "fast-import"], stdin=p1.stdout, cwd=git_path)
  p2.communicate()

  print 'Clean up repository with BFG'
  execute(["bfg",
    "--delete-folders", "CVSROOT",
    "--delete-files", ".dummy.txt",
    "--no-blob-protection"], cwd = '%s/.git' % git_path)
  execute(["git", "reflog", "expire", "--expire=now", "--all"], cwd = '%s/.git' % git_path)
  execute(["git", "gc", "--prune=now"], cwd = '%s/.git' % git_path)

  print 'Checkout repository'
  execute(["git", "checkout"], cwd = git_path)

if len(sys.argv) != 3:
  print 'usage: migrate.py /path/to/cvs/dir /path/to/git/dir'
else:
  cvs2git(sys.argv[1], sys.argv[2])

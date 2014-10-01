#!/usr/bin/python

import os
import subprocess

base_path = os.path.dirname(os.path.realpath('%s/..' % __file__))

def execute(cmd, cwd):
  subprocess.Popen(cmd, cwd=cwd).communicate()

def cvs2git(zip_path, module_path):
  global base_path
  cvs_path = '%s/repo-cvs' % module_path
  git_path = '%s/repo-git' % module_path
  cvs2git_blob_path = '%s/blob.dat' % module_path
  cvs2git_dump_path = '%s/dump.dat' % module_path

  if not os.path.exists(module_path): os.makedirs(module_path)
  if not os.path.exists(cvs_path):
    print 'Unzipping CVS module'
    execute(['unzip', '-q', zip_path, '-d', cvs_path], base_path)

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
      '--blobfile', cvs2git_blob_path,
      '--dumpfile', cvs2git_dump_path,
      '--username', 'chhoffme',
      '--encoding', 'windows-1252',
      cvs_path], base_path)

    print 'Importing to GIT repository'
    os.makedirs(git_path)
    execute(["git", "init"], git_path)
    p1 = subprocess.Popen(["cat", cvs2git_blob_path, cvs2git_dump_path], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(["git", "fast-import"], stdin=p1.stdout, cwd=git_path)
    p2.communicate()
    execute(["git", "checkout"], git_path)

def main():
  global base_path

  for f in os.listdir('%s/modules' % base_path):
    module_name, ext = os.path.splitext(f)
    if ext == '.zip':
      zip_path = os.path.join('%s/modules' % base_path, f)
      module_path = '%s/modules/%s' % (base_path, module_name)
      print '=== %s ===' % module_name
      cvs2git(zip_path, module_path)

main()

#!/usr/bin/python
# (Be in -*- mode: python; coding: utf-8 -*- mode.)

import os
import sys
import subprocess
import tempfile
import codecs

base_path = os.path.dirname(os.path.realpath('%s/..' % __file__))

def generate_config_file(tmpl_path, target_path, values, author_map):
  with codecs.open(tmpl_path, 'r', 'utf-8') as f: conf = f.read()
  for key in values: conf = conf.replace('$%s$' % key, values[key])
  author_str = "\n    ".join(map(lambda a: "'%s': (u'%s', '%s')," % (a, author_map[a][0], author_map[a][1]), author_map))
  conf = conf.replace('$author_map$', author_str)
  with codecs.open(target_path, 'w', 'utf-8') as f: f.write(conf)

def execute(cmd, cwd = None):
  subprocess.Popen(cmd, cwd=cwd).communicate()

def cvs2git(cvs_path, git_path, author_map):
  global base_path
  temp_blob_path = tempfile.mkstemp('-blob.dat')[1]
  temp_dump_path = tempfile.mkstemp('-dump.dat')[1]
  temp_conf_path = tempfile.mkstemp('-config.py')[1]

  generate_config_file('%s/config.tmpl.py' % base_path, temp_conf_path, {
    'blob_path': temp_blob_path,
    'dump_path': temp_dump_path,
    'cvs_path': cvs_path,
  }, author_map)

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
  execute(['cvs2git', '--options=%s' % temp_conf_path])

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
  author_map = {
    'user1': (u'First User', 'first.user@company.com'),
  }
  cvs2git(sys.argv[1], sys.argv[2], author_map)

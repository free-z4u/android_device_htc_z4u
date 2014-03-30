import re
import os
import shutil
import sys

pattern = re.compile(
    r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
    re.DOTALL | re.MULTILINE
)

pattern_white_space = re.compile(r'\s+')

def removeCCppComment(text):

    def replacer(match) :
        s = match.group(0)
        # Matched string is //...EOL or /*...*/  ==> Blot out all non-newline chars
        if s.startswith('/'):
            return ' '
        # Matched string is '...' or "..."  ==> Keep unchanged
        else:
            return s

    return re.sub(pattern, replacer, text)

def cleaupWhiteSpace(text):
    text = re.sub(pattern_white_space, '\n', text)
    return text.strip()

def file_hash(name):
    file_desc = open(name, 'r')
    with file_desc:
        text = removeCCppComment(file_desc.read())
        return cleaupWhiteSpace(text)

def process(to_dir, from_dir):
    for dirname, _, filenames in os.walk(from_dir):
        # print path to all filenames.
        for filename in filenames:
            if filename.endswith('.c') or filename.endswith('.h'):
                full_file = os.path.join(dirname, filename)
                origin_file = full_file.replace(from_dir, to_dir)
                if os.access(origin_file, os.R_OK):
                    statinfo_origin = os.stat(origin_file)
                    statinfo_new = os.stat(full_file)
                    if statinfo_new.st_size < statinfo_origin.st_size:
                        origin_file_hash = file_hash(origin_file)
                        new_file_hash = file_hash(full_file)
                        if new_file_hash == origin_file_hash:
                            shutil.copy2(origin_file, full_file)
                            print "copy %s => %s" % (origin_file, full_file)
                        else:
                            print "diff %s => %s" % (origin_file, full_file)
                    else:
                        print "same %s => %s" % (origin_file, full_file)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python restore.py linux-3.4 android_kernel_htc_z4u"
    else:
        process(sys.argv[1], sys.argv[2])

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

    def replacer(match):
        s = match.group(0)
        # Matched string is
        # //...EOL or /*...*/  ==> Blot out all non-newline chars
        if s.startswith('/'):
            return ' '
        # Matched string is '...' or "..."  ==> Keep unchanged
        else:
            return s

    return re.sub(pattern, replacer, text)


def get_hash(text, strip):
    cleaned_up_text = removeCCppComment(text)
    # drop whitespaces
    cleaned_up_text = re.sub(pattern_white_space, '\n', cleaned_up_text)
    if strip:
        # for compare case
        return cleaned_up_text.strip()
    else:
        # for search patern case
        return cleaned_up_text


def search_part_with_same_hash_head(text, hash, diff_len):
    stop = len(hash)
    # search start of magic
    start_hash = get_hash(text[:stop], False).strip()
    full_len = len(text) - diff_len
    while start_hash != hash:
        if full_len <= stop:
            return None
        last_stop = stop
        if len(hash) > len(start_hash):
            # try skip difference between hashes
            stop = stop + len(hash) - len(start_hash)
        else:
            if text[stop] not in ("/", "\n", "*"):
                for i in xrange(stop, len(text)):
                    if text[i] in ("/", "\n", "*"):
                        stop = i - 1
                        break
            # looks like not hashable
            stop = stop + 1
        start_hash = get_hash(text[:stop], False).strip()
        if start_hash[:len(hash)] == hash:
            # slowdown search
            stop = last_stop + 1
            start_hash = get_hash(text[:stop], False).strip()
        print "%d%%   \r" % (100 * stop / len(text)),
    return text[:stop]


def search_part_with_same_hash_tail(text, hash, diff_len):
    stop = len(text) - len(hash)
    # search start of magic
    start_hash = removeCCppComment(text[stop:])
    while start_hash.strip() != hash:
        if stop <= diff_len:
            return None
        if len(hash) > len(start_hash):
            # try skip difference between hashes
            stop = stop - (len(hash) - len(start_hash))
        else:
            # looks like not hashable
            stop = stop - 1
        start_hash = removeCCppComment(text[stop:])
        print "%d%%   \r" % (100 * stop / len(text)),
    return text[stop:]


def optimize_head(src_file, dst_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = src_desc.read()
    if not src_text:
        return
    dst_desc = open(dst_file, 'rb')
    with dst_desc:
        dst_text = dst_desc.read()
    if not dst_text:
        return
    src_hash = get_hash(src_text, True)
    dst_hash = get_hash(dst_text, True)
    common_hash = None
    for i in xrange(min(len(src_hash), len(dst_hash))):
        if src_hash[i] != dst_hash[i]:
            common_hash = src_hash[:i-1]
            break
    if common_hash:
        common_hash = common_hash.strip()
    while True:
        if common_hash:
            print "diff %s => %s: common head %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
            common_hash_dst = None
            common_hash_src = search_part_with_same_hash_head(
                src_text, common_hash,
                len(src_hash) - len(common_hash)
            )
            if common_hash_src:
                common_hash_dst = search_part_with_same_hash_head(
                    dst_text, common_hash,
                    len(dst_hash) - len(common_hash)
                )
            if common_hash_dst and common_hash_src:
                if len(common_hash_dst) < len(common_hash_src):
                    dst_desc = open(dst_file, 'wb')
                    with(dst_desc):
                        dst_desc.write(
                            common_hash_src + dst_text[len(common_hash_dst):]
                        )
                return
            # looks as too long hash
            found_something = False
            for i in xrange(1, len(common_hash)):
                if common_hash[-i] == "\n":
                    common_hash = common_hash[:-i].strip()
                    found_something = True
                    break
            if not found_something:
                print "diff %s => %s: No common head" % (
                    src_file, dst_file
                )
                return
            print "diff %s => %s: try shorter common head %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
        else:
            print "diff %s => %s: no common head" % (src_file, dst_file)
            return


def optimize_tail(src_file, dst_file):
    src_desc = open(src_file, 'rb')
    with src_desc:
        src_text = src_desc.read()
    if not src_text:
        return
    dst_desc = open(dst_file, 'rb')
    with dst_desc:
        dst_text = dst_desc.read()
    if not dst_text:
        return
    src_hash = removeCCppComment(src_text)
    dst_hash = removeCCppComment(dst_text)
    common_hash = None
    for i in xrange(1, min(len(src_hash), len(dst_hash))):
        if src_hash[-i] != dst_hash[-i]:
            common_hash = src_hash[-i + 1:]
            break
    while True:
        found_something = False
        if common_hash:
            if common_hash.index("\n") != -1:
                found_something = True
                common_hash = common_hash[common_hash.index("\n"):].strip()
        if common_hash:
            print "diff %s => %s: common tail %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
            common_hash_dst = None
            common_hash_src = search_part_with_same_hash_tail(
                src_text, common_hash,
                len(src_hash) - len(common_hash)
            )
            if common_hash_src:
                common_hash_dst = search_part_with_same_hash_tail(
                    dst_text, common_hash,
                    len(dst_hash) - len(common_hash)
                )
            if common_hash_dst and common_hash_src:
                if len(common_hash_dst) < len(common_hash_src):
                    dst_desc = open(dst_file, 'wb')
                    with(dst_desc):
                        dst_desc.write(
                            dst_text[:-len(common_hash_dst)] + common_hash_src
                        )
                return
            if not found_something:
                print "diff %s => %s: No common tail" % (
                    src_file, dst_file
                )
                return
            # looks as too long hash
            print "diff %s => %s: try shorter common tail %d%%" % (
                src_file, dst_file, 100 * len(common_hash) / len(dst_hash)
            )
        else:
            print "diff %s => %s: no comomn tail " % (src_file, dst_file)
            return


def file_hash(name):
    file_desc = open(name, 'rb')
    with file_desc:
        return get_hash(file_desc.read(), True)


def process_file(src_file, dst_file):
    if os.access(src_file, os.R_OK) and os.access(dst_file, os.R_OK):
        statinfo_origin = os.stat(src_file)
        statinfo_new = os.stat(dst_file)
        if statinfo_new.st_size < statinfo_origin.st_size:
            src_file_hash = file_hash(src_file)
            dst_file_hash = file_hash(dst_file)
            if dst_file_hash == src_file_hash:
                shutil.copy2(src_file, dst_file)
                print "copy %s => %s" % (src_file, dst_file)
            else:
                optimize_head(src_file, dst_file)
                optimize_tail(src_file, dst_file)
        else:
            print "same %s => %s" % (src_file, dst_file)


def process(src_inode, dst_inode):
    if os.path.isfile(dst_inode) and os.path.isfile(src_inode):
        process_file(src_inode, dst_inode)
    else:
        for dirname, _, filenames in os.walk(src_inode):
            # print path to all filenames.
            for filename in filenames:
                if filename.endswith('.c') or filename.endswith('.h'):
                    src_file = os.path.join(dirname, filename)
                    dst_file = src_file.replace(src_inode, dst_inode)
                    process_file(src_file, dst_file)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "usage: python restore.py linux-3.4 android_kernel_htc_z4u"
    else:
        process(sys.argv[1], sys.argv[2])

import argparse
import itertools
import os
import shutil
import stat
import sys
import time
from pathlib import Path

# default block size for -s option
BLOCK_SIZE = 1024

# setting constants for rows attributes formatting
# formatters should be called exactly the same as os.stat_results attributes.
# for those which are not, handlers should be defined in `REFORMAT` dictionary
ALL_FORMATTERS = (
    "st_ino",
    "size_in_blocks",
    "long_format",
)
LONG_FORMAT = (
    "mode",
    "st_nlink",
    "st_uid",
    "st_gid",
    "st_size",
    "date_time",
)
TIME_FORMAT = "%b %d %H:%M"

# for those columns which can't be used straight from os.stat_results object
# set up handler functions. Hope lambdas ok here as they aren't complicated
REFORMAT = {
    "mode": lambda x: stat.filemode(x.st_mode),
    "date_time": lambda x: time.strftime(TIME_FORMAT, time.localtime(x.st_ctime)),
    "size_in_blocks": lambda x: x.st_size // BLOCK_SIZE,
    # pwd works o Unix only so not sure it's a good idea to implement it here
    # 'st_uid': lambda x: pwd.getpwuid(x.st_uid).pwname
}

# the main code goes here. It is not split into functions and I'm sorry about it
# working on it in some time crunch
parser = argparse.ArgumentParser(description="Emulating Unix ls shell command")

# filter flags
parser.add_argument(
    "dir", nargs="?", default=".", help="Directory to explore (default: current)"
)
parser.add_argument(
    "-a",
    "--all",
    dest="all_items",
    action="store_true",
    default=False,
    help="Show hiddden items (default: False)",
)

# formatter flags
parser.add_argument(
    "-l",
    dest="long_format",
    action="store_true",
    default=False,
    help="Show detailed description (default: False)",
)
parser.add_argument(
    "-s",
    "--size",
    dest="size_in_blocks",
    action="store_true",
    default=False,
    help=f"Show size in blocks of {BLOCK_SIZE} bytes (default: False)",
)
parser.add_argument(
    "-i",
    "--inode",
    dest="st_ino",
    action="store_true",
    default=False,
    help="Show inode (serial number) (default: False)",
)

# printing flags
parser.add_argument(
    "-1",
    dest="per_line",
    default=False,
    action="store_true",
    help="Force one item per line (default: False)",
)

args = parser.parse_args()

# set up path
path = Path(args.dir)

# detect if it's a path was provided or a regexp (eg *.txt with a wildcard)
if not os.path.exists(args.dir):
    items = Path(".").glob(args.dir)
else:
    items = path.iterdir()

# filter all items by applying list of filters
if not args.all_items:
    items = (i for i in items if not i.name.startswith("."))

# turn from generator to regular list
items = list(items)

# nothing to handle
if not items:
    sys.exit(0)

# later we'll be able to use args.per_line to identify if only one column used
args.per_line = args.per_line or args.long_format

# define which formatters were provided from args
# vars(args) is a dictionary. We access to bool values in 'if'
formatters = [formatter for formatter in ALL_FORMATTERS if vars(args)[formatter]]

# as -l flag is a complex one we have to process it separately
# injecting needed columns by replacing `long_format` with them
if args.long_format:
    ind = formatters.index("long_format")
    formatters = formatters[:ind] + list(LONG_FORMAT) + formatters[ind + 1 :]

# this one is the most complicated part
# for each item (aka file or dir) - get stats. for those which can be used straight
# get appropriate formatter. For the rest, call appropriate re-format handler
# lastly, add file name
items_str = []
for item in items:
    item_stat = item.stat()
    items_str.append(
        [
            str(getattr(item_stat, formatter))
            if formatter not in REFORMAT
            else str(REFORMAT[formatter](item_stat))
            for formatter in formatters
        ]
        + [item.name]
    )

# check longest values in each column
longest = [max(len(v) for v in col) for col in zip(*items_str)]

# left aligning has to be changed to right for numeric types
# it is difficult to do which shows that program is not decoupled/extensible
str_format = "  ".join(["{:<" + str(l) + "}" for l in longest])

# transform list of lists in list of strings (merging columns)
formatted_rows = [str_format.format(*row) for row in items_str]

# easy part - render in one column
print("total", len(formatted_rows))
if args.per_line:
    for row in formatted_rows:
        print(row)
    sys.exit(0)

# not that easy part
longest = max(len(row) for row in formatted_rows)

# get terminal window width
terminal_size = shutil.get_terminal_size()
cols, rows = terminal_size.columns, terminal_size.lines

# calculate number of columns we can render
num_cols = cols // (longest + 2)
per_col = len(formatted_rows) // num_cols

# split so that sorting is vertical (by default -C option)
splitted = []
for i in range(0, len(formatted_rows), per_col):
    splitted.append(formatted_rows[i : i + per_col])

# merge back and show
for i in itertools.zip_longest(*splitted, fillvalue=""):
    print("  ".join(i))

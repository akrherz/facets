"""Fill single nan entries with previous row."""
import os
import glob
import sys


def main(argv):
    """Go Main Go."""
    os.chdir(argv[1])
    for subdir in ["temperature", "precipitation"]:
        os.chdir(subdir)
        for fn in glob.glob("*.txt"):
            data = open(fn).read()
            with open(fn, 'w') as fh:
                previous = ""
                for line in data.split("\n"):
                    if previous != "":
                        fh.write("\n")
                    if line.find("nan") > -1:
                        fh.write(previous)
                    else:
                        fh.write(line)
                    previous = line
        os.chdir("..")


if __name__ == "__main__":
    main(sys.argv)


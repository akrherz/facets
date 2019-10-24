"""Sometimes we get nan values."""
import os
import glob

from tqdm import tqdm


def main():
    """Go Main Go."""
    os.chdir("swatfiles")
    for mydir in ['temperature', 'precipitation']:
        os.chdir(mydir)
        pbar = tqdm(glob.glob("*.txt"))
        for fn in pbar:
            pbar.set_description(fn)
            tmpfn = '%s.tmp' % (fn, )
            with open(tmpfn, 'w') as fh:
                lastline = ""
                for line in open(fn):
                    if line.find("nan") < 0:
                        fh.write(line)
                        lastline = line
                        continue
                    fh.write(lastline)
            os.rename(tmpfn, fn)
        os.chdir("..")


if __name__ == '__main__':
    main()

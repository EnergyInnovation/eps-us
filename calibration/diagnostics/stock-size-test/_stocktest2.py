import shutil, subprocess, sys
from pathlib import Path
repo = Path(__file__).resolve().parents[1]
bak = repo/'calibration/runs/_stocktest_backup'
live = {'SoCDTtiNTY-psgr.csv': repo/'InputData/trans/SoCDTtiNTY/SoCDTtiNTY-psgr.csv',
        'SoCDTtiNTY-frgt.csv': repo/'InputData/trans/SoCDTtiNTY/SoCDTtiNTY-frgt.csv',
        'ANVCV-psgr.csv': repo/'InputData/trans/ANVCV/ANVCV-psgr.csv',
        'ANVCV-frgt.csv': repo/'InputData/trans/ANVCV/ANVCV-frgt.csv'}
pinned = repo/'calibration/runs/_stocktest_pinned_backup'; pinned.mkdir(exist_ok=True)
for n,p in live.items(): shutil.copy(p, pinned/n)          # save pinned (current) inputs
def run(name):
    r = subprocess.run([sys.executable, str(repo/'calibration/run_bau_export.py'), '--name', name,
                        '--savelist', 'calibration/_stocktest2.lst'], cwd=repo, capture_output=True, text=True)
    print(r.stdout[-300:], r.stderr[-800:]); r.check_returncode()
try:
    run('stocktest2_pinned')
    for n,p in live.items():                                 # original inputs = committed HEAD
        rel=p.relative_to(repo).as_posix()
        p.write_bytes(subprocess.run(['git','show',f'HEAD:{rel}'],cwd=repo,capture_output=True,check=True).stdout)
    run('stocktest2_original')
finally:
    for n,p in live.items(): shutil.copy(pinned/n, p)       # restore pinned
print('DONE, pinned inputs restored')

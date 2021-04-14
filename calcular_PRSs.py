#!/usr/bin/env python3
"""
Usage:
    calcular_PRSs.py --pheno-code CODE --plink-label LABEL [--max-threads N]

Options:
    --pheno-code=CODE    Código de fenotipo de UKBB.
    --plink-label=LABEL  Path + label hasta el dataset {bed,bim,fam} de PLINK
                         con los genotipos (sin .bed).
    --max-threads=N      Máximo de threads que usará LDAK. [default: 2]
"""

from os.path import basename, dirname
from os import makedirs

from docopt import docopt

from helpers import (
    download_url_to,
    make_executable,
    file_is_present,
    run_shell_command,
    gunzip,
    gzip,
)


host = "http://biocodices.hopto.org/public/tesis_juan"

def code2pheno(code):
    pheno_codes_fp = f"data/ukbb_phenotypes.phenotype-codes.tsv"

    with open(pheno_codes_fp) as f:
        lines = [l.strip().split("\t") for l in f]

    phenos = {l[1]: l[0] for l in lines}
    return phenos[code]


def main(ukbb_pheno_code, plink_label, max_threads):
    model = "bayesr"
    out_label = f"results/{ukbb_pheno_code}.{model}"
    out_profile_fp = f"{out_label}.profile"

    file_is_present(out_profile_fp) and exit()

    ldak_exec = f"software/ldak5.1.linux.fast"
    make_executable(ldak_exec)

    # get effect sizes file for the chosen phenotype
    pheno = code2pheno(ukbb_pheno_code)
    effects_gz_url = f"{host}/LDAK_effects/{pheno}.{model}.effects.best.gz"
    effects_gz_fp = f"data/{basename(effects_gz_url)}"
    download_url_to(effects_gz_url, effects_gz_fp)
    gunzip(effects_gz_fp)
    effects_fp = effects_gz_fp.replace(".gz", "")

    # compute the PRSs
    makedirs(dirname(out_label), exist_ok=True)
    command = (
        f"{ldak_exec} \\\n" +
        f"\t --calc-scores {out_label} \\\n"
        f"\t --bfile {plink_label} \\\n"
        f"\t --scorefile {effects_fp} \\\n"
        f"\t --power 0 \\\n"
        f"\t --max-threads {max_threads} | \\\n"
        f"\t tee {out_label}.log"
    )
    run_shell_command(command)

    # cleanup
    gzip(effects_fp)
    gzip(out_profile_fp)


if __name__ == "__main__":
    args = docopt(__doc__)
    main(
        ukbb_pheno_code=args["--pheno-code"],
        plink_label=args["--plink-label"],
        max_threads=args["--max-threads"],
    )

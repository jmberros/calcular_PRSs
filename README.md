# Calcular PRSs

Clonar este repo:

```bash
git clone https://github.com/jmberros/calcular_PRSs.git
```

Instalar los requisitos (usando Python 3.6 o superior):

```bash
cd calcular_PRSs
pip install -r requirements.txt
```

Asegurarse de tener un PLINK dataset `{bed,bim,fam}` con los ~6M genotipos de
la lista `data/all_predictors.tsv.gz`. En el `.bim`, los SNPs deben estar
nombrados como `CHROM:POS`, al igual que en la lista mencionada.

Calcular los PRSs así:

```bash
./calcular_PRS.py --pheno-code <CODE> --plink-label <LABEL> --max-threads 12
```

  * Los códigos de fenotipo UKBB disponibles están en `data/ukbb_phenotypes.phenotype-codes.tsv`. Por ejemplo, `K11_COELIAC` es celiaquía.
  * El `<LABEL>` del dataset de Plink debe ir sin `.bed`.
  * `--max-threads` controla el máximo de threads que usará LDAK.

Si todo sale bien, los archivos `.profile.gz` se generarán en `results/`.

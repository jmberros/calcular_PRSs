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
la lista `data/variants_for_LDAK.tsv.gz`. Debe cumplir que:

  * En el `.bim`, los SNPs deben estar nombrados como `CHROM:POS`, al igual que
    el campo `predictor` del archivo `data/variants_for_LDAK.tsv.gz`. PLINK2
    tiene una opción `--set-all-var-ids '@:#'` para esto
    (https://www.cog-genomics.org/plink/2.0/data#set_all_var_ids)
  * Sólo SNPs autosómicos. (Creo que acepta X Y MT pero en versión numérica,
    23, 24, 25 respectivamente. Más fácil quitarlos, pues los PRS que
    calcularemos no los incluyen.)
  * No debe haber SNPs duplicados. PLINK2 tiene `--rm-dup exclude-all` para
    resolverlo rápido. Tip: hacerlo luego de setear los IDs como CHROM:POS.
    (https://www.cog-genomics.org/plink/2.0/filter#rm_dup)
  * El campo de centimorgans parece ser opcional, en el `.bim` pueden ser todos
    `0`.

Si algo no está bien, LDAK mismo se quejará y se verá en el output, que suele
ser bastante claro.

Cuando ese dataset esté generado, se pueden calcular los PRSs así:

```bash
./calcular_PRSs.py --pheno-code <CODE> --plink-label <LABEL> --max-threads <N>
```

Por ejemplo, si el dataset PLINK está en `/datasets/EUR.{bed,bim,fam}` y nos
interesa calcular PRSs de Celiaquía (código: `K11_COELIAC`) usando `4` threads,
correríamos:

```bash
./calcular_PRSs.py --pheno-code K11_COELIAC --plink-label /datasets/EUR --max-threads 4
```

Si todo sale bien, los archivos `.profile.gz` se generarán en un nuevo
directorio de `results/`.

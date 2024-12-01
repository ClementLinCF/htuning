
# prerequres
# pip install pandas
# pip install openpyxl
# pip install tqdm

#!/bin/bash
if [ "$#" -lt 3 ]; then
    echo "Usage: $0 <rocm_bin_path> <training GPU devices> <assign the verified GPU device>"
    echo "Example: $0 /opt/rocm-6.3.0.1/bin \"8 9 10 11\" 11"
    exit 1
fi

ROCM_BIN_PATH="$1"
P_NUMBERS="$2"
LAST_P_NUMBER_PARAM="$3"

python tuned_before.py hipblaslt.log > shape_out.log
python runall_untuned.py shape_out.log untuned.csv "$ROCM_BIN_PATH" "$LAST_P_NUMBER_PARAM"
python alltuning.py shape_out.log "$ROCM_BIN_PATH\/" -p $P_NUMBERS

python merge_tuned.py
export HIPBLASLT_TUNING_OVERRIDE_FILE=tuning.txt
python aftertuning.py shape_out.log tuned.csv "$LAST_P_NUMBER_PARAM" "$ROCM_BIN_PATH\/"

python compare_tuned.py
python getftuning.py


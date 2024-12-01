import pandas as pd

def remove_negative_rows_from_tuning(comparison_file, tuning_file, output_file):
    improve_df = pd.read_excel(comparison_file, sheet_name="improve", engine="openpyxl")

    negative_rows = improve_df[
        (improve_df["Gflops improve (%)"] < 0) |
        (improve_df["GB/s improve (%)"] < 0) |
        (improve_df["us decrease (%)"] < 0)
    ][["transA", "transB", "m", "n", "k"]]

    with open(tuning_file, "r") as file:
        tuning_lines = file.readlines()

    updated_lines = []
    for line in tuning_lines:
        fields = line.strip().split(",")
        if len(fields) < 7:
            updated_lines.append(line)
            continue

        transA = str(fields[0]).strip()
        transB = str(fields[1]).strip()
        m = str(fields[4]).strip()
        n = str(fields[5]).strip()
        k = str(fields[6]).strip()

        match = negative_rows[
            (negative_rows["transA"].str.strip() == transA) &
            (negative_rows["transB"].str.strip() == transB) &
            (negative_rows["m"].astype(str).str.strip() == m) &
            (negative_rows["n"].astype(str).str.strip() == n) & 
            (negative_rows["k"].astype(str).str.strip() == k)
        ]

        if match.empty:
            updated_lines.append(line)

    with open(output_file, "w") as file:
        file.writelines(updated_lines)

    print(f"Updated tuning file saved as: {output_file}")

if __name__ == "__main__":
    comparison_file = "comparison.xlsx"
    tuning_file = "tuning.txt"
    output_file = "ftuning.txt"

    remove_negative_rows_from_tuning(comparison_file, tuning_file, output_file)


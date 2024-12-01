import pandas as pd
import numpy as np
import os
from openpyxl import load_workbook

def adjust_column_widths(workbook, sheet_name):
    sheet = workbook[sheet_name]
    for column in sheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        adjusted_width = max_length + 2
        sheet.column_dimensions[column_letter].width = adjusted_width

def generate_excel(untuned_file, tuned_file, output_file):
    untuned_df = pd.read_csv(untuned_file)
    tuned_df = pd.read_csv(tuned_file)

    key_columns = ['transA', 'transB', 'm', 'n', 'k']

    untuned_keys = untuned_df[key_columns].copy()
    tuned_keys = tuned_df[key_columns].copy()

    untuned_keys['m'] = untuned_keys['m'].astype(int)
    untuned_keys['n'] = untuned_keys['n'].astype(int)
    untuned_keys['k'] = untuned_keys['k'].astype(int)
    tuned_keys['m'] = tuned_keys['m'].astype(int)
    tuned_keys['n'] = tuned_keys['n'].astype(int)
    tuned_keys['k'] = tuned_keys['k'].astype(int)

    untuned_keys[['transA', 'transB']] = untuned_keys[['transA', 'transB']].apply(lambda col: col.str.strip())
    tuned_keys[['transA', 'transB']] = tuned_keys[['transA', 'transB']].apply(lambda col: col.str.strip())

    if not untuned_keys.reset_index(drop=True).equals(tuned_keys.reset_index(drop=True)):
        raise ValueError("The keys (transA, transB, m, n, k) in untuned and tuned files do not match!")

    improve_df = untuned_df[key_columns].copy()
    improve_df['Gflops improve (%)'] = (
        (tuned_df['hipblaslt-Gflops'] - untuned_df['hipblaslt-Gflops']) / untuned_df['hipblaslt-Gflops'] * 100
    ).round(2)
    improve_df['GB/s improve (%)'] = (
        (tuned_df['hipblaslt-GB/s'] - untuned_df['hipblaslt-GB/s']) / untuned_df['hipblaslt-GB/s'] * 100
    ).round(2)
    improve_df['us decrease (%)'] = (
        (untuned_df['us'] - tuned_df['us']) / untuned_df['us'] * 100
    ).round(2)

    final_improve_df = improve_df[
        (improve_df['Gflops improve (%)'] >= 0) &
        (improve_df['GB/s improve (%)'] >= 0) &
        (improve_df['us decrease (%)'] >= 0)
    ].reset_index(drop=True)

    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        untuned_df.to_excel(writer, sheet_name="untuned", index=False)
        tuned_df.to_excel(writer, sheet_name="tuned", index=False)
        improve_df.to_excel(writer, sheet_name="improve", index=False)
        final_improve_df.to_excel(writer, sheet_name="final_improve", index=False)

    workbook = load_workbook(output_file)
    for sheet in ["untuned", "tuned", "improve", "final_improve"]:
        adjust_column_widths(workbook, sheet)
    workbook.save(output_file)

    print(f"Excel file generated successfully: {output_file}")


if __name__ == "__main__":
    untuned_file = "untuned.csv"
    tuned_file = "tuned.csv"
    output_file = "comparison.xlsx"

    if not os.path.exists(untuned_file):
        raise FileNotFoundError(f"File not found: {untuned_file}")
    if not os.path.exists(tuned_file):
        raise FileNotFoundError(f"File not found: {tuned_file}")

    generate_excel(untuned_file, tuned_file, output_file)


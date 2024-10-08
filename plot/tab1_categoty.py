import os
import numpy as np
import pandas as pd
from utils.parse_xls import parse_xls, TURN_NUMBER

row_margins = 2.0, 1.5
def number_mapper(x, col_id):
    if col_id == 2:
        return f'{x:.2f}'
    else:
        return str(int(x))

def get_data(key):
    res = np.zeros((3, 4))
    
    try:
        df = parse_xls(key)
    except Exception as e:
        print(f'Error: {e}, when reading {key}')
        return res
    
    for index, row in df.iterrows():
        text = row['评判结果']
        base = 1 if row['multi_rounds_related'] else 0
        res[base, (0 if row['alignment'] == 'align' else 1)] += 1
        res[base, 2] += text.count('约束')
        res[base, 3] += 1
    
    res[2] = res[0] + res[1]
    
    res[:, 2] /= res[:, 3]
    res[:, 3] /= TURN_NUMBER
    
    return res

BEFORE_TEX = r'''\begin{table}[t]
\centering
\small
\begin{tabular}{c|cccc}
    \toprule
        & Aligned & Misaligned & C. per I. & \# Session \\
    \midrule
'''
ATRER_TEX = r'''\bottomrule
\end{tabular}
\caption{Table 1}
\end{table}
'''

if __name__ == '__main__':
    data_table = get_data('GPT-4o')

    print(BEFORE_TEX)
    print("% ====<<<<==== Auto-generated LaTeX code begin ====>>>>==== %\n")
    print(f"% --- generated by {os.path.basename(__file__)} --- %\n")

    for i, key in enumerate(['Parallel', 'Dependent', 'Total']):
        print(r'\rule{0pt}{' + str(row_margins[1 if i == 1 else 0]) + r'ex}')
        print(f'{key} & ' 
            + ' & '.join([number_mapper(x, j) for j, x in enumerate(data_table[i])])
            + ' \\\\')
        if i == 1:
            print('\\hline')

    print("\n% ====<<<<==== Auto-generated LaTeX code end ====>>>>==== %")
    print(ATRER_TEX)
    
    # print(data_table)
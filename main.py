import numpy as np
import pandas as pd
from calculator import Calculator


def main():
    calc = Calculator()
    calc.calculate()
    tasks = []
    for mode in ['global', 'local']:
        for alg in ['opt', 'fifo']:
            seq = [[res] for res in calc.seq[mode][alg]]
            pages = calc.result[mode][alg]
            accuracy = calc.accuracy[mode][alg]
            for i in range(len(seq)):
                seq[i] += pages[i]
                seq[i].append(accuracy[i])
            data = np.array(seq).T
            index = ['Очередь'] + [i+1 for i in range(10)] + ['Попадание']
            tasks.append(pd.DataFrame(data, index=index,
                                      columns=[i+1 for i in range(len(calc.result['global'][alg]))]))
    with pd.ExcelWriter('output.xlsx') as writer:
        tasks[0].to_excel(writer, sheet_name='Global Optimal')
        tasks[1].to_excel(writer, sheet_name='Global FIFO')
        tasks[2].to_excel(writer, sheet_name='Local Optimal')
        tasks[3].to_excel(writer, sheet_name='local FIFO')


if __name__ == '__main__':
    main()

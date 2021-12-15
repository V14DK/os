import copy
import pandas as pd
import numpy as np


class Calculator:
    def __init__(self):
        self.chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.people = ['Ильин Станислав Павлович',
                       'Карманов Владислав Игоревич',
                       'Карцева Арина Олеговна']
        self.algorithms = {'opt': self.__opt, 'fifo': self.__fifo}
        self.opt_time = {'global': {}, 'local': {}}
        self.fifo_queue = {'global': [], 'local': []}
        self.seq = {'global': {'opt': [], 'fifo': []},
                    'local':  {'opt': [], 'fifo': []}}
        self.cur_page = {'global': {'opt': {}, 'fifo': {}},
                         'local':  {'opt': {}, 'fifo': {}}}
        self.digits = {'global': {'opt': [], 'fifo': []},
                       'local': {'opt': [], 'fifo': []}}
        self.accuracy = {'global': {'opt': [], 'fifo': []},
                         'local': {'opt': [], 'fifo': []}}
        self.result = {'global': {'opt': [], 'fifo': []},
                       'local': {'opt': [], 'fifo': []}}
        self.n = []

    def __preparations(self):
        self.n = [len(man.split()[1]) for man in self.people]
        self.people = [''.join(man.lower().split()) for man in self.people]
        data = {self.chars[i]: str(i+1)+', ' for i in range(len(self.chars))}
        t = [man.maketrans(data) for man in self.people]
        self.digits['global']['opt'] = [self.people[i].translate(t[i]) for i
                                        in range(len(self.people))]
        self.digits['global']['opt'] = [digit.split(', ') for digit
                                        in self.digits['global']['opt']]
        for i in range(len(self.digits['global']['opt'])):
            self.digits['global']['opt'][i] = [int(digit) % self.n[i]
                                               for digit in self.digits['global']['opt'][i]
                                               if digit and int(digit) % self.n[i] != 0]
        self.digits['global']['fifo'] = copy.deepcopy(self.digits['global']['opt'])
        self.digits['local']['opt'] = copy.deepcopy(self.digits['global']['opt'])
        self.digits['local']['fifo'] = copy.deepcopy(self.digits['global']['opt'])
        self.people = [list(self.people[i]) for i in range(len(self.people))]

    def __start(self, mode, alg):
        i = 1
        while self.digits[mode][alg] != [[], [], []]:
            for index in range(len(self.digits[mode][alg])):
                try:
                    cur = str(index + 1) + '-' + str(self.digits[mode][alg][index].pop(0))
                except:
                    continue
                self.seq[mode][alg].append(cur)
                i = self.algorithms[alg](mode, alg, cur, i)

    def __opt(self, mode, alg, cur, i):
        opt_time = self.opt_time[mode]
        cur_page = self.cur_page[mode][alg]
        acc = self.accuracy[mode][alg]
        for key in opt_time:
            opt_time[key] += 1
        if cur not in cur_page:
            if len(cur_page) == 10:
                m = max(opt_time.items(), key=lambda pair: pair[1])
                page = cur_page[m[0]]
                del cur_page[m[0]], opt_time[m[0]]
                cur_page[cur] = page
                opt_time[cur] = 0
                acc.append(False)
            else:
                cur_page[cur] = i
                opt_time[cur] = 0
                i = len(cur_page) + 1
                acc.append(None)
        else:
            opt_time[cur] = 0
            acc.append(True)
            if len(cur_page) < 10:
                i = len(cur_page) + 1
        self.result[mode][alg].append([pair[0] for pair in sorted(cur_page.items(), key=lambda pair: pair[1])])
        return i

    def __fifo(self, mode, alg, cur, i):
        fifo_queue = self.fifo_queue[mode]
        cur_page = self.cur_page[mode][alg]
        acc = self.accuracy[mode][alg]
        if cur not in cur_page:
            if len(cur_page) == 10:
                m = fifo_queue.pop(0)
                page = cur_page[m]
                del cur_page[m]
                cur_page[cur] = page
                fifo_queue.append(cur)
                acc.append(False)
            else:
                cur_page[cur] = i
                fifo_queue.append(cur)
                i = len(cur_page) + 1
                acc.append(None)
        else:
            acc.append(True)
            if len(cur_page) == 10:
                fifo_queue.remove(cur)
                fifo_queue.append(cur)
            else:
                i = len(cur_page) + 1
        self.result[mode][alg].append([pair[0] for pair in sorted(cur_page.items(), key=lambda pair: pair[1])])
        return i

    def calculate(self):
        self.__preparations()
        self.__start('global', 'opt')
        self.__start('global', 'fifo')


calc = Calculator()
calc.calculate()
for alg in ['opt', 'fifo']:
    for res in calc.result['global'][alg]:
        while len(res) < 10:
            res.append(None)
task1 = []
for alg in ['opt', 'fifo']:
    seq = [[res] for res in calc.seq['global'][alg]]
    pages = calc.result['global'][alg]
    accuracy = calc.accuracy['global'][alg]
    for i in range(len(seq)):
        seq[i] += pages[i]
        seq[i].append(accuracy[i])
    data = np.array(seq).T
    index = ['Очередь'] + [i+1 for i in range(10)] + ['Попадание']
    task1.append(pd.DataFrame(data, index=index,
                             columns=[i+1 for i in range(len(calc.result['global'][alg]))]))
with pd.ExcelWriter('output.xlsx') as writer:
    task1[0].to_excel(writer, sheet_name='Optimal')
    task1[1].to_excel(writer, sheet_name='FIFO')
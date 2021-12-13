import copy


class Calculator:
    def __init__(self):
        self.chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.people = ['Ильин Станислав Павлович',
                       'Карманов Владислав Игоревич',
                       'Карцева Арина Олеговна']
        self.algorithms = {'opt': self.__opt, 'fifo': self.__fifo}
        self.sequence = {'global': {'opt': [], 'fifo': []},
                         'local':  {'opt': [], 'fifo': []}}
        self.pages = {'global': {'opt': [], 'fifo': []},
                      'local':  {'opt': [], 'fifo': []}}
        self.digits = {'global': {'opt': [], 'fifo': []},
                       'local': {'opt': [], 'fifo': []}}
        self.accuracy = {'global': {'opt': [], 'fifo': []},
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
        i = 0
        while self.digits[mode][alg] != [[], [], []]:
            for index in range(3):
                try:
                    cur = '{}-{}'.format(index + 1, self.digits[mode][alg][index].pop(0))
                except:
                    continue
                if alg == 'opt':
                    self.pages[mode][alg].append({})
                else:
                    self.pages[mode][alg].append([])
                self.sequence[mode][alg].append(cur)
                if i > 0:
                    self.pages[mode][alg][i] = copy.copy(self.pages[mode][alg][i - 1])
                i = self.algorithms[alg](mode, i, cur)

    def __opt(self, mode, i, cur):
        for key in self.pages[mode]['opt'][i]:
            self.pages[mode]['opt'][i][key] += 1
        if cur not in self.pages[mode]['opt'][i]:
            if len(self.pages[mode]['opt'][i]) == 10:
                self.accuracy[mode]['opt'].append(False)
                if mode == 'global':
                    m = max(self.pages[mode]['opt'][i].items(), key=lambda page: page[1])
                    del self.pages[mode]['opt'][i][m[0]]
                else:
                    proc = list(filter(lambda kv: kv[0][0] == cur[0], self.pages[mode]['opt'][i].items()))
                    m = max(proc, key=lambda pair: pair[1])
                    del self.pages[mode]['opt'][i][m[0]]
            else:
                self.accuracy[mode]['opt'].append(None)
        else:
            self.accuracy[mode]['opt'].append(True)
        self.pages[mode]['opt'][i][cur] = 0
        return i + 1

    def __fifo(self, mode, i, cur):
        print('cur', cur)
        if cur not in self.pages[mode]['fifo'][i]:
            if len(self.pages[mode]['fifo'][i]) == 10:
                self.accuracy[mode]['fifo'].append(False)
                if mode == 'global':
                    self.pages[mode]['fifo'][i].pop(0)
                else:
                    #TODO сделать изменение страниц на месте, а не путем удаления первого вхождения и добавления в конец нового элемента
                    proc = list(filter(lambda x: x[0] == cur[0], self.pages[mode]['fifo'][i]))
                    m = proc[0]
                    # id = self.pages[mode]['fifo'][i].index(m)
                    print('m', m)
                    print(self.pages[mode]['fifo'][i])
                    self.pages[mode]['fifo'][i].remove(m)
            else:
                self.accuracy[mode]['fifo'].append(None)
            self.pages[mode]['fifo'][i].append(cur)
            print(self.pages[mode]['fifo'][i])
        else:
            self.accuracy[mode]['fifo'].append(True)
        return i + 1

    def calculate(self):
        self.__preparations()
        # self.__start('global', 'opt')
        self.__start('local', 'fifo')


calc = Calculator()
calc.calculate()
print(calc.sequence)
import copy


class Calculator:
    def __init__(self):
        self.chars = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        self.people = ['Ильин Станислав Павлович',
                       'Карманов Владислав Игоревич',
                       'Карцева Арина Олеговна']
        self.seq = []
        self.cur_time = {}
        self.cur_page = {}
        # self.algorithms = {'opt': self.__opt, 'fifo': self.__fifo}
        # self.sequence = {'global': {'opt': [], 'fifo': []},
        #                  'local':  {'opt': [], 'fifo': []}}
        # self.pages = {'global': {'opt': [], 'fifo': []},
        #               'local':  {'opt': [], 'fifo': []}}
        self.digits = {'global': {'opt': [], 'fifo': []},
                       'local': {'opt': [], 'fifo': []}}
        # self.accuracy = {'global': {'opt': [], 'fifo': []},
        #                  'local': {'opt': [], 'fifo': []}}
        self.result = []
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

    def opt(self, mode, alg):
        i = 1
        while self.digits[mode][alg] != [[], [], []]:
            for index in range(len(self.digits[mode][alg])):
                try:
                    cur = str(index+1) + '-' + str(self.digits[mode][alg][index].pop(0))
                except:
                    continue
                self.seq.append(cur)
                for key in self.cur_time:
                    self.cur_time[key] += 1
                if cur not in self.cur_page:
                    if len(self.cur_page) == 10:
                        m = max(self.cur_time.items(), key=lambda pair: pair[1])
                        page = self.cur_page[m[0]]
                        del self.cur_page[m[0]], self.cur_time[m[0]]
                        self.cur_page[cur] = page
                        self.cur_time[cur] = 0

                    else:
                        self.cur_page[cur] = i
                        self.cur_time[cur] = 0
                        i = len(self.cur_page) + 1
                else:
                    self.cur_time[cur] = 0
                    if len(self.cur_page) < 10:
                        i = len(self.cur_page) + 1
                self.result.append([pair[0] for pair in sorted(self.cur_page.items(), key=lambda pair: pair[1])])

    def fifo(self, mode, alg):
        i = 1
        while self.digits[mode][alg] != [[], [], []]:
            for index in range(len(self.digits[mode][alg])):
                try:
                    cur = str(index + 1) + '-' + str(self.digits[mode][alg][index].pop(0))
                except:
                    continue
                self.seq.append(cur)


    # def __start(self, mode, alg):
    #     i = 0
    #     while self.digits[mode][alg] != [[], [], []]:
    #         for index in range(3):
    #             try:
    #                 cur = '{}-{}'.format(index + 1, self.digits[mode][alg][index].pop(0))
    #             except:
    #                 continue
    #             if alg == 'opt':
    #                 self.pages[mode][alg].append({})
    #             else:
    #                 self.pages[mode][alg].append([])
    #             self.sequence[mode][alg].append(cur)
    #             if i > 0:
    #                 self.pages[mode][alg][i] = self.pages[mode][alg][i - 1]
    #             i = self.algorithms[alg](mode, i, cur)

    # def __opt(self, mode, i, cur):
    #     for key in self.pages[mode]['opt'][i]:
    #         self.pages[mode]['opt'][i][key] += 1
    #     if cur not in self.pages[mode]['opt'][i]:
    #         if len(self.pages[mode]['opt'][i]) == 10:
    #             self.accuracy[mode]['opt'].append(False)
    #             if mode == 'global':
    #                 m = max(self.pages[mode]['opt'][i].items(), key=lambda page: page[1])
    #                 del self.pages[mode]['opt'][i][m[0]]
    #             else:
    #                 proc = list(filter(lambda kv: kv[0][0] == cur[0], self.pages[mode]['opt'][i].items()))
    #                 m = max(proc, key=lambda pair: pair[1])
    #                 del self.pages[mode]['opt'][i][m[0]]
    #         else:
    #             self.accuracy[mode]['opt'].append(None)
    #     else:
    #         self.accuracy[mode]['opt'].append(True)
    #     self.pages[mode]['opt'][i][cur] = 0
    #     self.[]
    #     print(self.pages[mode]['opt'][i])
    #     return i + 1

    # def __fifo(self, mode, i, cur):
    #     if cur not in self.pages[mode]['fifo'][i]:
    #         if len(self.pages[mode]['fifo'][i]) == 10:
    #             self.accuracy[mode]['fifo'].append(False)
    #             if mode == 'global':
    #                 self.pages[mode]['fifo'][i].pop(0)
    #             else:
    #                 #TODO сделать изменение страниц на месте, а не путем удаления первого вхождения и добавления в конец нового элемента
    #                 proc = list(filter(lambda x: x[0] == cur[0], self.pages[mode]['fifo'][i]))
    #                 m = proc[0]
    #                 self.pages[mode]['fifo'][i].remove(m)
    #         else:
    #             self.accuracy[mode]['fifo'].append(None)
    #         self.pages[mode]['fifo'][i].append(cur)
    #     else:
    #         self.accuracy[mode]['fifo'].append(True)
    #     return i + 1

    def calculate(self):
        self.__preparations()
        self.opt('global', 'opt')
        # self.__start('global', 'opt')
        # self.__start('local', 'fifo')


calc = Calculator()
calc.calculate()
for res in calc.result:
    print(res)
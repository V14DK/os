import copy


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
                    'local': {'opt': [], 'fifo': []}}
        self.cur_page = {'global': {'opt': {}, 'fifo': {}},
                         'local': {'opt': {}, 'fifo': {}}}
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
        data = {self.chars[i]: str(i + 1) + ', ' for i in range(len(self.chars))}
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
                acc.append(False)
                if mode == 'global':
                    m = max(opt_time.items(), key=lambda pair: pair[1])
                else:
                    proc = list(filter(lambda kv: kv[0][0] == cur[0],
                                       opt_time.items()))
                    m = max(proc, key=lambda pair: pair[1])
                page = cur_page[m[0]]
                del cur_page[m[0]], opt_time[m[0]]
                cur_page[cur] = page
            else:
                acc.append(None)
                cur_page[cur] = i
        else:
            acc.append(True)
        if len(cur_page) < 10:
            i = len(cur_page) + 1
        opt_time[cur] = 0
        self.result[mode][alg].append([pair[0] for pair
                                       in sorted(cur_page.items(),
                                                 key=lambda pair: pair[1])])
        return i

    def __fifo(self, mode, alg, cur, i):
        fifo_queue = self.fifo_queue[mode]
        cur_page = self.cur_page[mode][alg]
        acc = self.accuracy[mode][alg]
        if cur not in cur_page:
            if len(cur_page) == 10:
                acc.append(False)
                if mode == 'global':
                    m = fifo_queue.pop(0)
                else:
                    proc = list(filter(lambda x: x[0] == cur[0],
                                       fifo_queue))
                    m = proc[0]
                    fifo_queue.remove(m)
                page = cur_page[m]
                del cur_page[m]
                cur_page[cur] = page
            else:
                acc.append(None)
                cur_page[cur] = i
            fifo_queue.append(cur)
        else:
            acc.append(True)
            if len(cur_page) == 10:
                fifo_queue.remove(cur)
                fifo_queue.append(cur)
        if len(cur_page) < 10:
            i = len(cur_page) + 1
        self.result[mode][alg].append([pair[0] for pair
                                       in sorted(cur_page.items(),
                                                 key=lambda pair: pair[1])])
        return i

    def __last_preparations(self, mode, alg):
        for res in self.result[mode][alg]:
            while len(res) < 10:
                res.append(None)

    def calculate(self):
        self.__preparations()
        for mode in ['global', 'local']:
            for alg in ['opt', 'fifo']:
                self.__start(mode, alg)
                self.__last_preparations(mode, alg)

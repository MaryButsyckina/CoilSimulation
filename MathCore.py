import numpy as np
from functools import reduce


class Coil:
    def __init__(self, lay_num, turn_num, r_in, r_out, coef, mode='serial'):
        self.lay_num = lay_num
        self.turn_num = turn_num
        self.r_in = r_in
        self.r_out = r_out
        self.coef = coef
        self.mode = mode

    def calc_square(self, harm, length):
        if isinstance(self.r_in, list):
            s = 0
            for i in range(len(self.r_in)):
                s += self.r_out[i] ** harm - self.r_in[i] ** harm
            return s * self.lay_num * length / harm
        return (self.r_out ** harm - self.r_in ** harm) * self.lay_num * length / harm


class SextupleCoil:
    def __init__(self, coil):
        self.coil = coil

    def calc_square(self, harm, length):
        return self.coil.calc_square(harm, length)


class CompCoil:
    def __init__(self, *coils):
        self.coils = coils

    def calc_square(self, harm, length):
        square = 0
        for i in range(len(self.coils)):
            square += self.coils[i].calc_square(harm, length) * self.coils[i].coef
        return square

    def calc_coef(self):
        sum = reduce(lambda x, y: x.turn_nums + y.turn_nums, filter(lambda x: x.mode == 'parallel', self.coils))
        print(sum)
        for coil in self.coils:
            if coil.mode == 'serial':
                coil.coef = 1




class FLow:
    def __init__(self, field, length, r_ref, coil):
        self.field = field
        self.length = length
        self.r_ref = r_ref
        self.coil = coil

    def calc_flow(self):
        flow = [0 for _ in range(128)]
        for harm in self.field.keys():
            amp = self.count_harm_amp(harm)
            for k in range(128):
                flow[k] += amp * np.sin(k * 360 / 128 * np.pi / 180 * harm)
        return flow


    def count_harm_amp(self, harm):
        s = self.coil.calc_square(harm, self.length)
        amp = (self.field[harm] * s) / (40000 * self.r_ref ** (harm - 1))
        return amp


class EMF:
    def __init__(self, flow):
        self.flow = flow

    def calc_emf(self):
        emf = [self.flow[0]]
        for i in range(1, len(self.flow)):
            emf.append(self.flow[i] - self.flow[i-1])
        return emf

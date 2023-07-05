# import numpy as np
from MathCore import SextupleCoil, CompCoil, Coil, FLow, EMF
# from matplotlib import pyplot as plt


# def current_conf():
#     r_out = [0.011, 0.0114, 0.0118, 0.0122, 0.0126, 0.013, 0.0134]
#     r_out.reverse()
#     coil1 = Coil(12, 7, [0.0066, 0.0071, 0.0075, 0.0079, 0.0083, 0.0087, 0.0091], r_out, 1)
#     coil2 = Coil(9, 4, [0.0002, 0.0006, 0.001, 0.0014], [0.0085, 0.0081, 0.0077, 0.0073], 1)
#     coil3 = Coil(1, 3, [0.0002, 0.0006, 0.001], [0.0085, 0.0081, 0.0077], 1)
#     coil4 = Coil(12, 3, [0.0089, 0.0093, 0.0097], [0.0134, 0.013, 0.0126], -0.4)
#     coil5 = Coil(12, 2, [0.0002, 0.0006], [0.006, 0.0056], 0.6)
#     _half_coil = SextupleCoil(coil1)
#     _comp_coil = CompCoil(coil2, coil3, coil4, coil5)
#
#     _field = {1: 5.67, 2: 23.78, 3: 3117.9, 4: 7.55, 5: 1.6, 6: 0.26, 7: 0.306, 8: 0.39, 9: 0.094, 10: 0.051, 11: 0.034, 12: 0.033, 13: 0.077, 14: 0.16, 15: 2.71}
#     _length = 0.3
#     _r_ref = 0.01
#     _flow = FLow(_field, _length, _r_ref, half_coil).calc_flow()
#     _emf = EMF(_flow).calc_emf()
#     _flow1 = FLow(_field, _length, _r_ref, comp_coil).calc_flow()
#     _emf1 = EMF(flow1).calc_emf()
#     _comp_emf = (abs(max(_emf)) + abs(min(_emf))) / (abs(max(_emf1)) + abs(min(_emf1)))
#     _comp_flow = (abs(max(_flow)) + abs(min(_flow))) / (abs(max(_flow1)) + abs(min(_flow1)))
#     print('EMF 2:', max(_emf1), min(_emf1), (max(_emf1) - min(_emf1))/2)
#     print('EMF 0:', max(_emf), min(_emf), (max(_emf) - min(_emf))/2)
#     print('Flow 2:', max(_flow1), min(_flow1), (max(_flow1) - min(_flow1))/2)
#     print('Flow 0:', max(_flow), min(_flow), (max(_flow) - min(_flow))/2)
#     print("Compensation emf:", _comp_emf)
#     print("Compensation flow:", _comp_flow)


def change_s1_s3(_field, _length, _r_ref, r_outer_half, r_inner_half, r_outer_comp, r_inner_comp, comp_coef, coils_to_change, way='minus', mode='iter'):
    diff = 0.000001
    Diff = 0
    prev = 0

    while 1:
        coils_comp = []
        _half_coil = SextupleCoil(Coil(12, len(r_outer_half), r_inner_half, r_outer_half, 1))

        for _i in range(len(r_outer_comp)):
            coils_comp.append(Coil(12, len(r_outer_comp[_i]), r_inner_comp[_i], r_outer_comp[_i], comp_coef[_i]))
        _comp_coil = CompCoil(*coils_comp)

        _flow = FLow(_field, _length, _r_ref, _half_coil).calc_flow()
        _emf = EMF(_flow).calc_emf()
        _flow1 = FLow(_field, _length, _r_ref, _comp_coil).calc_flow()
        _emf1 = EMF(_flow1).calc_emf()
        _comp_emf = (abs(max(_emf)) + abs(min(_emf))) / (abs(max(_emf1)) + abs(min(_emf1)))
        _comp_flow = (abs(max(_flow)) + abs(min(_flow))) / (abs(max(_flow1)) + abs(min(_flow1)))
        if prev >= _comp_emf:
            if way == 'plus':
                for j in range(len(r_outer_comp[0])):
                    r_outer_comp[coils_to_change[0]][j] -= diff
                for j in range(len(r_outer_comp[1])):
                    r_inner_comp[coils_to_change[1]][j] -= diff
            else:
                for j in range(len(r_outer_comp[0])):
                    r_outer_comp[coils_to_change[0]][j] += diff
                for j in range(len(r_outer_comp[1])):
                    r_inner_comp[coils_to_change[1]][j] += diff
            break
        print('\nDIFF: ', Diff)
        print('EMF 2:', max(_emf1), min(_emf1), (max(_emf1) - min(_emf1)) / 2)
        print('EMF 0:', max(_emf), min(_emf), (max(_emf) - min(_emf)) / 2)
        print('Flow 2:', max(_flow1), min(_flow1), (max(_flow1) - min(_flow1)) / 2)
        print('Flow 0:', max(_flow), min(_flow), (max(_flow) - min(_flow)) / 2)
        print("Compensation emf:", _comp_emf)
        print("Compensation flow:", _comp_flow)
        print("r_out: ", r_outer_comp, "r_in: ", r_inner_comp)
        prev = _comp_emf
        Diff += diff
        if mode == 'once':
            return _comp_emf
        if way == 'plus':
            for j in range(len(r_outer_comp[0])):
                r_outer_comp[coils_to_change[0]][j] += diff
            for j in range(len(r_outer_comp[1])):
                r_inner_comp[coils_to_change[1]][j] += diff
        else:
            for j in range(len(r_outer_comp[0])):
                r_outer_comp[coils_to_change[0]][j] -= diff
            for j in range(len(r_outer_comp[1])):
                r_inner_comp[coils_to_change[1]][j] -= diff


# def change_s1(_field, _length, _r_ref, r_outer_half, r_inner_half, r_outer_comp, r_inner_comp, comp_coef, coils_to_change, way='minus', mode='iter'):
#     diff = 0.0001
#     Diff = 0
#     prev = 0
#
#     while 1:
#         coils_comp = []
#         _half_coil = SextupleCoil(Coil(12, len(r_outer_half), r_inner_half, r_outer_half, 1))
#
#         for _i in range(len(r_outer_comp)):
#             coils_comp.append(Coil(12, len(r_outer_comp[_i]), r_inner_comp[_i], r_outer_comp[_i], comp_coef[_i]))
#         _comp_coil = CompCoil(*coils_comp)
#
#         _flow = FLow(field, _length, _r_ref, half_coil).calc_flow()
#         _emf = EMF(flow).calc_emf()
#         _flow1 = FLow(field, _length, _r_ref, comp_coil).calc_flow()
#         _emf1 = EMF(_flow1).calc_emf()
#         _comp_emf = (abs(max(_emf)) + abs(min(_emf))) / (abs(max(_emf1)) + abs(min(_emf1)))
#         _comp_flow = (abs(max(flow)) + abs(min(flow))) / (abs(max(flow1)) + abs(min(flow1)))
#         if prev >= _comp_emf:
#             if way == 'plus':
#                 for j in range(len(r_outer_comp[coils_to_change[0]])):
#                     r_inner_comp[coils_to_change[0]][j] -= diff
#             else:
#                 for j in range(len(r_outer_comp[coils_to_change[0]])):
#                     r_inner_comp[coils_to_change[0]][j] += diff
#             break
#
#         print('\nDIFF: ', Diff)
#         print('EMF 2:', max(_emf1), min(_emf1), (max(_emf1) - min(_emf1)) / 2)
#         print('EMF 0:', max(_emf), min(_emf), (max(_emf) - min(_emf)) / 2)
#         print('Flow 2:', max(flow1), min(flow1), (max(flow1) - min(flow1)) / 2)
#         print('Flow 0:', max(flow), min(flow), (max(flow) - min(flow)) / 2)
#         print("Compensation emf:", _comp_emf)
#         print("Compensation flow:", _comp_flow)
#         print(r_outer_comp, r_inner_comp)
#
#         prev = _comp_emf
#         Diff += diff
#
#         if mode == 'once':
#             return _comp_emf
#
#         if way == 'plus':
#             for j in range(len(r_outer_comp[coils_to_change[0]])):
#                 r_inner_comp[coils_to_change[0]][j] += diff
#         else:
#             for j in range(len(r_outer_comp[coils_to_change[0]])):
#                 r_inner_comp[coils_to_change[0]][j] -= diff
#
#         if mode == 'once':
#             return _comp_emf


def change_all():  # r_outer_half, r_inner_half, r_outer_comp, r_inner_comp, comp_coef, coils_to_change):
    pass
    # prev = 0
    # while 1:
    #     s1 = change_s1(r_outer_half, r_inner_half, r_outer_comp, r_inner_comp, comp_coef, [1], way='plus', mode='once')
    #     if prev >= s1:
    #         for j in range(len(r_outer_comp[0])):
    #             r_outer_comp[0][j] += 0.0001
    #             r_inner_comp[0][j] -= 0.0001
    #         for j in range(len(r_outer_comp[1])):
    #             r_inner_comp[1][j] += 0.0001
    #         break
    #     prev = s1
    #     for j in range(len(r_outer_comp[0])):
    #         r_outer_comp[0][j] -= 0.0001
    #         r_inner_comp[0][j] += 0.0001
    #     for j in range(len(r_outer_comp[1])):
    #         r_inner_comp[1][j] -= 0.0001

    # while 1:
    #     s1 = change_s1(r_outer_half, r_inner_half, r_outer_comp, r_inner_comp, comp_coef, [1], way='plus', mode='once')
    #     if prev > s1:
    #         for j in range(len(r_outer_comp[0])):
    #             r_inner_comp[0][j] -= 0.0001
    #         break
    #     prev = s1
    #     for j in range(len(r_outer_comp[0])):
    #         r_inner_comp[0][j] += 0.0001
# TODO fix these version


def quad_coils(coil1_i, coil1_o, coil2_i, coil2_o, coil3_i, coil3_o, half_coil_i, half_coil_o):
    prev = 0
    while 1:
        print("\nSTEP")
        integral = [0, 0, 0, 0]
        for i in range(5):
            integral[0] -= (half_coil_i[i]*1000)**2
            integral[0] += (half_coil_o[i]*1000)**2
            integral[1] -= (coil1_i[i]*1000)**2
            integral[1] += (coil1_o[i]*1000)**2
            integral[2] -= (coil2_i[i]*1000)**2
            integral[2] += (coil2_o[i]*1000)**2
            integral[3] -= (coil3_i[i]*1000)**2
            integral[3] += (coil3_o[i]*1000)**2
        print("INTEGRAL: ", integral)
        f_ = (integral[1] - integral[2]) / 2 - integral[3]
        k = integral[0]/f_
        print("K: ", k, "F: ", f_)
        print("Coil: ", coil1_o, coil1_i)
        if prev > k:
            break
        prev = k
        for i in range(5):
            coil1_o[i] -= 0.001
            half_coil_o[i] -= 0.001


if __name__ == '__main__':
    coil1 = [[6.8, 7.2, 7.6, 8.0, 8.4], [13.4, 13.0, 12.6, 12.2, 11.8]]
    coil2 = [[0.2, 0.6, 1.0, 1.4, 1.8], [6.4, 6.0, 5.6, 5.2, 4.8]]
    coil3 = [[0.2, 0.6, 1.0, 1.4, 1.8], [6.4, 6.0, 5.6, 5.2, 4.8]]
    half_coil = [[7.2, 7.6, 8.0, 8.4, 8.8], [13.4, 13.0, 12.6, 12.2, 11.8]]
    quad_coils(coil1[0], coil1[1], coil2[0], coil2[1], coil3[0], coil3[1], half_coil[0], half_coil[1])
    # """ INPUT DATA """
    #
    # """field harmonics full version"""
    # field = {1: 5.67, 2: 23.78, 3: 3117.9, 4: 7.55, 5: 1.6, 6: 0.26, 7: 0.306, 8: 0.39, 9: 0.094, 10: 0.051,
    #          11: 0.034, 12: 0.033, 13: 0.077, 14: 0.16, 15: 2.71}
    # """field main harmonic"""
    # # field_ = {3: 3117.9}
    # field_ = {2: 3117.9}
    #
    # """NB magnet length, not coils"""
    # length = 0.3
    # r_ref = 0.01
    #
    # """radius of the half coil"""
    # r_in_half = [0.0072, 0.0076, 0.0080, 0.0084, 0.0088]
    # # r_in_half = [0.0068, 0.0072, 0.0076, 0.0080, 0.0084, 0.0088, 0.0092]
    # # # r_in_half = [0.0064, 0.0068, 0.0072, 0.0076, 0.0080, 0.0084, 0.0088]
    # # r_out_half = [0.0134, 0.013, 0.0126, 0.0122, 0.0118, 0.0114, 0.011]
    # r_out_half = [0.0134, 0.013, 0.0126, 0.0122, 0.0118]
    #
    # """radius of compensation coil"""
    # """
    #    the first array - radius of the bigger coil near the center (first coil)
    #    the second array - radius of the coil near the edge (second coil)
    #    the third array - radius of the small coil near the center (third coil)
    # """
    #
    # """first coil - 4 turns, second coil - 3 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001, 0.0014], [0.0089, 0.0093, 0.0097], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077, 0.0073], [0.0134, 0.013, 0.0126], [0.006, 0.0056]]
    # # k2, k3 = 3, 2
    #
    # """first coil - 4 turns, second coil - 4 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001, 0.0014], [0.0089, 0.0093, 0.0097, 0.0101], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077, 0.0073], [0.0134, 0.013, 0.0126, 0.0122], [0.006, 0.0056]]
    # # k2, k3 = 4, 2
    #
    # """first coil - 3 turns, second coil - 3 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001], [0.0089, 0.0093, 0.0097], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077], [0.0134, 0.013, 0.0126], [0.006, 0.0056]]
    # # k2, k3 = 3, 2
    #
    # """first coil - 3 turns, second coil - 4 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001], [0.0089, 0.0093, 0.0097, 0.0101], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077], [0.0134, 0.013, 0.0126, 0.0122], [0.006, 0.0056]]
    # # k2, k3 = 4, 2
    #
    # """first coil - 3 turns, second coil - 2 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001], [0.0089, 0.0093], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077], [0.0134, 0.013], [0.006, 0.0056]]
    # # k2, k3 = 2, 2
    #
    # """first coil - 3 turns, second coil - 1 turns"""
    # # r_in_comp = [[0.0002, 0.0006, 0.001], [0.0089], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077], [0.0134], [0.006, 0.0056]]
    # # k2, k3 = 1, 2
    # r_in_comp = [[0.0000199, 0.0006, 0.001003, 0.001408, 0.001802], [0.006810, 0.007205, 0.007608, 0.008009, 0.008409], [0.0000198, 0.000603, 0.001001, 0.001403, 0.001792]]
    # r_out_comp = [[0.006405, 0.006007, 0.005605, 0.005217, 0.004811], [0.013410, 0.013014, 0.012609, 0.012211, 0.011812], [0.006401, 0.006005, 0.005600, 0.005202, 0.004804]]
    # k2, k3 = 1, 1
    #
    # """first coil - 2 turns, second coil - 3 turns"""
    # # r_in_comp = [[0.0002, 0.0006], [0.0089, 0.0093, 0.0097], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081], [0.0134, 0.013, 0.0126], [0.006, 0.0056]]
    # # k2, k3 = 3, 2
    #
    # """first coil - 2 turns, second coil - 2 turns"""
    # # r_in_comp = [[0.0002, 0.0006], [0.0089, 0.0093], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081], [0.0134, 0.013], [0.006, 0.0056]]
    # # k2, k3 = 2, 2
    #
    # """coefficients for coils as 2nd and 3d have 3 and 2 turns"""
    # coef = [1, -k3/(k3+k2), -k2/(k3+k2)]  # TODO write a function to calculate these coefficients
    # print(coef)
    #
    # """make the first coil square more and the second coil square less"""
    # # change_s1_s3(field, length, r_ref, r_out_half, r_in_half, r_out_comp, r_in_comp, coef, [0, 1], way='plus')
    # # function changes the input array, be careful using two functions in a row
    #
    # """make the first coil square less and the second coil square bigger"""
    # # change_s1_s3(field_, length, r_ref, r_out_half, r_in_half, r_out_comp, r_in_comp, coef, [0, 1])
    #
    # print()
    # print("***NEW RADIUS***")
    # print(r_out_comp)
    # print(r_in_comp)
    # print("***________***")
    # print()
    #
    # """calculate emf and flow compensation with the new radius"""
    # half_coil = SextupleCoil(Coil(12, 7, r_in_half, r_out_half, 1))  # calculating coils
    # comp_coil = CompCoil(Coil(12, 3, r_in_comp[0], r_out_comp[0], coef[0]), Coil(12, 3, r_in_comp[1], r_out_comp[1], coef[1]), Coil(12, 2, r_in_comp[2], r_out_comp[2], coef[2]))
    #
    # flow = FLow(field, 0.3, 0.01, half_coil).calc_flow()  # calculating flow
    # flow1 = FLow(field, 0.3, 0.01, comp_coil).calc_flow()
    # print((max(flow) - min(flow))/(max(flow1)-min(flow1)))
    #
    # flow = FLow(field_, 0.3, 0.01, half_coil).calc_flow()
    # flow1 = FLow(field_, 0.3, 0.01, comp_coil).calc_flow()
    # print((max(flow) - min(flow))/(max(flow1)-min(flow1)))
    #
    # print()
    #
    # """calculate flow compensation for the main harmonic with another algorithm"""
    # integral = [0, 0, 0, 0]
    # # for i in range(7):
    # for i in range(5):
    #     integral[0] += (r_out_half[i]*1000)**2
    #     integral[0] -= (r_in_half[i]*1000)**2
    # for k in range(1, 4):
    #     for i in range(len(r_out_comp[k-1])):
    #         integral[k] += (r_out_comp[k-1][i]*1000)**2
    #         integral[k] -= (r_in_comp[k-1][i]*1000)**2
    # print(integral)
    # f_ = integral[1] + integral[3]*coef[2] + integral[2] * coef[1]
    # print(integral[0]/f_)
    #
    # # r_in_comp = [[0.0034, 0.0038, 0.0042], [0.0089, 0.0093, 0.0097], [0.0002, 0.0006]]
    # # r_out_comp = [[0.0085, 0.0081, 0.0077], [0.0134, 0.013, 0.0126], [0.006, 0.0056]]
    #
    # """field harmonics full version 10A"""
    # field = {1: 0, 2: 0, 3: 289, 4: 1.76, 5: 0.27, 6: 0.08, 7: 0.01, 8: 0.05, 9: 0.03, 10: 0.04,
    #          11: 0.02, 12: 0.03, 13: 0.03, 14: 0.01, 15: 0.12}
    # """field main harmonic 10A"""
    # field_ = {3: 289}
    #
    # """calculate emf and flow compensation with the new radius"""
    # half_coil = SextupleCoil(Coil(12, 7, r_in_half, r_out_half, 1))  # calculating coils
    # comp_coil = CompCoil(Coil(12, 3, r_in_comp[0], r_out_comp[0], coef[0]), Coil(12, 3, r_in_comp[1], r_out_comp[1], coef[1]), Coil(12, 2, r_in_comp[2], r_out_comp[2], coef[2]))
    #
    # flow = FLow(field, 0.3, 0.01, half_coil).calc_flow()  # calculating flow
    # flow1 = FLow(field, 0.3, 0.01, comp_coil).calc_flow()
    # emf1 = EMF(flow1).calc_emf()
    # print()
    # print(max(emf1))
    # print((max(flow) - min(flow))/(max(flow1)-min(flow1)))
    #
    # flow = FLow(field_, 0.3, 0.01, half_coil).calc_flow()
    # flow1 = FLow(field_, 0.3, 0.01, comp_coil).calc_flow()
    # print((max(flow) - min(flow))/(max(flow1)-min(flow1)))

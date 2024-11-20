# CGW - Calculation and Graphic Work
import tkinter as tk
from copy import deepcopy
from functools import partial
from pprint import pprint
from threading import Thread

import customtkinter as ctk
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import operations as op

global e, a
e = {}
a = {}


def create_res(resA, resB, resC):
    pprint(resA)
    pprint(resB)
    pprint(resC)
    window_res = ctk.CTk()
    frame = ctk.CTkFrame(window_res)
    frame.grid(row=0, column=0, padx=10, pady=10)
    lA = ctk.CTkLabel(frame, text="A", font=ctk.CTkFont(size=15))
    lA.grid(row=0, column=0)
    lAx = ctk.CTkLabel(frame, text=str(resA[0]), font=ctk.CTkFont(size=15))
    lAx.grid(row=0, column=1)
    lAy = ctk.CTkLabel(frame, text=str(resA[1]), font=ctk.CTkFont(size=15))
    lAy.grid(row=0, column=2)
    lAz = ctk.CTkLabel(frame, text=str(resA[2]), font=ctk.CTkFont(size=15))
    lAz.grid(row=0, column=3)
    lB = ctk.CTkLabel(frame, text="B", font=ctk.CTkFont(size=15))
    lB.grid(row=1, column=0)
    lBx = ctk.CTkLabel(frame, text=str(resB[0]), font=ctk.CTkFont(size=15))
    lBx.grid(row=1, column=1)
    lBy = ctk.CTkLabel(frame, text=str(resB[1]), font=ctk.CTkFont(size=15))
    lBy.grid(row=1, column=2)
    lBz = ctk.CTkLabel(frame, text=str(resB[2]), font=ctk.CTkFont(size=15))
    lBz.grid(row=1, column=3)
    lC = ctk.CTkLabel(frame, text="C", font=ctk.CTkFont(size=15))
    lC.grid(row=2, column=0)
    lCx = ctk.CTkLabel(frame, text=str(resC[0]), font=ctk.CTkFont(size=15))
    lCx.grid(row=2, column=1)
    lCy = ctk.CTkLabel(frame, text=str(resC[1]), font=ctk.CTkFont(size=15))
    lCy.grid(row=2, column=2)
    lCz = ctk.CTkLabel(frame, text=str(resC[2]), font=ctk.CTkFont(size=15))
    lCz.grid(row=2, column=3)
    triangles = [
        ((resA[0][0], resA[1][0], resA[2][0]),
         (resB[0][0], resB[1][0], resB[2][0]),
         (resC[0][0], resC[1][0], resC[2][0])),
    ]
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.add_collection(Poly3DCollection(triangles))

    ax.set_xlim([-10, 10])
    ax.set_ylim([-10, 10])
    ax.set_zlim([-10, 10])
    plt.show()
    window_res.mainloop()


def create_matrix(lst: list) -> list:
    matrix = []
    row = []
    count_row = 3
    count = 0
    for elem in lst:
        row.append(float(elem[1].get()))
        count += 1
        if count == count_row:
            matrix.append(row)
            row = []
            count = 0
    return matrix


def solve(vA, vB, vC):
    matrix_lst = []
    # e - entry, a - axes
    order = []
    op_dict = {"Гомотетия": op.stretching, "Проекция": op.projection, "Поворот": op.axis_rotation}
    for key, value in a.items():
        order.append(key)
    order = order[::-1]
    normal_order = order[:]
    for _ in range(len(order)):
        normal_order[_] = order[_][:-1]
    for key, value in a.items():
        a[key] = value.get()
    for key, value in e.items():
        e[key] = float(value.get())
    new_a = deepcopy(a)
    new_e = deepcopy(e)
    for key, value in a.items():
        new_a[key[:-1]] = new_a.pop(key)
    for key, value in e.items():
        new_e[key[:-1]] = new_e.pop(key)
    for oper in normal_order:
        if oper != "Проекция":
            matrix_lst.append(op_dict[oper](new_a[oper], new_e[oper]))
        else:
            matrix_lst.append(op_dict[oper](new_a[oper]))
    pprint(matrix_lst[0])
    pprint(matrix_lst[1])
    pprint(matrix_lst[2])
    T = op.multiply_matrices(op.multiply_matrices(matrix_lst[0], matrix_lst[1]), matrix_lst[2])
    pprint(T)
    resA = op.multiply_matrices(T, vA)
    resB = op.multiply_matrices(T, vB)
    resC = op.multiply_matrices(T, vC)
    create_res(resA, resB, resC)


def create_stretching_frame(main_frame, row, column, st):
    axes = ["ox", "oy", "oz"]
    stretching_frame = ctk.CTkFrame(main_frame)
    label1 = ctk.CTkLabel(stretching_frame, text="Гомотетия", font=ctk.CTkFont(size=15))
    label1.grid(row=0, column=0, padx=10, pady=10)
    label2 = ctk.CTkLabel(stretching_frame, text="Ось", font=ctk.CTkFont(size=15))
    label2.grid(row=1, column=0, padx=10, pady=10)
    axis1 = ctk.CTkOptionMenu(stretching_frame, dynamic_resizing=False, values=axes, font=ctk.CTkFont(size=15))
    a.update({"Гомотетия" + st: axis1})
    axis1.grid(row=2, column=0, padx=10, pady=10)
    label3 = ctk.CTkLabel(stretching_frame, text="Коэффициент", font=ctk.CTkFont(size=15))
    label3.grid(row=3, column=0, padx=10, pady=10)
    entry1 = ctk.CTkEntry(stretching_frame, textvariable=tk.IntVar(), font=ctk.CTkFont(size=15))
    e.update({"Гомотетия" + st: entry1})
    entry1.grid(row=4, column=0, padx=10, pady=10)
    stretching_frame.grid(row=row, column=column, padx=10, pady=10)


def create_rotation_frame(main_frame, row, column, st):
    axes = ["ox", "oy", "oz"]
    rotation_frame = ctk.CTkFrame(main_frame)
    label1 = ctk.CTkLabel(rotation_frame, text="Поворот", font=ctk.CTkFont(size=15))
    label1.grid(row=0, column=0, padx=10, pady=10)
    label2 = ctk.CTkLabel(rotation_frame, text="Ось", font=ctk.CTkFont(size=15))
    label2.grid(row=1, column=0, padx=10, pady=10)
    axis2 = ctk.CTkOptionMenu(rotation_frame, dynamic_resizing=False, values=axes, font=ctk.CTkFont(size=15))
    a.update({"Поворот" + st: axis2})
    axis2.grid(row=2, column=0, padx=10, pady=10)
    label3 = ctk.CTkLabel(rotation_frame, text="Угол", font=ctk.CTkFont(size=15))
    label3.grid(row=3, column=0, padx=10, pady=10)
    entry2 = ctk.CTkEntry(rotation_frame, textvariable=tk.IntVar(), font=ctk.CTkFont(size=15))
    e.update({"Поворот" + st: entry2})
    entry2.grid(row=4, column=0, padx=10, pady=10)
    rotation_frame.grid(row=row, column=column, padx=10, pady=10)


def create_projection_frame(main_frame, row, column, st):
    axes = ["ox", "oy", "oz"]
    rotation_frame = ctk.CTkFrame(main_frame)
    label1 = ctk.CTkLabel(rotation_frame, text="Проекция", font=ctk.CTkFont(size=15))
    label1.grid(row=0, column=0, padx=10, pady=10)
    label2 = ctk.CTkLabel(rotation_frame, text="Ось", font=ctk.CTkFont(size=15))
    label2.grid(row=1, column=0, padx=10, pady=10)
    axis3 = ctk.CTkOptionMenu(rotation_frame, dynamic_resizing=False, values=axes, font=ctk.CTkFont(size=15))
    a.update({"Проекция" + st: axis3})
    axis3.grid(row=2, column=0, padx=10, pady=10)
    rotation_frame.grid(row=row, column=column, padx=10, pady=10)


def create_params_window(vA, vB, vC):
    params_window = ctk.CTk()
    operations = {"гомотетия": create_stretching_frame, "поворот": create_rotation_frame,
                  "проекция": create_projection_frame}

    operations[optionmenu1.get()](params_window, 0, 0, "3")  # transform3
    operations[optionmenu2.get()](params_window, 0, 1, "2")  # transform2
    operations[optionmenu3.get()](params_window, 0, 2, "1")  # transform1
    hard_btn = ctk.CTkButton(params_window, text="Рассчёт", font=ctk.CTkFont(size=15),
                             command=partial(solve, vA, vB, vC))
    hard_btn.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    params_window.mainloop()


def get_operations():
    def first_show(vA, vB, vC):
        triangles = [
            ((vA[0][0], vA[1][0], vA[2][0]), (vB[0][0], vB[1][0], vB[2][0]), (vC[0][0], vC[1][0], vC[2][0])),
        ]
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.add_collection(Poly3DCollection(triangles))

        ax.set_xlim([-10, 10])
        ax.set_ylim([-10, 10])
        ax.set_zlim([-10, 10])
        plt.show()

    # matrix = create_matrix(field_list)
    vA = [[float(Ax.get())], [float(Ay.get())], [float(Az.get())]]
    vB = [[float(Bx.get())], [float(By.get())], [float(Bz.get())]]
    vC = [[float(Cx.get())], [float(Cy.get())], [float(Cz.get())]]
    t1 = Thread(target=first_show, args=(vA, vB, vC))
    t2 = Thread(target=create_params_window, args=(vA, vB, vC))
    t1.start()
    t2.start()


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()

label0 = ctk.CTkLabel(root, text=" Введите координаты точек", font=ctk.CTkFont(size=15))
label0.grid(row=0, column=0, columnspan=4)
label00 = ctk.CTkLabel(root, text="   ", font=ctk.CTkFont(size=15))
label00.grid(row=0, column=5)
label1 = ctk.CTkLabel(root, text=" Выберите порядок преобразований", font=ctk.CTkFont(size=15))
label1.grid(row=0, column=6)
label11 = ctk.CTkLabel(root, text="   ", font=ctk.CTkFont(size=15))
label11.grid(row=0, column=7)
values = ["гомотетия", "поворот", "проекция"]
axes = ["ox", "oy", "oz"]
optionmenu1 = ctk.CTkOptionMenu(root, dynamic_resizing=False, values=values, font=ctk.CTkFont(size=15))
optionmenu1.grid(row=1, column=6, padx=20, pady=5)
optionmenu2 = ctk.CTkOptionMenu(root, dynamic_resizing=False, values=values, font=ctk.CTkFont(size=15))
optionmenu2.grid(row=2, column=6, padx=20, pady=5)
optionmenu3 = ctk.CTkOptionMenu(root, dynamic_resizing=False, values=values, font=ctk.CTkFont(size=15))
optionmenu3.grid(row=3, column=6, padx=20, pady=5)
count_field = 0
labelA = ctk.CTkLabel(root, text="A", font=ctk.CTkFont(size=15))
labelA.grid(row=1, column=0, pady=5, padx=5)
labelB = ctk.CTkLabel(root, text="B", font=ctk.CTkFont(size=15))
labelB.grid(row=2, column=0, pady=5, padx=5)
labelC = ctk.CTkLabel(root, text="C", font=ctk.CTkFont(size=15))
labelC.grid(row=3, column=0, pady=5, padx=5)
Ax = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Ax.grid(row=1, column=1)
Bx = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Bx.grid(row=2, column=1)
Cx = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Cx.grid(row=3, column=1)
Ay = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Ay.grid(row=1, column=2)
By = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
By.grid(row=2, column=2)
Cy = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Cy.grid(row=3, column=2)
Az = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Az.grid(row=1, column=3)
Bz = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Bz.grid(row=2, column=3)
Cz = ctk.CTkEntry(root, width=40, height=5, font=ctk.CTkFont(size=15), placeholder_text="0")
Cz.grid(row=3, column=3)

btn = ctk.CTkButton(root, text="Рассчёт", font=ctk.CTkFont(size=15), command=get_operations)
btn.grid(row=4, column=0, columnspan=4, pady=5, padx=20)

root.mainloop()

from typing import List, Tuple

import numpy as np
from .periodic_box import Box


def db_list(box: Box) -> List[Tuple[int, int]]:
    nx = int(box.x)
    ny = int(box.y)
    nz = int(box.z)
    n = nx * ny * nz
    Lx = box.x / nx
    Ly = box.y / ny
    Lz = box.z / nz
    diagonal = Lx**2 + Ly**2 + Lz**2
    diagonal = diagonal * 1.1
    x = np.zeros(n, dtype=float)
    y = np.zeros(n, dtype=float)
    z = np.zeros(n, dtype=float)
    n = -1
    bonds: List[Tuple[int, int]] = []
    for i in range(nx):
        for j in range(ny):
            for k in range(nz):
                n = n + 1
                x[n] = Lx * i - 0.5 * Lx - 0.5 * box.x
                y[n] = Ly * j - 0.5 * Ly - 0.5 * box.y
                z[n] = Lz * k - 0.5 * Lz - 0.5 * box.z
    n_connect = 0
    for i in range(n - 1):
        for j in range(i + 1, n):
            dx = x[j] - x[i]
            dy = y[j] - y[i]
            dz = z[j] - z[i]
            dx, dy, dz = box.periodic_correct(dx, dy, dz)
            dr = np.sqrt(dx**2 + dy**2 + dz**2)
            if dr < diagonal:
                n_connect += 1
                bonds.append((i, j))
    return bonds


def attached_list(x: np.ndarray, y: np.ndarray, z: np.ndarray, box: Box):
    att_list = np.zeros(len(x))
    nx = int(box.x)
    ny = int(box.y)
    nz = int(box.z)
    n = nx * ny * nz
    main_list = np.zeros(n)
    for i in range(len(x)):
        kx = int((x[i] / box.x + 0.499998) * nx) + 1
        ky = int((y[i] / box.y + 0.499998) * ny) + 1
        kz = int((z[i] / box.z + 0.499998) * nz) + 1
        if kz < 1:
            kz = 1
        if kz > nz:
            kz = nz
        n = ((kx - 1) * ny + ky - 1) * nz + kz
        if main_list[n - 1] == 0:
            main_list[n - 1] = i
        else:
            na = main_list[n - 1]
            if att_list[na] == 0:
                att_list[na] = i
                break
            else:
                na = att_list[na]
    return main_list, att_list


def scan_list(
    x: np.ndarray,
    y: np.ndarray,
    z: np.ndarray,
    box: Box,
    bonds_list: List[Tuple[int, int]],
    main_list: np.ndarray,
    att_list: np.ndarray,
) -> List[Tuple[int, int]]:
    bonds: List[Tuple[int, int]] = []
    nx = int(box.x)
    ny = int(box.y)
    nz = int(box.z)
    n = nx * ny * nz
    for i in range(n):
        n1 = main_list[n - 1]
        while n1 != 0:
            n2 = att_list[n1]
            while n2 != 0:
                if n1 < n2:
                    bonds.append((n1, n2))
                else:
                    bonds.append((n2, n1))
            n2 = att_list[n2]
        n1 = att_list[n1]

    for i in range(len(bonds_list)):
        n1 = main_list[bonds_list[0][i]]
        while n1 != 0:
            n2 = main_list[bonds_list[1][i]]
            while n2 != 0:
                if n1 < n2:
                    bonds.append((n1, n2))
                else:
                    bonds.append((n2, n1))
            n2 = att_list[n2]
        n1 = att_list[n1]
    return bonds

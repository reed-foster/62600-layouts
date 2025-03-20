import phidl.geometry as pg
from phidl import Device


from phidl import quickplot as qp
from phidl import set_quickplot_options

set_quickplot_options(blocking=True)

designs = [
    ("student_designs/seshan_esparza_okoroafor.gds", "top"),
    ("student_designs/collins_camenisch_buonato.gds", "Unnamed_0"),
    ("standard_test_structures.gds", "top"),
]


def wafer_outline():
    radius = 75e3
    flat = 57.5e3
    circ = pg.circle(radius=radius)
    flat_dist = (radius**2 - (flat / 2) ** 2) ** 0.5
    flat = pg.rectangle(size=(flat, radius - flat_dist))
    flat.move((circ.x - flat.x, circ.ymin - flat.ymin))
    wafer = pg.kl_boolean(circ, flat, "A-B")
    outline = pg.outline(wafer, distance=1e-3, precision=1e-6, layer=255)
    outline.move(-outline.center)
    return outline


def grid(devlist, shape):
    return pg.grid(
        devlist,
        shape=shape,
        spacing=(0, 0),
        separation=True,
        align_x="x",
        align_y="y",
        edge_x="xmin",
        edge_y="ymin",
    )


def import_gds(gdsname, topcell):
    D = Device(gdsname)
    D << pg.import_gds(filename=gdsname, cellname=topcell, flatten=True)
    D.move(-D.center)
    r = pg.rectangle(size=(29499, 29499), layer=255)
    r.move(-r.center)
    D << pg.outline(r, distance=1, precision=1e-6, layer=255)
    return D


if __name__ == "__main__":
    A = Device("top")
    A << wafer_outline()
    devices = [import_gds(design[0], design[1]) for design in designs]
    all_devs = devices + devices[::-1]
    d = A << grid(all_devs, shape=(3, 2))
    d.move(-d.center)
    for i in range(2):
        devlist = devices[:2] if i == 0 else devices[1::-1]
        d1 = A << grid(devlist, shape=(2, 1))
        d1.move(-d1.center)
        d1.movex((devices[0].xsize / 6) * (-1) ** i)
        if i == 0:
            d1.movey(d.ymax - d1.ymin)
        else:
            d1.movey(d.ymin - d1.ymax)

    # add alignment marks
    X = pg.cross(length=100, width=2, layer=1)
    X2 = pg.cross(length=1000, width=100, layer=255)
    for i in range(2):
        for j in range(2):
            x = A << X
            x2 = A << X2
            x.move((40000 * (-1) ** i, 40000 * (-1) ** j))
            x2.move(x.center - x2.center)

    A.write_gds(
        "s25_consolidated.gds",
        unit=1e-6,
        precision=1e-9,
        auto_rename=True,
        max_cellname_length=28,
        cellname="top",
    )

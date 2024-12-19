import phidl.geometry as pg
from phidl import Device, LayerSet
from phidl import quickplot as qp
from phidl import set_quickplot_options

from qnngds.tests import alignment_mark, resolution_test

from typing import Tuple, List

set_quickplot_options(blocking=True)


def mim_cap(
    L_overlap: float = 100,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MIM capacitor between the two layers w1 and w2.

    Parameters:
        L_overlap (float): amount to extend pads to overlap
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created MIM capacitor
    """
    MIM = Device(f"MIM_CAP({L_overlap},{pad_size[1]})")
    bot_pad = pg.rectangle(
        (pad_size[0] + L_overlap, pad_size[1]), layer=layer_set["w1"].gds_layer
    )
    top_pad = pg.rectangle(
        (pad_size[0] + L_overlap, pad_size[1]), layer=layer_set["w2"].gds_layer
    )
    b = MIM << bot_pad
    t = MIM << top_pad
    b.move((-b.xmin, -b.ymin))
    t.move((pad_size[0] - t.xmin, -t.ymin))
    return MIM


def transistor(
    L_mesa: float = 8,
    L_gate: float = 2,
    L_overlap: float = 2,
    W_mesa: float = 12,
    W_contact: float = 10,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates the core of a transistor.

    Parameters:
        L_mesa (float): length of channel mesa
        L_gate (float): length of gate
        L_overlap (float): length of overlap between gate and source/drain
        W_mesa (float): width of channel mesa
        W_contact (float): width of source/drain contacts
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created transistor
    """

    GATE = Device("gate")
    SOURCE = Device("source")
    DRAIN = Device("drain")
    LAYOUT = Device("dummy")
    TRANSISTOR = Device(
        f"TRANSISTOR({L_mesa},{L_gate},{L_overlap},{W_mesa},{W_contact})"
    )

    # create transistor core
    mesa = pg.rectangle((L_mesa, W_mesa), layer=layer_set["mesa"].gds_layer)
    gate = pg.rectangle(
        (L_gate + 2 * L_overlap, W_mesa + 10), layer=layer_set["w1"].gds_layer
    )
    source = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["w2"].gds_layer
    )
    drain = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["w2"].gds_layer
    )
    mesa.move(-mesa.center)
    gate.move(-gate.center)
    source.move((gate.xmin - source.xmax + L_overlap, gate.y - source.y))
    drain.move((gate.xmax - drain.xmin - L_overlap, gate.y - drain.y))
    GATE << gate
    SOURCE << source
    DRAIN << drain
    LAYOUT << gate
    LAYOUT << source
    LAYOUT << drain
    LAYOUT << mesa

    # add pads
    gate_pad = pg.rectangle(pad_size, layer=layer_set["w1"].gds_layer)
    source_pad = pg.rectangle(pad_size, layer=layer_set["w2"].gds_layer)
    drain_pad = pg.rectangle(pad_size, layer=layer_set["w2"].gds_layer)
    gate_pad.move((gate.xmax - gate_pad.xmax, gate.ymax - gate_pad.ymin))
    source_pad.move((source.xmin - source_pad.xmax, source.ymax - source_pad.ymax))
    drain_pad.move((drain.xmax - drain_pad.xmin, drain.ymax - drain_pad.ymax))
    GATE << gate_pad
    SOURCE << source_pad
    DRAIN << drain_pad
    LAYOUT << gate_pad
    LAYOUT << source_pad
    LAYOUT << drain_pad

    # add text
    text = pg.text(
        f"W/Lg/Lov\n{W_contact}/{L_gate}/{L_overlap}", layer=layer_set["w1"].gds_layer
    )
    text.move((drain_pad.x - text.x, gate_pad.y - text.y))
    GATE << text
    LAYOUT << text

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    gate = pg.union(GATE, layer=layer_set["w1"].gds_layer)
    source = pg.union(SOURCE, layer=layer_set["w2"].gds_layer)
    drain = pg.union(DRAIN, layer=layer_set["w2"].gds_layer)
    mesa = pg.union(mesa, layer=layer_set["mesa"].gds_layer)

    # invert for positive tone
    if layer_set["w1"].gds_layer % 2 == 0:
        gate = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=gate, operation="not", layer=layer_set["w1"].gds_layer
        )
    else:
        gate = TRANSISTOR << gate
    if layer_set["w2"].gds_layer % 2 == 0:
        source = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=source, operation="not", layer=layer_set["w2"].gds_layer
        )
        drain = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=drain, operation="not", layer=layer_set["w2"].gds_layer
        )
    else:
        source = TRANSISTOR << source
        drain = TRANSISTOR << drain
    if layer_set["mesa"].gds_layer % 2 == 0:
        mesa = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=mesa, operation="not", layer=layer_set["mesa"].gds_layer
        )
    else:
        mesa = TRANSISTOR << mesa

    return TRANSISTOR


def test_chip(
    L_gate: List[float] = [2, 3, 5, 10, 15, 25],
    L_overlap: List[float] = [2, 3, 5, 10],
    W_contact: List[float] = [5, 10, 20, 50],
    L_mim: List[float] = [50, 100, 200],
) -> Device:
    # positive tone for even GDS layers, negative tone for odd GDS layers
    ls = LayerSet()
    ls.add_layer(
        name="w1",
        gds_layer=1,
        gds_datatype=0,
        description="tungsten gate",
        color=(0.6, 0.7, 0.9),
    )
    ls.add_layer(
        name="w2",
        gds_layer=3,
        gds_datatype=0,
        description="tungsten source/drain",
        color=(0.5, 0.4, 0.4),
    )
    ls.add_layer(
        name="mesa",
        gds_layer=5,
        gds_datatype=0,
        description="ito/igzo mesa",
        color=(0.6, 0.2, 0.5),
    )
    TOP = Device("top")
    TRANSISTOR_ARRAY = Device("transistors")
    MIM_CAP_ARRAY = Device("mimcaps")
    ALIGNMENT = Device("alignment")

    sample_w = 10000

    array_w = 4000
    array_margin = 100
    pad_size = (100, 100)
    pitch = 3 * pad_size[0]
    x_offset = array_margin
    y_offset = array_margin
    for L_ov in L_overlap:
        for W_c in W_contact:
            for L_g in L_gate:
                dut = transistor(
                    L_mesa=L_ov * 2 + L_g + 2,
                    L_gate=L_g,
                    L_overlap=L_ov,
                    W_mesa=2 + W_c,
                    W_contact=W_c,
                    layer_set=ls,
                    pad_size=pad_size,
                )
                if x_offset + pitch > array_w - array_margin:
                    x_offset = array_margin
                    y_offset += pitch
                dut_inst = TRANSISTOR_ARRAY << dut
                dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
                x_offset += pitch

    x_offset = array_margin
    y_offset = array_margin
    pitch = 4 * pad_size[0]
    for L_ov in L_mim:
        dut = mim_cap(L_overlap=L_ov, layer_set=ls, pad_size=pad_size)
        if x_offset + pitch > array_w - array_margin:
            x_offset = array_margin
            y_offset += pitch
        dut_inst = MIM_CAP_ARRAY << dut
        dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
        x_offset += pitch

    align = alignment_mark(layers=[l.gds_layer for k, l in ls._layers.items()])
    alignment_offset = 700
    resolutions = [1, 2, 3, 5]
    x_offset = alignment_offset
    y_offset = alignment_offset

    def rotate_i(dev, i):
        if i // 2 == 0:
            dev.rotate(i * 90)
        else:
            dev.rotate(-i * 90 + 90)

    for i in range(4):
        for li, layer in enumerate(ls._layers.keys()):
            pos = TOP << resolution_test(resolutions, True, layer=ls[layer].gds_layer)
            neg = TOP << resolution_test(resolutions, False, layer=ls[layer].gds_layer)
            rotate_i(neg, i)
            rotate_i(pos, i)
            neg.move((x_offset, y_offset))
            pos.move((x_offset, y_offset))
            if i == 0 or i == 3:
                neg.move((0, (-1) ** (i // 2) * (-300)))
                pos.move((0, (-1) ** (i // 2) * (-300)))
                neg.move(
                    (
                        (-1) ** (i // 2)
                        * (sample_w / 2 - 1000 * li - 500 - alignment_offset),
                        0,
                    )
                )
                pos.move(
                    (
                        (-1) ** (i // 2)
                        * (sample_w / 2 + 1000 * li + 500 - alignment_offset),
                        0,
                    )
                )
            else:
                neg.move(((-1) ** (i // 2) * 300, 0))
                pos.move(((-1) ** (i // 2) * 300, 0))
                neg.move(
                    (
                        0,
                        (-1) ** (i // 2)
                        * (sample_w / 2 - 1000 * li - 500 - alignment_offset),
                    )
                )
                pos.move(
                    (
                        0,
                        (-1) ** (i // 2)
                        * (sample_w / 2 + 1000 * li + 500 - alignment_offset),
                    )
                )
        a = TOP << align
        rotate_i(a, i)
        a.move((x_offset, y_offset))
        if i % 2 == 0:
            x_offset = sample_w - alignment_offset
        else:
            y_offset = sample_w - alignment_offset
            x_offset = alignment_offset
    # x_offset = 0
    # y_offset = 0
    # for i in range(4):
    #    #t_array = TOP << TRANSISTOR_ARRAY
    #    t_array = TOP << MIM_CAP_ARRAY
    #    t_array.move((x_offset - t_array.xmin, y_offset - t_array.ymin))
    #    if i % 2 == 0:
    #        x_offset += sample_w
    #    else:
    #        y_offset += sample_w
    #        x_offset = 0
    return TOP


if __name__ == "__main__":
    T = test_chip()
    qp(T)

import phidl.geometry as pg
from phidl import Device, LayerSet
from phidl import quickplot as qp
from phidl import set_quickplot_options

from qnngds.tests import alignment_mark, resolution_test

from typing import Tuple, List

set_quickplot_options(blocking=True)


def mos_cap(
    L_overlap: float = 100,
    L_contact: float = 10,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MOS capacitor between W1 and MESA, with contact on W2.

    Parameters:
        L_overlap (float): overlap between W1 and MESA
        L_contact (float): overlap (contact) between W2 and MESA
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created MOS capacitor
    """
    LAYOUT = Device(f"dummy")
    MOS = Device(f"MOS_CAP({L_overlap},{L_contact},{pad_size[1]})")
    bot_pad = pg.rectangle(
        (pad_size[0] + L_overlap, pad_size[1]), layer=layer_set["W1"].gds_layer
    )
    mesa = pg.rectangle(
        (L_overlap + L_contact, pad_size[1]), layer=layer_set["MESA"].gds_layer
    )
    top_pad = pg.rectangle(
        (pad_size[0] + L_contact, pad_size[1]), layer=layer_set["W2"].gds_layer
    )
    b = LAYOUT << bot_pad
    t = LAYOUT << top_pad
    m = LAYOUT << mesa
    b.move((-b.xmin, -b.ymin))
    m.move((pad_size[0] - m.xmin, -m.ymin))
    t.move((pad_size[0] + L_overlap - t.xmin, -t.ymin))
    text = LAYOUT << pg.text(
        f"W/L\n{pad_size[1]}/{L_overlap}", layer=layer_set["W1"].gds_layer
    )
    text.move((0.5 * (b.x + t.x) - text.x, t.ymax + 10 - text.ymin))

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    bot_u = pg.union(b, layer=layer_set["W1"].gds_layer)
    top_u = pg.union(t, layer=layer_set["W2"].gds_layer)
    mesa_u = pg.union(m, layer=layer_set["MESA"].gds_layer)
    text_u = pg.union(text, layer=layer_set["W1"].gds_layer)
    if layer_set["W1"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area, B=bot_u, operation="not", layer=layer_set["W1"].gds_layer
        )
        MOS << pg.kl_boolean(
            A=dev_area, B=text_u, operation="not", layer=layer_set["W1"].gds_layer
        )
    else:
        MOS << bot_u
        MOS << text_u
    if layer_set["W2"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area, B=top_u, operation="not", layer=layer_set["W2"].gds_layer
        )
    else:
        MOS << top_u
    if layer_set["MESA"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area, B=mesa_u, operation="not", layer=layer_set["MESA"].gds_layer
        )
    else:
        MOS << mesa_u
    return MOS


def mim_cap(
    L_overlap: float = 100,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MIM capacitor between the two layers W1 and W2.

    Parameters:
        L_overlap (float): amount to extend pads to overlap
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created MIM capacitor
    """
    LAYOUT = Device(f"dummy")
    MIM = Device(f"MIM_CAP({L_overlap},{pad_size[1]})")
    bot_pad = pg.rectangle(
        (pad_size[0] + L_overlap, pad_size[1]), layer=layer_set["W1"].gds_layer
    )
    top_pad = pg.rectangle(
        (pad_size[0] + L_overlap, pad_size[1]), layer=layer_set["W2"].gds_layer
    )
    b = LAYOUT << bot_pad
    t = LAYOUT << top_pad
    b.move((-b.xmin, -b.ymin))
    t.move((pad_size[0] - t.xmin, -t.ymin))
    text = LAYOUT << pg.text(
        f"W/L\n{pad_size[1]}/{L_overlap}", layer=layer_set["W1"].gds_layer
    )
    text.move((0.5 * (b.x + t.x) - text.x, t.ymax + 10 - text.ymin))

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    bot_u = pg.union(b, layer=layer_set["W1"].gds_layer)
    top_u = pg.union(t, layer=layer_set["W2"].gds_layer)
    text_u = pg.union(text, layer=layer_set["W1"].gds_layer)
    if layer_set["W1"].gds_layer % 2 == 0:
        MIM << pg.kl_boolean(
            A=dev_area, B=bot_u, operation="not", layer=layer_set["W1"].gds_layer
        )
        MIM << pg.kl_boolean(
            A=dev_area, B=text_u, operation="not", layer=layer_set["W1"].gds_layer
        )
    else:
        MIM << bot_u
        MIM << text_u
    if layer_set["W2"].gds_layer % 2 == 0:
        MIM << pg.kl_boolean(
            A=dev_area, B=top_u, operation="not", layer=layer_set["W2"].gds_layer
        )
    else:
        MIM << top_u
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
    """Creates a transistor with pads.

    Parameters:
        L_mesa (float): length of channel mesa
        L_gate (float): length of gate. if 0, does not construct a gate
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
    mesa = pg.rectangle((L_mesa, W_mesa), layer=layer_set["MESA"].gds_layer)
    if L_gate != 0:
        gate = pg.rectangle(
            (L_gate + 2 * L_overlap, W_mesa + 10), layer=layer_set["W1"].gds_layer
        )
    else:
        gate = pg.rectangle((L_mesa, W_mesa + 10), layer=layer_set["W1"].gds_layer)
    source = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["W2"].gds_layer
    )
    drain = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["W2"].gds_layer
    )
    mesa.move(-mesa.center)
    gate.move(-gate.center)
    source.move((gate.xmin - source.xmax + L_overlap, gate.y - source.y))
    drain.move((gate.xmax - drain.xmin - L_overlap, gate.y - drain.y))
    GATE << gate
    SOURCE << source
    DRAIN << drain
    if L_gate != 0:
        LAYOUT << gate
    LAYOUT << source
    LAYOUT << drain
    LAYOUT << mesa

    # add pads
    gate_pad = pg.rectangle(pad_size, layer=layer_set["W1"].gds_layer)
    source_pad = pg.rectangle(pad_size, layer=layer_set["W2"].gds_layer)
    drain_pad = pg.rectangle(pad_size, layer=layer_set["W2"].gds_layer)
    gate_pad.move((gate.xmax - gate_pad.xmax, gate.ymax - gate_pad.ymin))
    source_pad.move((source.xmin - source_pad.xmax, source.ymax - source_pad.ymax))
    drain_pad.move((drain.xmax - drain_pad.xmin, drain.ymax - drain_pad.ymax))
    GATE << gate_pad
    SOURCE << source_pad
    DRAIN << drain_pad
    if L_gate != 0:
        LAYOUT << gate_pad
    LAYOUT << source_pad
    LAYOUT << drain_pad

    # add text
    if L_gate != 0:
        text = pg.text(
            f"W/Lg/Lov\n{W_contact}/{L_gate}/{L_overlap}",
            layer=layer_set["W1"].gds_layer,
        )
        # align to upper right corner
        text.move((drain_pad.x - text.x, gate_pad.y - text.y))
        GATE << text
        LAYOUT << text
    else:
        text = pg.text(
            f"W/L\n{W_contact}/{L_mesa-2*L_overlap}", layer=layer_set["W1"].gds_layer
        )
        # align to drain / mesa
        text.move((mesa.x - text.x, drain_pad.ymax - text.ymin + 10))
        DRAIN << text
        LAYOUT << text

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    gate = pg.union(GATE, layer=layer_set["W1"].gds_layer)
    source = pg.union(SOURCE, layer=layer_set["W2"].gds_layer)
    drain = pg.union(DRAIN, layer=layer_set["W2"].gds_layer)
    mesa = pg.union(mesa, layer=layer_set["MESA"].gds_layer)

    # invert each layer for positive tone, only within the device area
    if L_gate != 0:
        # only do gate if L_gate is nonzero
        if layer_set["W1"].gds_layer % 2 == 0:
            gate = TRANSISTOR << pg.kl_boolean(
                A=dev_area, B=gate, operation="not", layer=layer_set["W1"].gds_layer
            )
        else:
            gate = TRANSISTOR << gate
    # source and drain on W2
    if layer_set["W2"].gds_layer % 2 == 0:
        source = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=source, operation="not", layer=layer_set["W2"].gds_layer
        )
        drain = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=drain, operation="not", layer=layer_set["W2"].gds_layer
        )
    else:
        source = TRANSISTOR << source
        drain = TRANSISTOR << drain
    # mesa
    if layer_set["MESA"].gds_layer % 2 == 0:
        mesa = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=mesa, operation="not", layer=layer_set["MESA"].gds_layer
        )
    else:
        mesa = TRANSISTOR << mesa

    return TRANSISTOR


def test_chip(
    neg_tone: int = 0,
    L_gate: List[float] = [2, 3, 5, 10, 15, 25],
    L_overlap: List[float] = [2, 3, 5, 10],
    W_contact: List[float] = [5, 10, 20, 50, 100],
    L_mim: List[float] = [25, 50, 75, 100, 125, 150, 175, 200],
    L_resistor: List[float] = [2, 3, 5, 10, 15, 25],
    W_resistor: List[float] = [10, 20, 50, 100],
) -> Device:
    # positive tone for even GDS layers, negative tone for odd GDS layers
    ls = LayerSet()
    ls.add_layer(
        name="W1",
        gds_layer=0 + neg_tone,
        gds_datatype=0,
        description="tungsten gate",
        color=(0.6, 0.7, 0.9),
    )
    ls.add_layer(
        name="W2",
        gds_layer=2 + neg_tone,
        gds_datatype=0,
        description="tungsten source/drain",
        color=(0.5, 0.4, 0.4),
    )
    ls.add_layer(
        name="MESA",
        gds_layer=4 + neg_tone,
        gds_datatype=0,
        description="ito/igzo mesa",
        color=(0.6, 0.2, 0.5),
    )
    TOP = Device("top")
    TRANSISTOR_ARRAY = Device("transistors")
    RESISTOR_ARRAY = Device("resistors")
    MIM_CAP_ARRAY = Device("mimcaps")
    ALIGNMENT = Device("alignment")
    LAYER_HEIGHTS = pg.preview_layerset(ls)

    sample_w = 10000

    array_w = 4000
    array_margin = 100
    pad_size = (100, 100)
    pitch = 3 * pad_size[0]

    # create transistors
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

    # create resistors
    x_offset = array_margin
    y_offset = array_margin
    for L in L_resistor:
        for W in W_resistor:
            dut = transistor(
                L_mesa=L + 20,
                L_gate=0,
                L_overlap=10,
                W_mesa=2 + W,
                W_contact=W,
                layer_set=ls,
                pad_size=pad_size,
            )
            if x_offset + pitch > array_w - array_margin:
                x_offset = array_margin
                y_offset += pitch
            dut_inst = RESISTOR_ARRAY << dut
            dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
            x_offset += pitch

    # create mimcaps
    x_offset = array_margin
    y_offset = array_margin
    pitch = 4.5 * pad_size[0]
    for L_ov in L_mim:
        dut = mim_cap(L_overlap=L_ov, layer_set=ls, pad_size=pad_size)
        if x_offset + pitch > array_w - array_margin:
            x_offset = array_margin
            y_offset += pitch
        dut_inst = MIM_CAP_ARRAY << dut
        dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
        x_offset += pitch

    # create alignment and lithography test structures
    align = alignment_mark(layers=[l.gds_layer for k, l in ls._layers.items()])
    alignment_offset = 700
    resolutions = [1, 2, 3, 5]
    x_offset = alignment_offset
    y_offset = alignment_offset
    rotate_i = lambda dev, i: dev.rotate(i * 90 if i // 2 == 0 else -i * 90 + 90)
    for i in range(4):
        for li, layer in enumerate(ls._layers.keys()):
            positive_litho = TOP << resolution_test(
                resolutions, True, layer=ls[layer].gds_layer
            )
            negative_litho = TOP << resolution_test(
                resolutions, False, layer=ls[layer].gds_layer
            )
            rotate_i(negative_litho, i)
            rotate_i(positive_litho, i)
            negative_litho.move((x_offset, y_offset))
            positive_litho.move((x_offset, y_offset))
            sign = (-1) ** (i // 2)
            if i == 0 or i == 3:
                negative_litho.move((0, sign * (-300)))
                positive_litho.move((0, sign * (-300)))
                negative_litho.move(
                    (sign * (sample_w / 2 - 1000 * (li + 0.5) - alignment_offset), 0)
                )
                positive_litho.move(
                    (sign * (sample_w / 2 + 1000 * (li + 0.5) - alignment_offset), 0)
                )
            else:
                negative_litho.move((sign * 300, 0))
                positive_litho.move((sign * 300, 0))
                negative_litho.move(
                    (0, sign * (sample_w / 2 - 1000 * (li + 0.5) - alignment_offset))
                )
                positive_litho.move(
                    (0, sign * (sample_w / 2 + 1000 * (li + 0.5) - alignment_offset))
                )
        alignment_marks = TOP << align
        rotate_i(alignment_marks, i)
        alignment_marks.move((x_offset, y_offset))
        if i % 2 == 0:
            x_offset = sample_w - alignment_offset
        else:
            y_offset = sample_w - alignment_offset
            x_offset = alignment_offset

    # add transistors and resistors
    dut_offset = 1200
    x_offset = dut_offset
    y_offset = dut_offset
    for i in range(4):
        t_array = TOP << TRANSISTOR_ARRAY
        r_array = TOP << RESISTOR_ARRAY
        t_array.move((x_offset - t_array.xmin, y_offset - t_array.ymin))
        r_array.move((x_offset - r_array.xmin, y_offset - r_array.ymin))
        if i // 2 == 0:
            r_array.movey(150 + t_array.ymax - r_array.ymin)
        else:
            r_array.movey(-150 + t_array.ymin - r_array.ymax)
        if i % 2 == 0:
            x_offset = sample_w - dut_offset - t_array.xsize
        else:
            x_offset = dut_offset
            y_offset = sample_w - dut_offset - t_array.ysize
    # add mimcaps
    x_offset = dut_offset
    y_offset = sample_w / 2
    for i in range(2):
        m_array = TOP << MIM_CAP_ARRAY
        m_array.move((x_offset - m_array.xmin, y_offset - m_array.y))
        x_offset = sample_w - dut_offset - m_array.xsize
    return TOP


if __name__ == "__main__":
    T = test_chip(neg_tone=0)
    T.write_gds(
        "bottom_gate_3mask.gds",
        unit=1e-6,
        precision=1e-9,
        auto_rename=True,
        max_cellname_length=28,
        cellname="top",
    )

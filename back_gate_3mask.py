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
    W: float = 100,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MOS capacitor between gate and mesa, with contact on
    sourcedrain.

    Parameters:
        L_overlap (float): overlap between gate and mesa
        L_contact (float): overlap (contact) between sourcedrain and mesa
        W (float): width of capacitor structure
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created MOS capacitor
    """
    LAYOUT = Device(f"dummy")
    MOS = Device(f"MOS_CAP({L_overlap},{L_contact},{pad_size[1]})")
    bot_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    bot_pad.move((-bot_pad.xmin, -bot_pad.ymin))
    bot = bot_pad << pg.rectangle((L_overlap, W), layer=layer_set["gate"].gds_layer)
    bot.move((pad_size[0] - bot.xmin, pad_size[1] / 2 - bot.y))
    mesa = pg.rectangle((L_overlap + L_contact, W), layer=layer_set["mesa"].gds_layer)
    top_pad = pg.rectangle(
        (pad_size[0] + L_contact, pad_size[1]), layer=layer_set["sourcedrain"].gds_layer
    )
    b = LAYOUT << bot_pad
    t = LAYOUT << top_pad
    m = LAYOUT << mesa
    b.move((-b.xmin, -b.ymin))
    m.move((pad_size[0] - m.xmin, b.y - m.y))
    t.move((pad_size[0] + L_overlap - t.xmin, b.y - t.y))
    text = LAYOUT << pg.text(
        f"W/L\n{pad_size[1]}/{L_overlap}", layer=layer_set["gate"].gds_layer
    )
    text.move((t.x - text.x, t.ymax + 10 - text.ymin))

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    bot_u = pg.union(
        pg.kl_boolean(A=b, B=text, operation="or", layer=layer_set["gate"].gds_layer),
        layer=layer_set["gate"].gds_layer,
    )
    top_u = pg.union(t, layer=layer_set["sourcedrain"].gds_layer)
    mesa_u = pg.union(m, layer=layer_set["mesa"].gds_layer)
    if layer_set["gate"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area, B=bot_u, operation="not", layer=layer_set["gate"].gds_layer
        )
    else:
        MOS << bot_u
    if layer_set["sourcedrain"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area,
            B=top_u,
            operation="not",
            layer=layer_set["sourcedrain"].gds_layer,
        )
    else:
        MOS << top_u
    if layer_set["mesa"].gds_layer % 2 == 0:
        MOS << pg.kl_boolean(
            A=dev_area, B=mesa_u, operation="not", layer=layer_set["mesa"].gds_layer
        )
    else:
        MOS << mesa_u
    return MOS


def mim_cap(
    L_overlap: float = 100,
    W: float = 100,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MIM capacitor between the two layers gate and sourcedrain.

    Parameters:
        L_overlap (float): amount to extend pads to overlap
        W (float): width of overlapped region
        layer_set (LayerSet): layers
        pad_size (tuple(float,float)): pad length and width

    Returns:
        Device: the created MIM capacitor
    """
    LAYOUT = Device(f"dummy")
    MIM = Device(f"MIM_CAP({L_overlap},{pad_size[1]})")
    bot_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    bot_pad.move((-bot_pad.xmin, -bot_pad.ymin))
    bot = bot_pad << pg.rectangle((L_overlap, W), layer=layer_set["gate"].gds_layer)
    bot.move((pad_size[0] - bot.xmin, pad_size[1] / 2 - bot.y))
    top_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    top_pad.move((-top_pad.xmin, -top_pad.ymin))
    top = top_pad << pg.rectangle(
        (L_overlap, W), layer=layer_set["sourcedrain"].gds_layer
    )
    top.move((-top.xmax, pad_size[1] / 2 - top.y))
    b = LAYOUT << bot_pad
    t = LAYOUT << top_pad
    b.move((-b.xmin, -b.ymin))
    t.move((pad_size[0] - t.xmin, b.y - t.y))
    text = LAYOUT << pg.text(
        f"W/L\n{pad_size[1]}/{L_overlap}", layer=layer_set["gate"].gds_layer
    )
    text.move(
        (t.xmax - pad_size[0] / 2 - text.x, t.y + pad_size[1] / 2 + 10 - text.ymin)
    )

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    bot_u = pg.union(
        pg.kl_boolean(A=b, B=text, operation="or", layer=layer_set["gate"].gds_layer),
        layer=layer_set["gate"].gds_layer,
    )
    top_u = pg.union(t, layer=layer_set["sourcedrain"].gds_layer)
    if layer_set["gate"].gds_layer % 2 == 0:
        MIM << pg.kl_boolean(
            A=dev_area, B=bot_u, operation="not", layer=layer_set["gate"].gds_layer
        )
    else:
        MIM << bot_u
    if layer_set["sourcedrain"].gds_layer % 2 == 0:
        MIM << pg.kl_boolean(
            A=dev_area,
            B=top_u,
            operation="not",
            layer=layer_set["sourcedrain"].gds_layer,
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
    mesa = pg.rectangle((L_mesa, W_mesa), layer=layer_set["mesa"].gds_layer)
    if L_gate != 0:
        gate = pg.rectangle(
            (L_gate + 2 * L_overlap, W_mesa + 10), layer=layer_set["gate"].gds_layer
        )
    else:
        gate = pg.rectangle((L_mesa, W_mesa + 10), layer=layer_set["gate"].gds_layer)
    source = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["sourcedrain"].gds_layer
    )
    drain = pg.rectangle(
        ((L_mesa - L_gate) / 2 + 5, W_contact), layer=layer_set["sourcedrain"].gds_layer
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
    gate_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    source_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    drain_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
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
            layer=layer_set["gate"].gds_layer,
        )
        # align to upper right corner
        text.move((drain_pad.x - text.x, gate_pad.y - text.y))
        GATE << text
        LAYOUT << text
    else:
        text = pg.text(
            f"W/L\n{W_contact}/{L_mesa-2*L_overlap}", layer=layer_set["gate"].gds_layer
        )
        # align to drain / mesa
        text.move((mesa.x - text.x, drain_pad.ymax - text.ymin + 10))
        DRAIN << text
        LAYOUT << text

    dev_area = pg.rectangle((LAYOUT.xsize + 10, LAYOUT.ysize + 10))
    dev_area.move((LAYOUT.x - dev_area.x, LAYOUT.y - dev_area.y))
    gate = pg.union(GATE, layer=layer_set["gate"].gds_layer)
    source = pg.union(SOURCE, layer=layer_set["sourcedrain"].gds_layer)
    drain = pg.union(DRAIN, layer=layer_set["sourcedrain"].gds_layer)
    mesa = pg.union(mesa, layer=layer_set["mesa"].gds_layer)

    # invert each layer for positive tone, only within the device area
    if L_gate != 0:
        # only do gate if L_gate is nonzero
        if layer_set["gate"].gds_layer % 2 == 0:
            gate = TRANSISTOR << pg.kl_boolean(
                A=dev_area, B=gate, operation="not", layer=layer_set["gate"].gds_layer
            )
        else:
            gate = TRANSISTOR << gate
    # source and drain on sourcedrain
    if layer_set["sourcedrain"].gds_layer % 2 == 0:
        source = TRANSISTOR << pg.kl_boolean(
            A=dev_area,
            B=source,
            operation="not",
            layer=layer_set["sourcedrain"].gds_layer,
        )
        drain = TRANSISTOR << pg.kl_boolean(
            A=dev_area,
            B=drain,
            operation="not",
            layer=layer_set["sourcedrain"].gds_layer,
        )
    else:
        source = TRANSISTOR << source
        drain = TRANSISTOR << drain
    # mesa
    if layer_set["mesa"].gds_layer % 2 == 0:
        mesa = TRANSISTOR << pg.kl_boolean(
            A=dev_area, B=mesa, operation="not", layer=layer_set["mesa"].gds_layer
        )
    else:
        mesa = TRANSISTOR << mesa

    return TRANSISTOR


def positivetoneify(
    D: Device = None, cutout: Device = None, layer_set: LayerSet = LayerSet()
) -> Device:
    """Inverts device D over area specified by cutout.

    Parameters:
        D (Device): negative tone version of device
        cutout (Device): area to apply inversion (can just be the bounding box of D + extent, or can be irregular shape)
        layer_set (LayerSet): GDS layers

    Returns:
        Device: positive tone version
    """
    POS = Device(D.name)
    for k, l in layer_set._layers.items():
        # only do gate if L_gate is nonzero
        if l.gds_layer % 2 == 0:
            layer = Device()
            for p in D.get_polygons(by_spec=(l.gds_layer, l.gds_datatype)):
                layer.add_polygon(p, layer=l.gds_layer)
            POS << pg.kl_boolean(A=cutout, B=layer, operation="not", layer=l.gds_layer)
        else:
            POS << D
    return POS


def test_chip(neg_tone: int = 0) -> Device:
    #### parameters to sweep ###

    # transistors
    L_gate = [2, 3, 5, 7, 10, 15, 25]
    L_overlap = [2, 3, 5, 10]
    W_contact = [5, 10, 30, 100]

    # MIM/MOS capacitors
    L_cap = [20, 40, 80, 100, 200]
    W_cap = [50, 70, 80, 100]

    # ITO resistors
    L_resistor = [2, 3, 5, 10, 15, 25]
    W_resistor = [10, 20, 50, 100]

    # W resistors

    # positive tone for even GDS layers, negative tone for odd GDS layers
    ls = LayerSet()
    ls.add_layer(
        name="gate",
        gds_layer=0 + neg_tone,
        gds_datatype=0,
        description="tungsten gate",
        color=(0.6, 0.7, 0.9),
    )
    ls.add_layer(
        name="sourcedrain",
        gds_layer=2 + neg_tone,
        gds_datatype=0,
        description="tungsten source/drain",
        color=(0.5, 0.4, 0.4),
    )
    ls.add_layer(
        name="mesa",
        gds_layer=4 + neg_tone,
        gds_datatype=0,
        description="ito/igzo mesa",
        color=(0.6, 0.2, 0.5),
    )
    TOP = Device("top")
    RESISTOR_ARRAY = Device("resistors")

    sample_w = 5000
    pad_size = (100, 100)

    # create alignment marks
    align = alignment_mark(layers=[l.gds_layer for k, l in ls._layers.items()])
    ALIGN = Device("ALIGN")
    ## positive/negative tone
    align_footprint = pg.rectangle((align.ysize / 2 + 10, align.ysize / 2 + 10))
    align_area = Device()
    for i in range(2):
        for j in range(2):
            if (i == j) and (i == 0):
                continue
            aa = align_area << align_footprint
            aa.move(-aa.center)
            aa.move((aa.xsize / 2 * (-1) ** i, aa.ysize / 2 * (-1) ** j))
    ALIGN << positivetoneify(align, align_area, ls)
    # for k, l in ls._layers.items():
    #    # only do gate if L_gate is nonzero
    #    if l.gds_layer % 2 == 0:
    #        align_layer = Device()
    #        for p in align.get_polygons(by_spec=(l.gds_layer, 0)):
    #            align_layer.add_polygon(p, layer=l.gds_layer)
    #        al = ALIGN << pg.kl_boolean(
    #            A=align_area, B=align_layer, operation="not", layer=l.gds_layer
    #        )
    #    else:
    #        al = ALIGN << align
    # source and drain on sourcedrain
    # if layer_set["sourcedrain"].gds_layer % 2 == 0:
    #    source = TRANSISTOR << pg.kl_boolean(
    #        A=dev_area, B=source, operation="not", layer=layer_set["sourcedrain"].gds_layer
    #    )
    #    drain = TRANSISTOR << pg.kl_boolean(
    #        A=dev_area, B=drain, operation="not", layer=layer_set["sourcedrain"].gds_layer
    #    )
    # else:
    #    source = TRANSISTOR << source
    #    drain = TRANSISTOR << drain
    ## mesa
    # if layer_set["mesa"].gds_layer % 2 == 0:
    #    mesa = TRANSISTOR << pg.kl_boolean(
    #        A=dev_area, B=mesa, operation="not", layer=layer_set["mesa"].gds_layer
    #    )
    # else:
    #    mesa = TRANSISTOR << mesa
    # pg.kl_boolean
    alignment_offset = 700
    resolutions = [1, 2, 3, 5]
    rotate_i = lambda dev, i: dev.rotate(i * 90 if i // 2 == 0 else -i * 90 + 90)
    x_offset = alignment_offset
    y_offset = alignment_offset
    for i in range(4):
        alignment_marks = TOP << ALIGN
        rotate_i(alignment_marks, i)
        alignment_marks.move((x_offset, y_offset))
        if i % 2 == 0:
            x_offset = sample_w - alignment_offset
        else:
            y_offset = sample_w - alignment_offset
            x_offset = alignment_offset

    # create lithography structures
    LITHO = Device("LITHO")
    for layer_name, layer in ls._layers.items():
        for i in range(2):
            rt = resolution_test([1, 2, 3], inverted=i, layer=layer.gds_layer)
            rt.flatten()
            rt.move(-rt.center)
            if layer_name == "gate":
                cutout = rt << pg.rectangle(rt.size, layer=ls["sourcedrain"].gds_layer)
                cutout.move(-cutout.center)
            rt_i = LITHO << rt
            if layer_name == "gate":
                rt_i.move(
                    (-rt_i.xmin + i * (rt.xsize + 50), align.xsize - rt_i.ymin + 50)
                )
            if layer_name == "sourcedrain":
                if i == 0:
                    rt_i.move(
                        (-rt_i.xmin + 2 * (rt.xsize + 50), align.xsize - rt_i.ymin + 50)
                    )
                else:
                    rt_i.move(
                        (
                            -rt_i.xmin + (align.xsize - align.ysize / 2),
                            (align.xsize - align.ysize / 2) - rt_i.ymin + 50,
                        )
                    )
            if layer_name == "mesa":
                rt_i.rotate(90)
                rt_i.move(
                    (
                        align.xsize - rt_i.xmin + 50,
                        align.xsize - rt_i.ymin + 50 - (i + 1) * (rt_i.ysize + 50),
                    )
                )
    litho = TOP << LITHO

    # create MOS CAP and MIM CAP test structures
    MOS = pg.gridsweep(
        function=lambda L, W: mos_cap(L, 10, W, ls, pad_size),
        param_x={"L": L_cap},
        param_y={"W": W_cap},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    MIM = pg.gridsweep(
        function=lambda L, W: mim_cap(L, W, ls, pad_size),
        param_x={"L": L_cap},
        param_y={"W": W_cap},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    mos = TOP << MOS
    mim = TOP << MIM
    mos.move((litho.xmax - mos.xmin + 50, litho.ymin - mos.ymin))
    mim.move((litho.xmax - mim.xmin + 50, mos.ymax - mim.ymin + 50))

    # create transistors
    TRANSISTOR = pg.gridsweep(
        function=lambda L_ov, W_c, L_g: transistor(
            L_mesa=L_ov * 2 + L_g + 2,
            L_gate=L_g,
            L_overlap=L_ov,
            W_mesa=2 + W_c,
            W_contact=W_c,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_y={"L_g": L_gate},
        param_x={"L_ov": L_overlap, "W_c": W_contact},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    trans = TOP << TRANSISTOR
    trans.move((sample_w / 2 - trans.x, litho.ymax + 50 - trans.ymin))
    # x_offset = array_margin
    # y_offset = array_margin
    # for L_ov in L_overlap:
    #    for W_c in W_contact:
    #        for L_g in L_gate:
    #            dut = transistor(
    #                L_mesa=L_ov * 2 + L_g + 2,
    #                L_gate=L_g,
    #                L_overlap=L_ov,
    #                W_mesa=2 + W_c,
    #                W_contact=W_c,
    #                layer_set=ls,
    #                pad_size=pad_size,
    #            )
    #            if x_offset + pitch > array_w - array_margin:
    #                x_offset = array_margin
    #                y_offset += pitch
    #            dut_inst = TRANSISTOR_ARRAY << dut
    #            dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
    #            x_offset += pitch

    ## create resistors
    # x_offset = array_margin
    # y_offset = array_margin
    # for L in L_resistor:
    #    for W in W_resistor:
    #        dut = transistor(
    #            L_mesa=L + 20,
    #            L_gate=0,
    #            L_overlap=10,
    #            W_mesa=2 + W,
    #            W_contact=W,
    #            layer_set=ls,
    #            pad_size=pad_size,
    #        )
    #        if x_offset + pitch > array_w - array_margin:
    #            x_offset = array_margin
    #            y_offset += pitch
    #        dut_inst = RESISTOR_ARRAY << dut
    #        dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
    #        x_offset += pitch

    ## create mimcaps
    # x_offset = array_margin
    # y_offset = array_margin
    # pitch = 4.5 * pad_size[0]
    # for L_ov in L_mim:
    #    dut = mim_cap(L_overlap=L_ov, layer_set=ls, pad_size=pad_size)
    #    if x_offset + pitch > array_w - array_margin:
    #        x_offset = array_margin
    #        y_offset += pitch
    #    dut_inst = MIM_CAP_ARRAY << dut
    #    dut_inst.move((x_offset - dut_inst.xmin, y_offset - dut_inst.ymin))
    #    x_offset += pitch

    ## add transistors and resistors
    # dut_offset = 1200
    # x_offset = dut_offset
    # y_offset = dut_offset
    # for i in range(4):
    #    t_array = TOP << TRANSISTOR_ARRAY
    #    r_array = TOP << RESISTOR_ARRAY
    #    t_array.move((x_offset - t_array.xmin, y_offset - t_array.ymin))
    #    r_array.move((x_offset - r_array.xmin, y_offset - r_array.ymin))
    #    if i // 2 == 0:
    #        r_array.movey(150 + t_array.ymax - r_array.ymin)
    #    else:
    #        r_array.movey(-150 + t_array.ymin - r_array.ymax)
    #    if i % 2 == 0:
    #        x_offset = sample_w - dut_offset - t_array.xsize
    #    else:
    #        x_offset = dut_offset
    #        y_offset = sample_w - dut_offset - t_array.ysize
    ## add mimcaps
    # x_offset = dut_offset
    # y_offset = sample_w / 2
    # for i in range(2):
    #    m_array = TOP << MIM_CAP_ARRAY
    #    m_array.move((x_offset - m_array.xmin, y_offset - m_array.y))
    #    x_offset = sample_w - dut_offset - m_array.xsize
    return TOP


if __name__ == "__main__":
    T = test_chip(neg_tone=0)
    T.write_gds(
        "ito_test.gds",
        unit=1e-6,
        precision=1e-9,
        auto_rename=True,
        max_cellname_length=28,
        cellname="top",
    )

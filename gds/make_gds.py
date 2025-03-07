import phidl.geometry as pg
from phidl import Device, LayerSet
from phidl import quickplot as qp
from phidl import set_quickplot_options

from via import test_via

from qnngds.tests import alignment_mark, resolution_test, vdp
from qnngds.devices.resistor import meander

import phidlfem.analysis as pfa

import numpy as np

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
    MOS = Device(f"MOS_CAP({L_overlap},{L_contact},{pad_size[1]})")
    bot_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    bot_pad.move((-bot_pad.xmin, -bot_pad.ymin))
    bot = bot_pad << pg.rectangle(
        (L_overlap + 15, W + 10), layer=layer_set["gate"].gds_layer
    )
    bot.move((pad_size[0] - bot.xmin - 5, pad_size[1] / 2 - bot.y))
    bot_via = bot_pad << pg.rectangle(
        (pad_size[0], pad_size[1]), layer=layer_set["via"].gds_layer
    )
    bot_via.move((pad_size[0] / 2 - bot_via.x, pad_size[1] / 2 - bot_via.y))
    bot_via_cover = bot_pad << pg.rectangle(
        (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    bot_via_cover.move(
        (pad_size[0] / 2 - bot_via_cover.x, pad_size[1] / 2 - bot_via_cover.y)
    )
    bot_via_conn = bot_pad << pg.rectangle(
        (2, W + 10 + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    bot_via_conn.move(
        (
            bot_pad.xmax - L_overlap - 10 - bot_via_conn.xmin,
            pad_size[1] / 2 - bot_via_conn.y,
        )
    )
    mesa = pg.rectangle((L_overlap + L_contact, W), layer=layer_set["mesa"].gds_layer)
    top_pad = pg.rectangle(
        (pad_size[0] + L_contact, pad_size[1]), layer=layer_set["sourcedrain"].gds_layer
    )
    top = top_pad << pg.rectangle(
        (10, W + 10), layer=layer_set["sourcedrain"].gds_layer
    )
    top.move((-top.xmin, pad_size[1] / 2 - top.y))
    b = MOS << bot_pad
    t = MOS << top_pad
    m = MOS << mesa
    b.move((-b.xmin, -b.ymin))
    m.move((b.xmax - m.xmin - L_overlap, b.y - m.y))
    t.move((m.xmax - t.xmin - 5, b.y - t.y))
    text = MOS << pg.text(f"W/L\n{W}/{L_overlap}", layer=layer_set["gate"].gds_layer)
    text.move((t.x - text.x, t.ymax + 10 - text.ymin))
    MOS << pg.union(text, layer=layer_set["sourcedrain"].gds_layer)

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
    MIM = Device(f"MIM_CAP({L_overlap},{pad_size[1]})")
    bot_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    bot_pad.move((-bot_pad.xmin, -bot_pad.ymin))
    bot = bot_pad << pg.rectangle(
        (L_overlap + 10, W + 10), layer=layer_set["gate"].gds_layer
    )
    bot.move((pad_size[0] - bot.xmin, pad_size[1] / 2 - bot.y))
    bot_via = bot_pad << pg.rectangle(
        (pad_size[0], pad_size[1]), layer=layer_set["via"].gds_layer
    )
    bot_via.move((pad_size[0] / 2 - bot_via.x, pad_size[1] / 2 - bot_via.y))
    bot_via_cover = bot_pad << pg.rectangle(
        (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    bot_via_cover.move(
        (pad_size[0] / 2 - bot_via_cover.x, pad_size[1] / 2 - bot_via_cover.y)
    )
    bot_via_conn = bot_pad << pg.rectangle(
        (2, W + 10 + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    bot_via_conn.move(
        (
            bot_pad.xmax - L_overlap - 10 - bot_via_conn.xmin,
            pad_size[1] / 2 - bot_via_conn.y,
        )
    )
    top_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    top_pad.move((-top_pad.xmin, -top_pad.ymin))
    top = top_pad << pg.rectangle(
        (L_overlap + 10, W), layer=layer_set["sourcedrain"].gds_layer
    )
    top.move((-top.xmax, pad_size[1] / 2 - top.y))
    b = MIM << bot_pad
    t = MIM << top_pad
    b.move((-b.xmin, -b.ymin))
    t.move((b.xmax - t.xmin - L_overlap, b.y - t.y))
    text = MIM << pg.text(f"W/L\n{W}/{L_overlap}", layer=layer_set["gate"].gds_layer)
    text.move(
        (t.xmax - pad_size[0] / 2 - text.x, t.y + pad_size[1] / 2 + 10 - text.ymin)
    )
    MIM << pg.union(text, layer=layer_set["sourcedrain"].gds_layer)

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

    TRANSISTOR = Device(
        f"TRANSISTOR({L_mesa},{L_gate},{L_overlap},{W_mesa},{W_contact})"
    )

    # create transistor core
    mesa = pg.rectangle((L_mesa, W_mesa), layer=layer_set["mesa"].gds_layer)
    if L_gate != 0:
        gate = pg.rectangle(
            (L_gate + 2 * L_overlap, W_mesa + 20), layer=layer_set["gate"].gds_layer
        )
    else:
        # dummy device that is used as a reference point/location
        gate = pg.rectangle((L_mesa, W_mesa + 20), layer=layer_set["gate"].gds_layer)
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
    if L_gate != 0:
        TRANSISTOR << gate
    TRANSISTOR << source
    TRANSISTOR << drain
    TRANSISTOR << mesa

    # add pads
    gate_pad = pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
    gate_via = pg.rectangle(
        (pad_size[0], pad_size[1]), layer=layer_set["via"].gds_layer
    )
    gate_via_cover = pg.rectangle(
        (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    gate_via_conn = pg.rectangle(
        (L_gate + 2 * L_overlap + 2, 2), layer=layer_set["sourcedrain"].gds_layer
    )
    source_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    drain_pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    gate_pad.move((gate.xmax - gate_pad.xmax, gate.ymax - gate_pad.ymin))
    gate_via.move(gate_pad.center - gate_via.center)
    source_pad.move((source.xmin - source_pad.xmax, source.ymax - source_pad.ymax))
    drain_pad.move((drain.xmax - drain_pad.xmin, drain.ymax - drain_pad.ymax))
    gate_via_cover.move(gate_pad.center - gate_via_cover.center)
    gate_via_conn.move((gate.x - gate_via_conn.x, gate.ymax - gate_via_conn.ymax))
    if L_gate != 0:
        TRANSISTOR << gate_pad
        TRANSISTOR << gate_via
        TRANSISTOR << gate_via_cover
        TRANSISTOR << gate_via_conn
    TRANSISTOR << source_pad
    TRANSISTOR << drain_pad

    # add text
    if L_gate != 0:
        text = pg.text(
            f"W/Lg/Lov\n{W_mesa}/{L_gate}/{L_overlap}",
            layer=layer_set["gate"].gds_layer,
        )
        # align to upper right corner
        text.move((drain_pad.x - text.x, gate_pad.y - text.y))
        TRANSISTOR << text
    else:
        text = pg.text(
            f"W/L\n{W_mesa}/{L_mesa-2*L_overlap}", layer=layer_set["gate"].gds_layer
        )
        # align to drain / mesa
        text.move((mesa.x - text.x, drain_pad.ymax - text.ymin + 10))
        TRANSISTOR << text
    TRANSISTOR << pg.union(text, layer=layer_set["sourcedrain"].gds_layer)

    return TRANSISTOR


def gated_vdp(
    gated: bool = True,
    rotation: float = 0,
    pad_size: Tuple[float, float] = (100, 100),
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates Van-der-Pauw test structure, with optional back gate.

    Parameters:
        gated (bool): if true, include back gate
        rotation (float): rotation of test structure in degrees
        pad_size (tuple(float,float)): pad length and width
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: VDP structure
    """
    VDP = Device(f"VDP({gated})")
    ito = VDP << vdp(l=2 * max(pad_size), w=10, layer=layer_set["mesa"].gds_layer)
    pad = pg.rectangle(pad_size, layer=layer_set["sourcedrain"].gds_layer)
    pad.move((-pad.xmin, -pad.y))
    contact = pad << pg.rectangle((20, 10), layer=layer_set["sourcedrain"].gds_layer)
    contact.move((-contact.xmax, -contact.y))
    pad.add_port(
        name=1, midpoint=(contact.xmin + 5, contact.y), orientation=180, width=10
    )
    pads = {}
    for p in ito.ports:
        pad_i = VDP << pad
        pad_i.connect(pad_i.ports[1], ito.ports[p])
        pads[p] = pad_i
    if gated:
        gate = VDP << vdp(
            l=2 * max(pad_size) + 10, w=15, layer=layer_set["gate"].gds_layer
        )
        gate.move(ito.center - gate.center)
        gate_pad = VDP << pg.rectangle(pad_size, layer=layer_set["gate"].gds_layer)
        gate_pad.move(
            (pads["E1"].xmax - gate_pad.xmax, pads["S1"].ymin - gate_pad.ymin)
        )
        via = VDP << pg.rectangle(
            (pad_size[0], pad_size[1]), layer=layer_set["via"].gds_layer
        )
        via.move(gate_pad.center - via.center)
        via_cover = VDP << pg.rectangle(
            (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
        )
        via_cover.move(via.center - via_cover.center)
        gate_contact = VDP << pg.rectangle(
            ((VDP.xsize - max(pad_size)) / 2**0.5, 10),
            layer=layer_set["gate"].gds_layer,
        )
        gate_contact.rotate(-45)
        gate_contact.move(
            (gate_pad.x - gate_contact.xmax, gate_pad.y - gate_contact.ymin)
        )
    VDP.rotate(rotation)
    return VDP


def metal_resistor(
    width: float = 5,
    squares: float = 50,
    layer_name: str = "gate",
    pad_size: Tuple[float, float] = (100, 100),
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates meandered metal resistor.

    Parameters:
        width (float): wire width in microns
        squares (float): number of squares
        layer_name (string): name of layer to define resistor on
        pad_size (tuple(float,float)): pad length and width
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: meandered metal resistor
    """
    pitch = 2 * width
    max_length = np.ceil(squares / (pad_size[1] / width)) * pitch
    RESISTOR = Device(f"RESISTOR({width, squares})")
    m = meander(
        width=width,
        pitch=pitch,
        squares=squares,
        max_length=max_length,
        layer=layer_set[layer_name].gds_layer,
    )
    RESISTOR << m
    contact = pg.rectangle(pad_size, layer=layer_set[layer_name].gds_layer)
    contact.add_port(
        name=1, midpoint=(contact.xmin, contact.y), width=pad_size[1], orientation=180
    )
    # add vias
    VIAS = Device("vias")
    via = pg.rectangle((pad_size[0], pad_size[1]), layer=layer_set["via"].gds_layer)
    via_cover = pg.rectangle(
        (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
    )
    via_conn = pg.rectangle((width + 2, 2), layer=layer_set["sourcedrain"].gds_layer)
    for i in range(2):
        contact_i = RESISTOR << contact
        contact_i.connect(contact_i.ports[1], m.ports[i + 1])
        if layer_name == "gate":
            via_i = VIAS << via
            via_i.move(contact_i.center - via_i.center)
            via_cover_i = VIAS << via_cover
            via_cover_i.move(contact_i.center - via_cover_i.center)
            via_conn_i = VIAS << via_conn
            via_conn_i.move(
                (
                    via_i.x - via_conn_i.x,
                    contact_i.y
                    + (-1) ** i * (-via_conn_i.ysize / 2 - pad_size[1] / 2)
                    - via_conn_i.y,
                )
            )
    dummy = pg.union(RESISTOR, by_layer=True)
    dummy.add_port(
        name=1, midpoint=(RESISTOR.x, RESISTOR.ymin), width=pad_size[1], orientation=270
    )
    dummy.add_port(
        name=2, midpoint=(RESISTOR.x, RESISTOR.ymax), width=pad_size[1], orientation=90
    )
    sq_actual = 0.5 * (pfa.get_squares(dummy, 2)[1] + pfa.get_squares(m, 2)[1])
    RESISTOR << VIAS
    RESISTOR.rotate(90)
    text = pg.text(
        f"W/sq\n{width}/{round(sq_actual)}", layer=layer_set[layer_name].gds_layer
    )
    # align to drain / mesa
    text.move((RESISTOR.xmin + pad_size[1] / 2 - text.x, RESISTOR.ymax - text.ymin + 5))
    RESISTOR << text
    RESISTOR << pg.union(text, layer=layer_set["sourcedrain"].gds_layer)
    return RESISTOR


def step_heights(
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates test structures for measuring step heights of various layers.

    Parameters:
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: test step heights
    """
    STEPS = Device(f"STEPS")
    # gate
    gs = STEPS << pg.rectangle((50, 50), layer=layer_set["gate"].gds_layer)
    # via
    os = STEPS << pg.rectangle((50, 50), layer=layer_set["via"].gds_layer)
    os.move(gs.center - os.center + (100, 0))
    # gate + via
    gs_ox1 = STEPS << pg.rectangle((50, 50), layer=layer_set["gate"].gds_layer)
    gs_ox2 = STEPS << pg.rectangle((60, 60), layer=layer_set["via"].gds_layer)
    gs_ox1.move(os.center - gs_ox1.center + (100, 0))
    gs_ox2.move(os.center - gs_ox2.center + (100, 0))
    # source/drain
    sd = STEPS << pg.rectangle((50, 50), layer=layer_set["sourcedrain"].gds_layer)
    sd.move(gs.center - sd.center + (0, -100))
    # ITO
    ms = STEPS << pg.rectangle((50, 50), layer=layer_set["mesa"].gds_layer)
    ms.move(sd.center - ms.center + (100, 0))
    return STEPS


def via_tests(
    num_vias: List[int] = [10, 20, 30],
    wire_width: float = 2,
    pad_size: Tuple[float, float] = (100, 100),
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates test structures for measuring vias.

    Parameters:
        num_vias (List[int]): increasing list of number of vias
        wire_width (float): width of wire
        pad_size (tuple(float,float)): pad length and width
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: via test array
    """
    VIA_TEST = Device(f"VIA_TEST({num_vias}, {wire_width})")
    vt = lambda nv: test_via(
        num_vias=nv,
        wire_width=wire_width,
        via_width=wire_width,
        via_spacing=4 * wire_width,
        pad_size=pad_size,
        min_pad_spacing=0,
        pad_layer=layer_set["sourcedrain"].gds_layer,
        wiring1_layer=layer_set["sourcedrain"].gds_layer,
        wiring2_layer=layer_set["gate"].gds_layer,
        via_layer=layer_set["via"].gds_layer,
    )
    sweep = VIA_TEST << pg.gridsweep(
        function=vt,
        param_x={"nv": num_vias},
        param_y={},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )

    return VIA_TEST


def tlm(
    contact_l: float = 10,
    spacings: List[float] = [10, 10, 20, 50, 80, 100, 200],
    contact_w: float = 100,
    via_layer: int = None,
    finger_layer: int = 3,
    mesa_layer: int = 4,
    gate_layer: int = 1,
    pad_size: Tuple[float, float] = (80, 80),
) -> Device:
    """Creates transfer-length-method test structures.

    Parameters:
        contact_l (float): length of metal contact on semiconductor
        spacings (List[float]): list of spacings between contacts
        contact_w (float): width of contact/semiconductor
        via_layer (int): if not None, layer to put via on
        finger_layer (int): layer for metal fingers
        mesa_layer (int): layer for semiconductor
        gate_layer (int): if not None, layer to put gate on
        pad_size (tuple(float,float)): width, height of pad

    Returns:
        Device: TLM structure
    """
    TLM = Device(f"TLM({contact_w},{spacings})")
    if gate_layer == finger_layer:
        # can't have gated TLM with contacts on the same layer as gate
        return TLM
    xoff = 0
    for n, space in enumerate(spacings):
        fp_w = space + 2 * contact_l
        w = contact_w * 1.2 + 10
        for i in range(2):
            fp = TLM << pg.flagpole(
                size=(fp_w, pad_size[1]),
                stub_size=(contact_l, w),
                shape=("d" if i % 2 else "p"),
                taper_type=None,
                layer=finger_layer,
            )
            if i % 2:
                fp.movey(-fp.ymax + contact_w / 2 + 5)
                fp.movex(xoff - fp.xmax)
            else:
                fp.movey(-fp.ymin - contact_w / 2 - 5)
                fp.movex(xoff - fp.xmin + 50)
            if via_layer is not None:
                via = TLM << pg.rectangle(
                    size=(contact_l, contact_w + 10), layer=via_layer
                )
                if i % 2:
                    via.move((fp.xmax - contact_l / 2 - via.x, -via.y))
                else:
                    via.move((fp.xmin + contact_l / 2 - via.x, -via.y))
                # add vias to lower metal pads
                # pad_via = TLM << pg.rectangle(size=(fp_w, pad_size[1]), layer=
            xoff = fp.xmax
        text = TLM << pg.text(str(space), layer=finger_layer)
        text.move((xoff - text.xmin + 5, -w / 2 - pad_size[1] + 10 - text.ymin))
        if gate_layer is not None:
            TLM << pg.union(text, layer=gate_layer)
    # add mesa
    mesa = pg.rectangle(size=(TLM.xsize + 50, contact_w), layer=mesa_layer)
    mesa.move((TLM.x - mesa.x, -mesa.y))
    # add gate
    if gate_layer is not None:
        gate = pg.rectangle(size=(mesa.xsize + 10, contact_w + 10), layer=gate_layer)
        gate.move((mesa.xmin - gate.xmin - 5, -gate.y))
        gate_pad = pg.rectangle(size=(TLM.xsize, pad_size[1]), layer=gate_layer)
        gate_pad.move((TLM.x - gate_pad.x, TLM.ymax - gate_pad.ymin + 10))
        gate_wire = pg.rectangle(size=(40, TLM.ysize / 2), layer=gate_layer)
        gate_wire.move(
            (
                TLM.xmin + 2 * contact_l + spacings[0] + 5 - gate_wire.xmin,
                gate.ymax - gate_wire.ymin - 10,
            )
        )
        TLM << gate
        TLM << gate_pad
        TLM << gate_wire

    TLM << mesa
    return TLM


def test_chip(ls: LayerSet = LayerSet()) -> Device:
    #### parameters to sweep ###

    # transistors
    L_gate = [1, 2, 3, 5, 10, 20, 50]
    L_overlap = [2, 5, 10]
    W_channel = [5, 10, 20, 50, 100]

    # MIM/MOS capacitors
    L_cap = [5, 10, 20, 50, 100, 200]
    W_cap = [5, 10, 20, 50, 100]

    # ITO resistors
    L_resistor = [2, 5, 10, 20, 50, 100]
    W_resistor = [10, 20, 50, 100]

    # W resistors
    SQ_resistor = [50, 100, 500]

    # via tests
    via_counts = [2, 50, 5, 10, 20]
    via_test_w = 8

    # tlm options
    tlm_contact_l = 50
    tlm_contact_w = 50
    tlm_spacings = [10, 20, 50, 80, 100, 150]
    tlm_pad_size = (100, 100)

    TOP = Device("top")
    RESISTOR_ARRAY = Device("resistors")

    sample_w = 5000
    pad_size = (100, 100)

    # create alignment marks
    align = alignment_mark(layers=[l.gds_layer for _, l in ls._layers.items()])
    alignment_marks = TOP << align
    alignment_marks.move((-alignment_marks.xmin, -alignment_marks.ymin))

    # create lithography structures
    LITHO = Device("LITHO")
    resolutions = [1, 1.5, 2]
    align_dummy = alignment_mark(
        layers=[l.gds_layer for _, l in ls._layers.items()][:2]
    )
    n_shift = {"gate": 0, "via": 1, "sourcedrain": 2, "mesa": 3}
    for layer_name, layer in ls._layers.items():
        for i in range(2):
            rt = resolution_test(resolutions, inverted=i, layer=layer.gds_layer)
            rt.flatten()
            rt.move(-rt.center)
            rt_i = LITHO << rt
            shift_x = (
                0
                - rt_i.xmin
                + i * (rt.xsize + 50)
                + n_shift[layer_name] * (align_dummy.xsize - 50)
                + 150
            )
            shift_y = (
                3 * (align_dummy.ysize + 25)
                - rt_i.ymin
                + 100
                - n_shift[layer_name] * (align_dummy.ysize + 40)
            )
            rt_i.move((shift_x, shift_y))
    litho = TOP << LITHO

    # create VDP structures
    # gated VDP
    for i in range(2):
        vdp = gated_vdp(
            gated=True,
            rotation=i * 45,
            pad_size=pad_size,
            layer_set=ls,
        )
        vdp_i = TOP << vdp
        shift_x = 0 - vdp_i.xmin + 1200 + i * (vdp_i.xsize + 100)
        shift_y = 3 * (align_dummy.ysize + 25) - vdp_i.ymin
        vdp_i.move((shift_x, shift_y))
    # ungated VDP
    for i in range(2):
        vdp = gated_vdp(
            gated=False,
            rotation=i * 45,
            pad_size=pad_size,
            layer_set=ls,
        )
        vdp_i = TOP << vdp
        shift_x = 2400 - vdp_i.xmin
        shift_y = align_dummy.ysize + 25 - vdp_i.ymin + i * (vdp_i.ysize + 100)
        vdp_i.move((shift_x, shift_y))

    # create step-height test structures
    sh_i = TOP << step_heights(ls)
    shift_x = 2400 - sh_i.xmin
    shift_y = 3 * (align_dummy.ysize + 25) - sh_i.ymin
    sh_i.move((shift_x, shift_y))

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
    mos.move((2900 - mos.xmin, -mos.ymin))
    mim.move((2900 - mim.xmin, mos.ymax - mim.ymin + 50))

    # create transistors
    TRANSISTOR = pg.gridsweep(
        function=lambda L_ov, W, L_g: transistor(
            L_mesa=L_ov * 2 + L_g - 1,
            L_gate=L_g,
            L_overlap=L_ov,
            W_mesa=W,
            W_contact=W + 4,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_y={"L_g": L_gate},
        param_x={"L_ov": L_overlap, "W": W_channel},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    trans = TOP << TRANSISTOR
    trans.move((sample_w / 2 - trans.x, litho.ymax + 30 - trans.ymin))

    # create ITO resistors
    RESISTOR = pg.gridsweep(
        function=lambda L, W: transistor(
            L_mesa=L + 20,
            L_gate=0,
            L_overlap=10,
            W_mesa=W,
            W_contact=W + 2,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_x={"L": L_resistor},
        param_y={"W": W_resistor},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    ito_res = TOP << RESISTOR
    ito_res.move((trans.xmin - ito_res.xmin, trans.ymax + 50 - ito_res.ymin))

    # create W resistors
    W_RESISTOR = pg.gridsweep(
        function=lambda sq, layer_name: metal_resistor(
            width=5,
            squares=sq,
            layer_name=layer_name,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_x={"sq": SQ_resistor, "layer_name": ["gate", "sourcedrain"]},
        param_y={},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    w_res = TOP << W_RESISTOR
    w_res.move((trans.xmax - w_res.xmax, trans.ymin - w_res.ymax - 50))

    # create TLM
    tlm_fn = lambda gated, bot: tlm(
        contact_l=tlm_contact_l,
        spacings=tlm_spacings,
        contact_w=tlm_contact_w,
        via_layer=ls["via"].gds_layer if bot else None,
        finger_layer=ls["gate"].gds_layer if bot else ls["sourcedrain"].gds_layer,
        mesa_layer=ls["mesa"],
        gate_layer=ls["gate"].gds_layer if gated else None,
        pad_size=tlm_pad_size,
    )
    tlm_1 = TOP << pg.gridsweep(
        function=lambda bot: tlm_fn(False, bot),
        param_x={},
        param_y={"bot": [True, False]},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    tlm_2 = TOP << tlm_fn(True, False)
    tlm_1.move((ito_res.xmax - tlm_1.xmin + 20, trans.ymax - tlm_1.ymin + 50))
    tlm_2.move((tlm_1.xmax - tlm_2.xmin + 20, trans.ymax - tlm_2.ymin + 20))

    # create via test structures
    VIA_TESTS_1 = via_tests(
        num_vias=via_counts[2:], wire_width=via_test_w, pad_size=pad_size, layer_set=ls
    )
    VIA_TESTS_2 = via_tests(
        num_vias=via_counts[:2], wire_width=via_test_w, pad_size=pad_size, layer_set=ls
    )
    vt1 = TOP << VIA_TESTS_1
    vt2 = TOP << VIA_TESTS_2
    vt1.move((tlm_1.xmax - vt1.xmin + 20, tlm_2.ymax - vt1.ymin + 20))
    vt2.move((tlm_1.xmax - vt2.xmin + 20, vt1.ymax - vt2.ymin + 20))

    return TOP


if __name__ == "__main__":
    ls = LayerSet()
    ls.add_layer(
        name="gate",
        gds_layer=1,
        gds_datatype=0,
        description="tungsten gate",
        color=(0.6, 0.7, 0.9),
    )
    ls.add_layer(
        name="via",
        gds_layer=2,
        gds_datatype=0,
        description="oxide via",
        color=(0.8, 0.7, 0.2),
    )
    ls.add_layer(
        name="sourcedrain",
        gds_layer=3,
        gds_datatype=0,
        description="tungsten/nickel source/drain",
        color=(0.5, 0.4, 0.4),
    )
    ls.add_layer(
        name="mesa",
        gds_layer=4,
        gds_datatype=0,
        description="ito/igzo mesa",
        color=(0.6, 0.2, 0.5),
    )
    T = test_chip(ls)
    # array
    A = Device("array")
    for i in range(8):
        for j in range(8):
            ij = A << T
            ij.move(-ij.center)
            ij.move((7000 * i, 7000 * j))
            label = A << pg.text(
                text=chr(0x41 + (7 - j)) + str(i + 1),
                size=300,
                layer=ls["gate"].gds_layer,
            )
            label.move((ij.xmin - label.xmin, ij.ymin - label.ymin))
            label.move((1750, 1100))
    A.move(-A.center)
    for _, l in ls._layers.items():
        X = pg.cross(length=100, width=2, layer=l.gds_layer)
        C = pg.rectangle(size=(10, 10), layer=l.gds_layer)
        for i in range(2):
            for j in range(2):
                x = A << X
                x.move((27200 * (-1) ** i, 27200 * (-1) ** j))
                c = A << C
                c.move((27295 * (-1) ** i - c.x, 27295 * (-1) ** j - c.y))
    A.write_gds(
        "ito_test.gds",
        unit=1e-6,
        precision=1e-9,
        auto_rename=True,
        max_cellname_length=28,
        cellname="top",
    )

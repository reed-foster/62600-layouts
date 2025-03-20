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
    cover_bottom: bool = True,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MOS capacitor between gate and mesa, with contact on
    sourcedrain.

    Parameters:
        L_overlap (float): overlap between gate and mesa
        L_contact (float): overlap (contact) between sourcedrain and mesa
        W (float): width of capacitor structure
        cover_bottom (bool): if True, include a pad on sourcedrain layer that overlaps gate layer
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
    if cover_bottom:
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
    text.move((t.x - text.x, t.y + pad_size[1] / 2 + 10 - text.ymin))
    MOS << pg.union(text, layer=layer_set["sourcedrain"].gds_layer)

    return MOS


def mim_cap(
    L_overlap: float = 100,
    W: float = 100,
    cover_bottom: bool = True,
    layer_set: LayerSet = LayerSet(),
    pad_size: Tuple[float, float] = (100, 100),
) -> Device:
    """Creates a MIM capacitor between the two layers gate and sourcedrain.

    Parameters:
        L_overlap (float): amount to extend pads to overlap
        W (float): width of overlapped region
        cover_bottom (bool): if True, include a pad on sourcedrain layer that overlaps gate layer
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
    if cover_bottom:
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
    cover_bottom: bool = True,
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
        cover_bottom (bool): if True, include a pad on sourcedrain layer that overlaps gate layer
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
    if cover_bottom:
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
    if cover_bottom:
        gate_via_cover.move(gate_pad.center - gate_via_cover.center)
        gate_via_conn.move((gate.x - gate_via_conn.x, gate.ymax - gate_via_conn.ymax))
    if L_gate != 0:
        TRANSISTOR << gate_pad
        TRANSISTOR << gate_via
        if cover_bottom:
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


def vdp_ito(
    gated: bool = True,
    rotation: float = 0,
    contact_size: Tuple[float, float] = (5, 10),
    pad_size: Tuple[float, float] = (100, 100),
    pad_layer: str = "sourcedrain",
    cover_bottom: bool = True,
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates Van-der-Pauw test structure, with optional back gate.

    Parameters:
        gated (bool): if true, include back gate
        rotation (float): rotation of test structure in degrees
        contact_size (tuple(float, float)): size of contact between pad and mesa
        pad_layer (str): name of layer to put pads on. If gate, will also add necessary via
        cover_bottom (bool): if True, include a pad on sourcedrain layer that overlaps gate layer
        pad_size (tuple(float,float)): pad length and width
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: VDP structure
    """
    VDP = Device(f"VDP({gated})")
    ito = VDP << vdp(
        l=2 * max(pad_size), w=contact_size[0], layer=layer_set["mesa"].gds_layer
    )
    pad = pg.rectangle(pad_size, layer=layer_set[pad_layer].gds_layer)
    pad.move((-pad.xmin, -pad.y))
    contact = pad << pg.rectangle(
        (2 * contact_size[1], contact_size[0]), layer=layer_set[pad_layer].gds_layer
    )
    contact.move((-contact.xmax, -contact.y))
    if pad_layer == "gate":
        pad << pg.union(pad, layer=layer_set["via"].gds_layer)
    pad.add_port(
        name=1,
        midpoint=(contact.xmin + contact_size[1], contact.y),
        orientation=180,
        width=10,
    )
    pads = {}
    for p in ito.ports:
        pad_i = VDP << pad
        pad_i.connect(pad_i.ports[1], ito.ports[p])
        pads[p] = pad_i
    if gated:
        gate = VDP << vdp(
            l=2 * max(pad_size) + 10,
            w=contact_size[0] + 5,
            layer=layer_set["gate"].gds_layer,
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
        if cover_bottom:
            via_cover = VDP << pg.rectangle(
                (pad_size[0] + 2, pad_size[1] + 2),
                layer=layer_set["sourcedrain"].gds_layer,
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


def vdp_metal(
    metal_layer: str = "sourcedrain",
    rotation: float = 0,
    pad_size: Tuple[float, float] = (100, 100),
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates Van-der-Pauw test structure.

    Parameters:
        metal_layer (string): name of layer on which to place VDP cell
        rotation (float): rotation of test structure in degrees
        pad_size (tuple(float,float)): pad length and width
        layer_set (LayerSet): layer set to generate alignment marks for

    Returns:
        Device: VDP structure
    """
    VDP = Device(f"VDP({metal_layer})")
    gds_layer = layer_set[metal_layer].gds_layer
    mesa = VDP << vdp(l=2 * max(pad_size), w=10, layer=gds_layer)
    pad = pg.rectangle(pad_size, layer=gds_layer)
    pad.move((-pad.xmin, -pad.y))
    if metal_layer == "gate":
        via = pg.rectangle(pad_size, layer=layer_set["via"].gds_layer)
        via.move(pad.center - via.center)
        pad << via
    contact = pad << pg.rectangle((20, 10), layer=gds_layer)
    contact.move((-contact.xmax, -contact.y))
    pad.add_port(
        name=1, midpoint=(contact.xmin + 5, contact.y), orientation=180, width=10
    )
    pads = {}
    for p in mesa.ports:
        pad_i = VDP << pad
        pad_i.connect(pad_i.ports[1], mesa.ports[p])
        pads[p] = pad_i
    VDP.rotate(rotation)
    return VDP


def metal_resistor(
    width: float = 5,
    squares: float = 50,
    layer_name: str = "gate",
    cover_bottom: bool = True,
    pad_size: Tuple[float, float] = (100, 100),
    layer_set: LayerSet = LayerSet(),
) -> Device:
    """Creates meandered metal resistor.

    Parameters:
        width (float): wire width in microns
        squares (float): number of squares
        layer_name (string): name of layer to define resistor on
        cover_bottom (bool): if True, include a pad on sourcedrain layer that overlaps gate layer
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
    if cover_bottom:
        via_cover = pg.rectangle(
            (pad_size[0] + 2, pad_size[1] + 2), layer=layer_set["sourcedrain"].gds_layer
        )
        via_conn = pg.rectangle(
            (width + 2, 2), layer=layer_set["sourcedrain"].gds_layer
        )
    for i in range(2):
        contact_i = RESISTOR << contact
        contact_i.connect(contact_i.ports[1], m.ports[i + 1])
        if layer_name == "gate":
            via_i = VIAS << via
            via_i.move(contact_i.center - via_i.center)
            if cover_bottom:
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
    # sq_actual = 0.5 * (pfa.get_squares(dummy, 5)[1] + pfa.get_squares(m, 5)[1])
    sq_actual = squares
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


def rect_tlm(
    contact_l: float = 10,
    spacings: List[float] = [10, 10, 20, 50, 80, 100, 200],
    contact_w: float = 100,
    via_layer: int = 2,
    finger_layer: int = 3,
    pad_layer: int = 3,
    mesa_layer: int = 4,
    gate_layer: int = 1,
    cover_bottom: bool = True,
    pad_size: Tuple[float, float] = (80, 80),
) -> Device:
    """Creates rectangular transfer-length-method test structures.

    Parameters:
        contact_l (float): length of metal contact on semiconductor
        spacings (List[float]): list of spacings between contacts
        contact_w (float): width of contact/semiconductor
        via_layer (int): layer to put via on
        finger_layer (int): layer for metal fingers
        pad_layer (int): layer for metal pads
        mesa_layer (int): layer for semiconductor
        gate_layer (int): if not None, layer to put gate on
        cover_bottom (bool): if True, cover finger layer/gate layer with pad layer
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
            xoff = fp.xmax
            if finger_layer < via_layer:
                via = TLM << pg.rectangle(
                    size=(contact_l, contact_w + 10), layer=via_layer
                )
                if i % 2:
                    via.move((fp.xmax - contact_l / 2 - via.x, -via.y))
                else:
                    via.move((fp.xmin + contact_l / 2 - via.x, -via.y))
                if pad_layer != finger_layer:
                    # add vias to lower metal pads
                    pad_via = TLM << pg.rectangle(
                        size=(fp_w, pad_size[1]), layer=via_layer
                    )
                    pad_via.movex(fp.xmax - pad_via.xmax)
                    if i % 2:
                        pad_via.movey(fp.ymin - pad_via.ymin)
                    else:
                        pad_via.movey(fp.ymax - pad_via.ymax)
                    if cover_bottom:
                        top_pad = TLM << pg.rectangle(
                            size=(fp_w + 2, pad_size[1] + 2), layer=pad_layer
                        )
                        top_pad.move(pad_via.center - top_pad.center)
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
        pad_via = TLM << pg.rectangle(
            size=(gate_pad.xsize, pad_size[1]), layer=via_layer
        )
        pad_via.move(gate_pad.center - pad_via.center)
        if cover_bottom:
            top_pad = TLM << pg.rectangle(
                size=(gate_pad.xsize + 2, pad_size[1] + 2), layer=pad_layer
            )
            top_pad.move(gate_pad.center - top_pad.center)

    TLM << mesa
    return TLM


def circ_tlm(
    pad_radius: float = 50,
    spacings: List[float] = [10, 10, 20, 50, 80, 100, 200],
    pad_layer: int = 3,
    mesa_layer: int = 4,
) -> Device:
    """Creates circular transfer-length-method test structures.

    Parameters:
        pad_radius (float): radius of center pad
        spacings (float): distance between center pad and external contact
        pad_layer (int): layer for metal pads
        mesa_layer (int): layer for semiconductor

    Returns:
        Device: TLM structure
    """
    TLM = Device(f"TLM({spacings})")

    def pad(int_radius: float, ext_radius: float):
        PAD = Device(f"PAD({int_radius},{ext_radius})")
        big_circ = PAD << pg.circle(radius=ext_radius, layer=mesa_layer)
        PAD << pg.circle(radius=int_radius, layer=pad_layer)
        text = PAD << pg.text(f"R={ext_radius},{int_radius}", layer=mesa_layer)
        text.move((big_circ.x - text.x, big_circ.ymin - text.ymax - 10))
        return PAD

    Dlist = [
        pad(int_radius=pad_radius, ext_radius=pad_radius + space) for space in spacings
    ]
    cuts = pg.packer(
        Dlist,
        spacing=50,
        aspect_ratio=(1, 1),
        max_size=(None, None),
        sort_by_area=True,
        density=2,
    )[0]
    mesa = TLM << pg.rectangle((cuts.xsize + 100, cuts.ysize + 100), layer=mesa_layer)
    mesa.move(cuts.center - mesa.center)
    pads = TLM << pg.kl_boolean(mesa, cuts, "A-B", layer=pad_layer)
    TLM << cuts
    TLM = pg.union(TLM, by_layer=True)
    TLM.name = f"TLM({spacings})"
    return TLM


def test_chip(cover_bottom: bool = True, ls: LayerSet = LayerSet()) -> Device:
    #### parameters to sweep ###

    # transistors
    L_gate = [1, 1, 1.5, 1.5, 2, 2, 3, 3, 5, 5, 10, 10, 20, 20, 50, 50]
    L_overlap = [1, 2, 5, 10]
    W_channel = [2, 5, 10, 20, 50, 100]

    # MIM/MOS capacitors
    L_cap = [2, 5, 10, 20, 50, 100, 200]
    W_cap = [2, 2, 5, 5, 10, 10, 20, 20, 50, 100, 200]

    # ITO resistors
    L_resistor = [1, 2, 5, 10, 15, 20, 50, 100]
    W_resistor = [1, 2, 5, 10, 20, 50, 100, 200]

    # W resistors
    SQ_resistor = [49, 99, 200, 500, 1000, 2000]

    # via tests
    via_counts = [2, 4, 8, 10, 20, 50, 100, 250]
    via_test_w = 8

    # rect_tlm options
    tlm_contact_l = 50
    tlm_contact_w = 50
    tlm_spacings = [10, 20, 50, 100, 200, 500, 1000]
    tlm_pad_size = (100, 100)

    circ_tlm_spacings = [1, 2, 3, 5, 10, 15, 20, 30, 50, 80, 100, 200]

    TOP = Device("top")

    sample_w = 7800
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

    # create step-height test structures
    sh_i = TOP << step_heights(ls)
    sh_i.rotate(90)
    shift_x = 1200 - sh_i.xmin
    shift_y = 3 * (align_dummy.ysize + 25) - sh_i.ymin - 50
    sh_i.move((shift_x, shift_y))

    # create circular TLM
    circ_tlm_i = TOP << circ_tlm(
        pad_radius=40,
        spacings=circ_tlm_spacings,
        pad_layer=ls["sourcedrain"].gds_layer,
        mesa_layer=ls["mesa"].gds_layer,
    )

    circ_tlm_i.move((litho.xmax - circ_tlm_i.xmax, litho.ymax - circ_tlm_i.ymax))

    # create MOS CAP and MIM CAP test structures
    MOS = pg.gridsweep(
        function=lambda L, W: mos_cap(L, 10, W, cover_bottom, ls, pad_size),
        param_x={"L": L_cap},
        param_y={"W": W_cap},
        spacing=(70, 50) if cover_bottom else (71, 51),
        separation=True,
        label_layer=None,
    )
    MIM = pg.gridsweep(
        function=lambda L, W: mim_cap(L, W, cover_bottom, ls, pad_size),
        param_x={"L": L_cap},
        param_y={"W": W_cap},
        spacing=(70, 50) if cover_bottom else (71, 51),
        separation=True,
        label_layer=None,
    )
    mos = TOP << MOS
    mim = TOP << MIM
    mos.move((sample_w - mos.xmax, -mos.ymin))
    mim.move((mos.xmin - mim.xmax - 50, -mim.ymin))
    if not cover_bottom:
        mos.move((1, 1))
        mim.move((1, 1))

    # create W resistors
    METAL_RESISTOR = pg.gridsweep(
        function=lambda sq, layer_name: metal_resistor(
            width=5,
            squares=sq,
            layer_name=layer_name,
            cover_bottom=cover_bottom,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_x={"sq": SQ_resistor, "layer_name": ["gate", "sourcedrain"]},
        param_y={},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    metal_res = TOP << METAL_RESISTOR
    metal_res.move((sample_w - metal_res.xmax, mim.ymax - metal_res.ymin + 50))
    # create via test structures
    vt = TOP << via_tests(
        num_vias=via_counts, wire_width=via_test_w, pad_size=pad_size, layer_set=ls
    )
    vt.move((metal_res.xmax - vt.xmax, metal_res.ymin + pad_size[1] + 50 - vt.ymin))

    # create transistors
    TRANSISTOR = pg.gridsweep(
        function=lambda L_ov, W, L_g: transistor(
            L_mesa=L_ov * 2 + L_g - 1,
            L_gate=L_g,
            L_overlap=L_ov,
            W_mesa=W,
            W_contact=W + 4,
            cover_bottom=cover_bottom,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_y={"L_g": L_gate},
        param_x={"L_ov": L_overlap, "W": W_channel},
        spacing=(55, 30) if cover_bottom else (55, 31),
        separation=True,
        label_layer=None,
    )
    trans = TOP << TRANSISTOR
    trans.move((sample_w / 2 - trans.x, vt.ymax + 50 - trans.ymin))

    # create ITO resistors
    RESISTOR = pg.gridsweep(
        function=lambda L, W: transistor(
            L_mesa=L + 100,
            L_gate=0,
            L_overlap=50,
            W_mesa=W,
            W_contact=W + 2,
            cover_bottom=cover_bottom,
            layer_set=ls,
            pad_size=pad_size,
        ),
        param_x={"L": L_resistor},
        param_y={"W": W_resistor},
        spacing=(50, 20),
        separation=True,
        label_layer=None,
    )
    ito_res = TOP << RESISTOR
    ito_res.move((trans.xmin - ito_res.xmin, trans.ymax + 50 - ito_res.ymin))

    # create ITO TLM
    tlm_fn = lambda gated, bot: rect_tlm(
        contact_l=tlm_contact_l,
        spacings=tlm_spacings,
        contact_w=tlm_contact_w,
        via_layer=ls["via"].gds_layer,
        finger_layer=ls["gate"].gds_layer if bot else ls["sourcedrain"].gds_layer,
        pad_layer=ls["sourcedrain"].gds_layer,
        mesa_layer=ls["mesa"].gds_layer,
        gate_layer=ls["gate"].gds_layer if gated else None,
        cover_bottom=cover_bottom,
        pad_size=tlm_pad_size,
    )
    tlm_i = TOP << pg.gridsweep(
        function=lambda gated_bot: tlm_fn(gated_bot[0], gated_bot[1]),
        param_x={},
        param_y={"gated_bot": [(True, False), (False, True), (False, False)]},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    tlm_i.move((ito_res.xmax - tlm_i.xmin + 20, trans.ymax - tlm_i.ymin + 50))

    # create W TLM
    w_tlm = TOP << rect_tlm(
        contact_l=tlm_contact_l,
        spacings=tlm_spacings,
        contact_w=tlm_contact_w,
        via_layer=ls["via"].gds_layer,
        finger_layer=ls["sourcedrain"].gds_layer,
        pad_layer=ls["sourcedrain"].gds_layer,
        mesa_layer=ls["gate"].gds_layer,
        gate_layer=None,
        cover_bottom=False,
        pad_size=tlm_pad_size,
    )
    w_tlm.move((tlm_i.xmin - w_tlm.xmin, tlm_i.ymax - w_tlm.ymin + 50))

    # create VDP structures
    # gated VDP
    tlm_xmax = 10 * ((max(tlm_i.xmax, w_tlm.xmax) + 9) // 10)
    vdp = TOP << pg.gridsweep(
        function=lambda gated, rotation: vdp_ito(
            gated=gated,
            rotation=rotation,
            contact_size=(20, 10),
            cover_bottom=cover_bottom,
            pad_layer="sourcedrain",
            pad_size=pad_size,
            layer_set=ls,
        ),
        param_x={"gated": [True, False]},
        param_y={"rotation": [0, 45]},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    vdp.move((tlm_xmax - vdp.xmin + 50, trans.ymax - vdp.ymin + 50))
    vdp_m = TOP << pg.gridsweep(
        function=lambda layer: vdp_metal(
            metal_layer=layer,
            rotation=45,
            pad_size=pad_size,
            layer_set=ls,
        ),
        param_x={},
        param_y={"layer": ["sourcedrain", "gate"]},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    vdp_xmax = 10 * ((vdp.xmax + 9) // 10)
    vdp_m.move((vdp_xmax - vdp_m.xmin + 50, vdp.ymin - vdp_m.ymin))

    # gated VDP with fat overlap for high-current hall measurements
    vdp_fat = TOP << pg.gridsweep(
        function=lambda rotation: vdp_ito(
            gated=True,
            rotation=rotation,
            contact_size=(50, 20),
            cover_bottom=cover_bottom,
            pad_layer="sourcedrain",
            pad_size=pad_size,
            layer_set=ls,
        ),
        param_x={"rotation": [0, 45]},
        param_y={},
        spacing=(50, 50),
        separation=True,
        label_layer=None,
    )
    vdp_ymax = 10 * ((vdp.ymax + 9) // 10)
    vdp_fat.move((tlm_xmax - vdp_fat.xmin + 50, vdp_ymax - vdp_fat.ymin + 50))

    # bottom TLM (tungsten pads)
    vdp_w = TOP << vdp_ito(
        gated=False,
        rotation=45,
        contact_size=(20, 10),
        cover_bottom=False,
        pad_layer="gate",
        pad_size=pad_size,
        layer_set=ls,
    )
    vdp_w.move((vdp_xmax - vdp_w.xmin + 50, vdp_ymax - vdp_w.ymin + 50))

    return TOP


def standard_test_structures(ls: LayerSet = LayerSet()):
    T1 = test_chip(False, ls)
    T2 = test_chip(True, ls)
    # array
    A = Device("array")
    N_row = 3
    N_col = 3
    for i in range(N_col):
        for j in range(N_row):
            cover_bottom = (i + j) % 2
            ij = A << (T1 if cover_bottom == 0 else T2)
            ij.move(-ij.center)
            ij.movey(0 if cover_bottom == 0 else 0.5)
            # ij.movex(0 if cover_bottom == 0 else 0.5)
            ij.move((10000 * i, 10000 * j))
            label = A << pg.text(
                text=chr(0x41 + (N_row - 1 - j)) + str(i + 1),
                size=400,
                layer=ls["gate"].gds_layer,
            )
            label.move((ij.xmin - label.xmin, ij.ymin - label.ymin))
            label.move((2300, 500))
    A.move(-A.center)
    return A


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
        description="nickel/gold source/drain",
        color=(0.5, 0.4, 0.4),
    )
    ls.add_layer(
        name="mesa",
        gds_layer=4,
        gds_datatype=0,
        description="ito mesa",
        color=(0.6, 0.2, 0.5),
    )
    A = standard_test_structures(ls)
    A.write_gds(
        "standard_test_structures.gds",
        unit=1e-6,
        precision=1e-9,
        auto_rename=True,
        max_cellname_length=28,
        cellname="top",
    )

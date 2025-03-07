from torch import nn
from torchmore import layers
from torchmore import flex
from torchmore import combos
from torchmore import inputstats
from .utils import model
from . import ocrlayers


@model
def text_model_210113(noutput):
    model = nn.Sequential(
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        *combos.conv2d_block(32, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(48, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(64, 3, mp=2, repeat=2),
        *combos.conv2d_block(96, 3, repeat=2),
        flex.Lstm2(100),
        layers.Fun("lambda x: x.max(2)[0]"),
        flex.ConvTranspose1d(400, 1, stride=2),
        flex.Conv1d(100, 3),
        flex.BatchNorm1d(),
        nn.ReLU(),
        layers.Reorder("BDL", "LBD"),
        flex.LSTM(100, bidirectional=True),
        layers.Reorder("LBD", "BDL"),
        flex.Conv1d(noutput, 1),
    )
    flex.shape_inference(model, (1, 1, 48, 300))
    return model


@model
def segmentation_model_210113(noutput=4):
    model = nn.Sequential(
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        layers.ModPad(8),
        layers.KeepSize(
            sub=nn.Sequential(
                *combos.conv2d_block(32, 3, mp=2, repeat=2),
                *combos.conv2d_block(48, 3, mp=2, repeat=2),
                *combos.conv2d_block(96, 3, mp=2, repeat=2),
                flex.BDHW_LSTM(100),
            )
        ),
        flex.BDHW_LSTM(40),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 256, 256))
    return model


@model
def segmentation_model_210117(noutput=4):
    model = nn.Sequential(
        inputstats.InputStats("segmodel"),
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        layers.ModPad(8),
        layers.KeepSize(
            sub=nn.Sequential(
                *combos.conv2d_block(32, 3, mp=2, repeat=2),
                *combos.conv2d_block(48, 3, mp=2, repeat=2),
                *combos.conv2d_block(96, 3, mp=2, repeat=2),
                flex.BDHW_LSTM(100),
            )
        ),
        flex.BDHW_LSTM(40),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 256, 256))
    return model


@model
def text_model_210118(noutput):
    model = nn.Sequential(
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("textmodel"),
        *combos.conv2d_block(32, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(48, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(64, 3, mp=2, repeat=2),
        *combos.conv2d_block(96, 3, repeat=2),
        flex.Lstm2(100),
        layers.Fun("lambda x: x.max(2)[0]"),
        flex.ConvTranspose1d(400, 1, stride=2),
        flex.Conv1d(100, 3),
        flex.BatchNorm1d(),
        nn.ReLU(),
        layers.Reorder("BDL", "LBD"),
        flex.LSTM(100, bidirectional=True),
        layers.Reorder("LBD", "BDL"),
        flex.Conv1d(noutput, 1),
    )
    flex.shape_inference(model, (1, 1, 48, 300))
    return model


@model
def segmentation_model_210118(noutput=4):
    model = nn.Sequential(
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("segmodel"),
        layers.ModPad(8),
        layers.KeepSize(
            sub=nn.Sequential(
                *combos.conv2d_block(32, 3, mp=2, repeat=2),
                *combos.conv2d_block(48, 3, mp=2, repeat=2),
                *combos.conv2d_block(96, 3, mp=2, repeat=2),
                flex.BDHW_LSTM(100),
            )
        ),
        flex.BDHW_LSTM(40),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 256, 256))
    return model



@model
def segmentation_model_210218x(noutput=4):
    model = nn.Sequential(
        ocrlayers.GrayDocument(),
        # ocrlayers.Zoom(0.5),
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("segmodel"),
        layers.ModPad(8),
        layers.KeepSize(
            sub=nn.Sequential(
                *combos.conv2d_block(32, 3, mp=2, repeat=2),
                *combos.conv2d_block(48, 3, mp=2, repeat=2),
                *combos.conv2d_block(96, 3, mp=2, repeat=2),
                flex.BDHW_LSTM(100),
            )
        ),
        flex.BDHW_LSTM(40),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 512, 512))
    return model


@model
def segmentation_model_210218(noutput=4):
    model = nn.Sequential(
        ocrlayers.GrayDocument(),
        # ocrlayers.Zoom(0.5),
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("segmodel"),
        layers.ModPad(8),
        combos.make_unet([32, 64, 96], sub=flex.BDHW_LSTM(100)),
        *combos.conv2d_block(48, 3, repeat=2),
        flex.BDHW_LSTM(32),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 512, 512))
    return model


@model
def publaynet_model_210321(noutput=4):
    model = nn.Sequential(
        ocrlayers.GrayDocument(),
        # ocrlayers.Zoom(0.5),
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("segmodel"),
        layers.ModPad(16),
        combos.make_unet([40, 60, 80, 100], sub=flex.BDHW_LSTM(100)),
        *combos.conv2d_block(48, 3, repeat=2),
        flex.BDHW_LSTM(32),
        flex.Conv2d(noutput, 3, padding=1),
    )
    flex.shape_inference(model, (1, 1, 512, 512))
    return model


@model
def cbinarization_210317():
    model = nn.Sequential(
        ocrlayers.GrayDocument(),
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        inputstats.InputStats("cbinarization"),
        layers.ModPad(32),
        combos.make_unet([32, 64, 128, 256, 512], sub=nn.Sequential(*combos.conv2d_block(256, 3, repeat=1))),
        flex.Conv2d(1, 3, padding=1),
        nn.Sigmoid(),
    )
    flex.shape_inference(model, (2, 1, 161, 391))
    return model

from torchmore import flex, layers, combos
from torch import nn


def make_model(noutput):
    model = nn.Sequential(
        layers.Input("BDHW", range=(0, 1), sizes=[None, 1, None, None]),
        *combos.conv2d_block(100, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(200, 3, mp=(2, 1), repeat=2),
        *combos.conv2d_block(300, 3, mp=2, repeat=2),
        *combos.conv2d_block(400, 3, repeat=2),
        flex.Lstm2(400),
        layers.Fun("lambda x: x.max(2)[0]"),
        flex.ConvTranspose1d(400, 1, stride=2),
        flex.Conv1d(400, 3),
        flex.BatchNorm1d(),
        nn.ReLU(),
        layers.Reorder("BDL", "LBD"),
        flex.LSTM(100, bidirectional=True),
        layers.Reorder("LBD", "BDL"),
        flex.Conv1d(noutput, 1),
    )
    flex.shape_inference(model, (1, 1, 48, 300))
    return model

import numpy as np
from rpxdock.data import datadir
from rpxdock import homog as hm

tetrahedral_frames = np.load(datadir + "/tetrahedral_frames.pickle", allow_pickle=True)
octahedral_frames = np.load(datadir + "/octahedral_frames.pickle", allow_pickle=True)
icosahedral_frames = np.load(datadir + "/icosahedral_frames.pickle", allow_pickle=True)

def symframes(sym):
   if isinstance(sym, int) or sym.startswith("C"):
      if not isinstance(sym, int): sym = int(sym[1:])
      return list(hm.hrot([0, 0, 1], np.arange(sym) / sym * 360))
   if sym.startswith("T"):
      return tetrahedral_frames
   if sym.startswith("O"):
      return octahedral_frames
   if sym.startswith("I"):
      return icosahedral_frames

frames = dict(T=tetrahedral_frames, O=octahedral_frames, I=icosahedral_frames)

tetrahedral_axes = {
   2: hm.hnormalized([1, 0, 0]),
   3: hm.hnormalized([1, 1, 1]),
   33: hm.hnormalized([1, 1, -1]),
}  # other c3
octahedral_axes = {
   2: hm.hnormalized([1, 1, 0]),
   3: hm.hnormalized([1, 1, 1]),
   4: hm.hnormalized([1, 0, 0]),
}
icosahedral_axes = {
   2: hm.hnormalized([1, 0, 0]),
   3: hm.hnormalized([0.934172, 0.000000, 0.356822]),
   5: hm.hnormalized([0.850651, 0.525731, 0.000000]),
}
axes = dict(T=tetrahedral_axes, O=octahedral_axes, I=icosahedral_axes)

to_neighbor_olig = dict(
   T={
      2: frames["T"][2],
      3: frames["T"][1],
      33: frames["T"][1]
   },
   O={
      2: frames["O"][2],
      3: frames["O"][1],
      4: frames["O"][1]
   },
   I={
      2: frames["I"][1],
      3: frames["I"][1],
      5: frames["I"][2]
   },
)

axes_second = {s: {k: to_neighbor_olig[s][k] @ v for k, v in axes[s].items()} for s in "TOI"}

# tetrahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# octahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, -0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (-0.000000, -1.000000, -0.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# icosahedral_frames = np.array(
# [
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (+0.000000, -0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, +0.000000, -1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+1.000000, -0.000000, -0.000000, +0.000000),
# (+0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, +0.000000, +0.000000, +0.000000),
# (-0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (+1.000000, +0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, +0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (+0.000000, -0.000000, -1.000000, +0.000000),
# (-1.000000, -0.000000, -0.000000, +0.000000),
# (-0.000000, +1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (+0.000000, -1.000000, -0.000000, +0.000000),
# (+0.000000, +0.000000, +1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-1.000000, -0.000000, +0.000000, +0.000000),
# (-0.000000, +1.000000, +0.000000, +0.000000),
# (-0.000000, -0.000000, -1.000000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.309017, -0.500000, +0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (+0.500000, +0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, +0.809017, +0.000000),
# (-0.500000, -0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (+0.500000, +0.809017, +0.309017, +0.000000),
# (+0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, +0.500000, -0.809017, +0.000000),
# (-0.500000, -0.809017, -0.309017, +0.000000),
# (-0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (+0.500000, -0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, +0.809017, +0.000000),
# (-0.500000, +0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (+0.500000, -0.809017, +0.309017, +0.000000),
# (-0.809017, -0.309017, +0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# (
# (-0.309017, -0.500000, -0.809017, +0.000000),
# (-0.500000, +0.809017, -0.309017, +0.000000),
# (+0.809017, +0.309017, -0.500000, +0.000000),
# (+0.000000, +0.000000, +0.000000, +1.000000),
# ),
# ]
# )
#
# tetrahedral_frames.dump("rpxdock/data/tetrahedral_frames.pickle")
# octahedral_frames.dump("rpxdock/data/octahedral_frames.pickle")
# icosahedral_frames.dump("rpxdock/data/icosahedral_frames.pickle")
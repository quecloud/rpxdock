from time import perf_counter
import numpy as np
import xarray as xr
import homog as hm
import sicdock
from sicdock.sampling import OriCart1Hier_f4
from sicdock.search import hier_sample, expand_samples, hier_evaluate
from sicdock.search import hier_evaluate_executor, filter_redundancy
from sicdock.search import trim_atom_to_res_numbering
from sicdock.util import Bunch
from sicdock.io.io_body import dump_pdb_from_bodies
from sicdock.sym import symframes


def make_cyclic(monomer, sym, hscore, **kw):
    args = Bunch(kw)
    ttot = perf_counter()
    sym = "C%i" % i if isinstance(sym, int) else sym
    args.nresl = len(hscore.hier) if args.nresl is None else args.nresl
    args.out_prefix = sym if args.out_prefix is None else args.out_prefix

    cart_resl, ori_resl = hscore.base.attr.xhresl
    ncart = int(np.ceil(2 * monomer.radius_max() / cart_resl))
    sampler = OriCart1Hier_f4([0.0], [ncart * cart_resl], [ncart], ori_resl)

    evaluator = CyclicEvaluator(monomer, sym, hscore, **args)
    xforms, scores, stats = hier_sample(sampler, evaluator, **args)
    ibest = filter_redundancy(xforms, monomer, scores, **args)
    tdump = dump_cyclic(xforms, monomer, sym, scores, ibest, evaluator, **args)

    ttot = perf_counter() - ttot
    print(f"rate: {int(stats.ntot / ttot):,}/s ttot {ttot:7.3f} tdump {tdump:7.3f}")
    print("stage time:", " ".join([f"{t:8.2f}s" for t, n in stats.neval]))
    print("stage rate:  ", " ".join([f"{int(n/t):7,}/s" for t, n in stats.neval]))

    xforms = xforms[ibest]
    wrpx = args.wts.sub(rpx=1, ncontact=0)
    wnct = args.wts.sub(rpx=0, ncontact=1)
    rpx, lb, ub = evaluator(xforms, args.nresl - 1, wrpx)
    ncontact, *_ = evaluator(xforms, args.nresl - 1, wnct)
    return xr.Dataset(
        dict(
            scores=(["model"], scores[ibest].astype("f4")),
            xforms=(["model", "hrow", "hcol"], xforms),
            rpx=(["model"], rpx.astype("f4")),
            ncontact=(["model"], ncontact.astype("f4")),
            reslb=(["model"], lb),
            resub=(["model"], ub),
        )
    )


class CyclicEvaluator:
    def __init__(self, body, sym, hscore, **kw):
        self.args = Bunch(kw)
        self.body = body
        self.hscore = hscore
        self.symrot = hm.hrot([0, 0, 1], 360 / int(sym[1:]), degrees=True)

    def __call__(self, xforms, iresl, wts={}):
        wts = self.args.wts.sub(wts)
        xeye = np.eye(4, dtype="f4")
        xforms = xforms.reshape(-1, 4, 4)
        body, sfxn = self.body, self.hscore.scorepos
        dclsh, max_trim = self.args.clashdis, self.args.max_trim
        xsym = self.symrot @ xforms

        # check for "flatness"
        ok = np.abs((xforms @ body.pcavecs[0])[:, 2]) <= self.args.max_longaxis_dot_z

        # check clash, or get non-clash range
        if max_trim > 0:
            ptrim = body.intersect_range(body, dclsh, max_trim, xforms[ok], xsym[ok])
            ptrim, trimok = trim_atom_to_res_numbering(ptrim, body.nres, max_trim)
            ok[ok] &= trimok
        else:
            ok[ok] &= body.clash_ok(body, dclsh, xforms[ok], xsym[ok])
            ptrim = [0], [body.nres - 1]

        # score everything that didn't clash
        xok = xforms[ok]
        scores = np.zeros(len(xforms))
        scores[ok] = sfxn(iresl, body, body, xok, xsym[ok], wts, (*ptrim, *ptrim))

        # record ranges used
        plb = np.zeros(len(scores), dtype="i4")
        pub = np.ones(len(scores), dtype="i4") * (body.nres - 1)
        if ptrim:
            plb[ok], pub[ok] = ptrim[0], ptrim[1]

        return scores, plb, pub


def dump_cyclic(xforms, body, sym, scores, ibest, evaluator, **kw):
    args = Bunch(kw)
    t = perf_counter()
    nout = min(10 if args.nout is None else args.nout, len(ibest))
    for iout in range(nout):
        i = ibest[iout]
        body.move_to(xforms[i])
        wrpx, wnct = (args.wts.sub(rpx=1, ncontact=0), args.wts.sub(rpx=0, ncontact=1))
        scr, *lbub = evaluator(xforms[i], args.nresl - 1, wrpx)
        cnt, *lbub = evaluator(xforms[i], args.nresl - 1, wnct)
        fn = args.out_prefix + "_%02i.pdb" % iout
        print(
            f"{fn} score {scores[i]:7.3f} rpx {scr[0]:7.3f} cnt {cnt[0]:4}",
            f"resi {lbub[0][0]}-{lbub[1][0]}",
        )
        dump_pdb_from_bodies(fn, [body], symframes(sym), resbounds=[lbub])
    return perf_counter() - t
import rpxdock as rp, concurrent

def _test_cage_hier_onecomp_notrim(hscore, bodyC3):
   arg = rp.app.defaults()
   arg.wts = rp.Bunch(ncontact=0.3, rpx=1.0)
   arg.beam_size = 2e4
   arg.max_bb_redundancy = 2.0
   arg.max_delta_h = 9999
   arg.nout_debug = 0
   arg.nout_top = 0
   arg.nout_each = 0
   arg.score_only_ss = 'H'
   arg.max_trim = 0
   # arg.debug = True
   arg.executor = concurrent.futures.ThreadPoolExecutor(min(4, arg.ncpu / 2))

   spec = rp.search.DockSpec1CompCage('T3')
   sampler = rp.sampling.hier_axis_sampler(spec.nfold, 0, 100)
   result = rp.search.make_onecomp(bodyC3, spec, hscore, rp.hier_search, sampler, **arg)
   print(result)
   # result.dump_pdbs_top_score(hscore=hscore,
   # **arg.sub(nout_top=10, output_prefix='test_cage_hier_onecomp_notrim'))

   rp.dump(result, 'rpxdock/data/testdata/test_cage_hier_onecomp_notrim.pickle')
   ref = rp.data.get_test_data('test_cage_hier_onecomp_notrim')
   rp.search.assert_results_close(result, ref)

def main():
   hscore = rp.data.small_hscore()
   C3 = rp.data.get_body('C3_1na0-1_1')

   _test_cage_hier_onecomp_notrim(hscore, C3)

if __name__ == '__main__':
   main()
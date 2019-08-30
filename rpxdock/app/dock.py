#! /home/sheffler/.conda/envs/rpxdock/bin/python

import logging, itertools, concurrent, tqdm, rpxdock as rp

def get_rpxdock_args():
   arg = rp.options.get_cli_args()
   if not arg.architecture: raise ValueError("architecure must be specified")
   return arg

def get_spec(arch):
   if arch.startswith('P'):
      spec = rp.search.DockSpec3CompLayer(arch)
   else:
      spec = rp.search.DockSpec2CompCage(arch)
   return spec

def main():
   arg = get_rpxdock_args()
   logging.info(f'weights: {arg.wts}')

   spec = get_spec(arg.architecture)

   sampler = rp.sampling.hier_multi_axis_sampler(spec, **arg)
   logging.info(f'num base samples {sampler.size(0)}')

   hscore = rp.CachedProxy(rp.RpxHier(arg.hscore_files, **arg))

   bodies = [[rp.Body(fn, **arg) for fn in inp] for inp in arg.inputs]
   assert len(bodies) == spec.num_components

   exe = concurrent.futures.ProcessPoolExecutor
   # exe = rp.util.InProcessExecutor
   with exe(arg.ncpu) as pool:
      futures = list()
      for ijob, bod in enumerate(itertools.product(*bodies)):
         futures.append(
            pool.submit(rp.search.make_multicomp, bod, spec, hscore, rp.hier_search, sampler,
                        **arg))
         futures[-1].ijob = ijob
      result = [None] * len(futures)
      for f in tqdm.tqdm(concurrent.futures.as_completed(futures), total=len(futures)):
         result[f.ijob] = f.result()
   result = rp.concat_results(result)

   print(result)
   if arg.dump_pdbs:
      result.dump_pdbs_top_score(hscore=hscore, **arg)
      result.dump_pdbs_top_score_each(hscore=hscore, **arg)
   if not arg.suppress_dump_results:
      rp.util.dump(result, arg.output_prefix + '_Result.pickle')

if __name__ == '__main__':
   main()
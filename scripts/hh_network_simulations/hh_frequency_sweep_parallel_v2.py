"""
hh_frequency_sweep_parallel_v2.py
 
Parallelised version of the HH frequency sweep using multiprocessing.
Each worker gets its own Brian2 cpp_standalone build directory to avoid
file-system conflicts.
 
Changes vs previous version:
  - Raw traces (time_array, rate_exc, rate_inh, Raster_exc, Raster_inh) are
    stripped from each result before accumulation, reducing memory usage ~100x
    and preventing OOM crashes.
  - Partial saves use numbered filenames (e.g. _partial_050.pkl) so a crash
    mid-write never corrupts the last good checkpoint.
 
Usage:
    python -m network_simulations.hh_frequency_sweep_parallel
    python -m network_simulations.hh_frequency_sweep_parallel --workers 4
"""
 
import argparse
import multiprocessing as mp
import os
import pickle
import time
import numpy as np
from itertools import product
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "async_responsiveness" / "data"
DATA_DIR.mkdir(exist_ok=True)
 
 
# ---------------------------------------------------------------------------
# Worker function (must be at module level for pickling on macOS/spawn)
# ---------------------------------------------------------------------------
 
def run_single_sim(job):
    EL_inh, per_value, seed, job_id = job
 
    build_dir = os.path.join("brian2_builds", f"build_{job_id}")
    os.makedirs(build_dir, exist_ok=True)
 
    from hh_network_simulations.hh_impulse_sim_parallel import run_hh_impulse_sim_parallel
 
    freq_value = 1000.0 / per_value
 
    results = run_hh_impulse_sim_parallel(
        NRN_exc        = 'HH_RS_grid',
        NRN_inh        = 'HH_FS_grid',
        NTWK           = 'CONFIG1',
        DT             = 0.1,
        tstop          = 5000,
        ext_drive      = 4.0,
        Qe_ext         = 1.5,
        osc_amplitude  = 1.0,
        osc_period     = per_value,
        osc_onset      = 2500,
        El_exc         = -70,
        El_inh         = EL_inh,
        SEED           = seed,
        save_file      = False,
        show_plots     = False,
        build_dir      = build_dir,
    )
 
    results["EL_inh"]    = EL_inh
    results["El_exc"]    = -70
    results["period"]    = per_value
    results["frequency"] = freq_value
 
    return results
 
 
# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
 
def main(n_workers):
 
    # ---- Sweep parameters --------------------------------------------------
    # EL_inh_range    = np.arange(-80, -45, 5)
    EL_inh_range    = np.array([-80.0, -77.5, -75.0, -72.5, -70.0, -67.5, -65.0, -62.5, -60.0, -57.5, -55.0, -52.5, -50.0]) # new EL_inh_range for supplementary sims
    frequency_range = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                       15, 20, 25, 30, 35, 40, 45, 50,
                       55, 60, 65, 70, 75, 80, 85, 90, 95, 100,
                       120, 140, 160, 180, 200]
    period_range    = 1000.0 / np.array(frequency_range)
    init_seed       = 12
    num_runs        = 10
    tag             = "hh_grid"
    save_interval   = 50
 
    # Keys to strip before accumulating — raw traces not needed across 3740 sims
    STRIP_KEYS = ("time_array", "rate_exc", "rate_inh", "Raster_exc", "Raster_inh")
    # ------------------------------------------------------------------------
 
    # Build job list: (EL_inh, period, seed, unique_job_id)
    jobs = []
    for job_id, (EL_inh, per_value, run_i) in enumerate(
            product(EL_inh_range, period_range, range(num_runs))):
        jobs.append((EL_inh, per_value, init_seed + run_i, job_id))
 
    total = len(jobs)
    print("======================================")
    print("Starting HH impulse frequency sweep (parallel)")
    print(f"  Total simulations : {total}")
    print(f"  Workers           : {n_workers}")
    print(f"  Est. speedup      : ~{n_workers}x")
    print("======================================\n")
 
    impulse_results = []
    completed       = 0

    # # ------------------------------------------------------------------------
    # # Resume from last checkpoint if available (TEMP!!! Lost sim due to crash)
    # # ------------------------------------------------------------------------
    # resume_file = "impulse_results_hh_grid_supp_partial_0750.pkl"

    # if os.path.exists(resume_file):
    #     print(f"\n>> Resuming from {resume_file}")
        
    #     with open(resume_file, "rb") as f:
    #         impulse_results = pickle.load(f)
        
    #     completed = len(impulse_results)
    #     print(f">> Loaded {completed} completed simulations")

    #     # Identify completed jobs via unique identifiers
    #     done_keys = set(
    #         (r["EL_inh"], r["period"], r["frequency"])
    #         for r in impulse_results
    #     )

    #     # Filter remaining jobs
    #     jobs = [
    #         job for job in jobs
    #         if (job[0], job[1], 1000.0 / job[1]) not in done_keys
    #     ]

    #     print(f">> Remaining simulations: {len(jobs)}")

    # else:
    #     impulse_results = []
    #     completed = 0
 
    global_start    = time.time()
    
    with mp.Pool(processes=n_workers) as pool:
        for result in pool.imap_unordered(run_single_sim, jobs):
 
            # Strip raw traces before accumulating
            for key in STRIP_KEYS:
                result.pop(key, None)
 
            impulse_results.append(result)
            completed += 1
 
            elapsed    = time.time() - global_start
            throughput = completed / elapsed
            remaining  = (total - completed) / throughput
            pct        = 100 * completed / total
 
            print(
                f"\n┌─ Progress: {completed}/{total}  ({pct:.1f}%)  |  "
                f"elapsed: {elapsed/60:.1f} min  |  "
                f"est. remaining: {remaining/60:.1f} min  |  "
                f"throughput: {throughput*60:.1f} sims/min\n"
                f"└─ EL_inh={result['EL_inh']} mV | "
                f"freq={result['frequency']:.1f} Hz | "
                f"exc amp={result['amp_exc']:.3f} Hz | "
                f"inh amp={result['amp_inh']:.3f} Hz"
            )
 
            # Numbered partial save — old checkpoints are never overwritten
            if completed % save_interval == 0:
                partial_path = DATA_DIR / f"impulse_results_{tag}_partial_{completed:04d}.pkl"
                with open(partial_path, "wb") as f:
                    pickle.dump(impulse_results, f)
                
                print(f"  >> Checkpoint saved: {partial_path}")
 
    # Final save — sorted to match deterministic ordering of original script
    impulse_results.sort(key=lambda r: (r["EL_inh"], r["frequency"], r["period"]))
 
    final_path = DATA_DIR / f"impulse_results_{tag}_final.pkl"
    with open(final_path, "wb") as f:
        pickle.dump(impulse_results, f)
 
    total_time = time.time() - global_start
    print("\n======================================")
    print("All simulations completed.")
    print(f"Total elapsed time : {total_time/60:.2f} minutes")
    print(f"Results saved to   : {final_path}")
    print("======================================")
 
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--workers", type=int,
        default=max(1, mp.cpu_count() - 1),
        help="Number of parallel workers (default: CPU count - 1)"
    )
    args = parser.parse_args()
    main(args.workers)
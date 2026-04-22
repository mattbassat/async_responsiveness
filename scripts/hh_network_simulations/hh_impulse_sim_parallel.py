from brian2 import *
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse

# HH network modules
from hh_single_cell_models.cell_library import get_neuron_params
from hh_single_cell_models.cell_construct import get_membrane_equation
from hh_synapses_and_connectivity.syn_and_connec_library import get_connectivity_and_synapses_matrix
from hh_synapses_and_connectivity.syn_and_connec_construct import build_up_recurrent_connections_for_2_pop

# # Standalone device
# set_device('cpp_standalone', build_on_run=True)

# Directories
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)


# -------------------------------
# Utility functions
# -------------------------------

def bin_array(array, BIN, time_array):
    dt = time_array[1] - time_array[0]
    N0 = int(BIN/dt)
    N1 = int(len(array)/N0)
    return array[:N0*N1].reshape((N1, N0)).mean(axis=1)


def fit_sinusoid(time_ms, rate_hz, period_ms):
    t = np.asarray(time_ms)
    r = np.asarray(rate_hz)
    omega = 2*np.pi/period_ms
    X = np.column_stack([np.cos(omega*t), np.sin(omega*t), np.ones_like(t)])
    coeffs, _, _, _ = np.linalg.lstsq(X, r, rcond=None)
    A_cos, A_sin, offset = coeffs
    amp = np.sqrt(A_cos**2 + A_sin**2)
    phase = np.arctan2(-A_sin, A_cos)
    return amp, phase, offset


# -------------------------------
# Main simulation
# -------------------------------


def run_hh_impulse_sim_parallel(NRN_exc='HH_RS', NRN_inh='HH_FS', NTWK='CONFIG1',
                       DT=0.1, tstop=5000, ext_drive=4.0, Qe_ext=1.5,
                       osc_amplitude=2.0, osc_period=500, osc_onset=2500,
                       El_exc=None, El_inh=None, SEED=1, show_plots=True, save_file=True,
                       filename='hh_impulse.npy', build_dir=None):

    from brian2 import device
    import shutil
    if build_dir is None:
        build_dir = os.path.join(BASE_DIR, 'output')
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    device.reinit()
    device.activate()
    set_device('cpp_standalone', build_on_run=True, directory=build_dir)
    
    start_scope()
    
    defaultclock.dt = DT * ms
    seed(SEED)
    np.random.seed(SEED)

    # Connectivity
    M = get_connectivity_and_synapses_matrix(NTWK, number=2)
    Ne = int(M[0, 0]['Ntot'] * (1 - M[0, 0]['gei']))
    Ni = int(M[0, 0]['Ntot'] * M[0, 0]['gei'])

    # Neuron params
    exc_params = get_neuron_params(NRN_exc, number=Ne)
    inh_params = get_neuron_params(NRN_inh, number=Ni)

    exc_neurons = get_membrane_equation(exc_params, M[:, 0])
    inh_neurons = get_membrane_equation(inh_params, M[:, 1])

    # Override El if provided (correct mV interpretation)
    exc_neurons.El = (El_exc if El_exc is not None else exc_params['El']) * mV
    inh_neurons.El = (El_inh if El_inh is not None else inh_params['El']) * mV

    # Explicitly define VT
    exc_neurons.VT = exc_params['VT'] * mV
    inh_neurons.VT = inh_params['VT'] * mV

    # Initial conditions
    exc_neurons.V = '(-90+30*rand())*mV'
    inh_neurons.V = '(-90+30*rand())*mV'
    exc_neurons.p = 0.2

    # Recurrent connections
    exc_exc, exc_inh, inh_exc, inh_inh = \
        build_up_recurrent_connections_for_2_pop(
            [exc_neurons, inh_neurons], M)

    # Monitors
    PRe = PopulationRateMonitor(exc_neurons)
    PRi = PopulationRateMonitor(inh_neurons)
    raster_exc = SpikeMonitor(exc_neurons)
    raster_inh = SpikeMonitor(inh_neurons)

    # -------------------------------
    # Oscillatory drive (oscillates ABOUT ext_drive)
    # -------------------------------
    time_array = np.arange(int(tstop/DT)) * DT

    osc_drive = np.zeros_like(time_array)
    mask = time_array >= osc_onset
    osc_drive[mask] = osc_amplitude * np.sin(
        2 * np.pi * (time_array[mask] - osc_onset) / osc_period
    )

    total_drive = ext_drive + osc_drive
    drive_array = TimedArray(total_drive * Hz, dt=DT*ms)

    # Poisson drive
    N_afferent = Ne
    G_aff = PoissonGroup(N_afferent, rates='drive_array(t)')
    Qe_ext = Qe_ext * nS

    S_aff_ex = Synapses(G_aff, exc_neurons, on_pre='Gee_post += Qe_ext')
    S_aff_ex.connect(p=0.05)

    S_aff_in = Synapses(G_aff, inh_neurons, on_pre='Gei_post += Qe_ext')
    S_aff_in.connect(p=0.05)

    # -------------------------------
    # Run
    # -------------------------------
    # set_device('cpp_standalone', build_on_run=True) # Testing
    run(tstop * ms, report='text')

    # # Force clean rebuild — parameters are baked in at compile time
    # device.build(
    #     directory='output',
    #     compile=True,
    #     run=True,
    #     clean=True,      
    #     debug=False
    # )

    # -------------------------------
    # Extract data (MATCH DEMO FORMAT)
    # -------------------------------

    rate_exc = np.array(PRe.rate / Hz)
    rate_inh = np.array(PRi.rate / Hz)

    Raster_exc = [
        np.array(raster_exc.t / ms),
        np.array(raster_exc.i)
    ]

    Raster_inh = [
        np.array(raster_inh.t / ms),
        np.array(raster_inh.i + Ne)  # critical shift
    ]

    # Save in demo-compatible structure

    if save_file:
        filename = os.path.join(DATA_DIR, filename)
        np.save(filename,
                np.array([time_array,
                        total_drive,
                        rate_exc,
                        rate_inh,
                        Raster_exc,
                        Raster_inh],
                        dtype=object))

    # -------------------------------
    # Bin rates
    # -------------------------------
    BIN = 1  # ms

    time_monitor = np.asarray(PRe.t / ms)

    rate_exc_binned = bin_array(rate_exc, BIN, time_monitor)
    rate_inh_binned = bin_array(rate_inh, BIN, time_monitor)
    time_binned = bin_array(time_monitor, BIN, time_monitor)

    # -------------------------------
    # Baseline firing rates
    # (after 500 ms transient and before stimulus onset)
    # -------------------------------

    transient_ms = 500

    baseline_mask = (time_binned >= transient_ms) & (time_binned < osc_onset)

    average_exc_rate = np.mean(rate_exc_binned[baseline_mask])
    average_inh_rate = np.mean(rate_inh_binned[baseline_mask])

    print("\n--- Baseline firing rates ---")
    print(f"Excitatory: {average_exc_rate:.3f} Hz")
    print(f"Inhibitory: {average_inh_rate:.3f} Hz")
    print("-----------------------------\n")

    # -------------------------------
    # Sinusoid fitting (post-onset only)
    # -------------------------------

    # Exclude transient (initial 3 s)
    transient_cutoff = 3000  # ms (fit based on last two seconds)

    mask = time_binned >= 3000

    amp_exc, phase_exc, offset_exc = fit_sinusoid(
        time_binned[mask], rate_exc_binned[mask], osc_period)

    amp_inh, phase_inh, offset_inh = fit_sinusoid(
        time_binned[mask], rate_inh_binned[mask], osc_period)
    
    # --- Construct fitted curves ------------------------------------------------
    omega = 2 * np.pi / osc_period
    fitted_exc = offset_exc + amp_exc * np.cos(omega * time_binned[mask] + phase_exc)
    fitted_inh = offset_inh + amp_inh * np.cos(omega * time_binned[mask] + phase_inh)

    # -------------------------------
    # Plotting
    # -------------------------------

    if show_plots:

        plt.figure(figsize=(10, 4))
        plt.plot(time_binned, rate_exc_binned, color='green', label='Exc')
        plt.plot(time_binned, rate_inh_binned, color='red', label='Inh')
        # Add fitted sinusoids
        plt.plot(time_binned[mask], fitted_exc, color='darkgreen', linestyle='-', linewidth=2,
                 label=f'Exc Fit')
        plt.plot(time_binned[mask], fitted_inh, color='darkred', linestyle='-', linewidth=2,
                 label=f'Inh Fit')

        plt.xlabel('Time (ms)')
        plt.ylabel('Firing Rate (Hz)')
        plt.title('Population Firing Rates with Sinusoidal Fits')
        plt.plot(time_array, total_drive, '--', label='Input')
        plt.xlabel('Time (ms)')
        plt.ylabel('Firing Rate (Hz)')
        plt.legend()
        plt.tight_layout()
        # plt.show()

        plt.figure(figsize=(10, 4))
        plt.plot(Raster_exc[0], Raster_exc[1], '.g', markersize=1)
        plt.plot(Raster_inh[0], Raster_inh[1], '.r', markersize=1)
        plt.xlabel('Time (ms)')
        plt.ylabel('Neuron index')
        plt.title('Raster plot')
        plt.tight_layout()
        plt.show()


    return {
        "time_array": time_array, 
        "rate_exc": rate_exc, 
        "rate_inh": rate_inh,
        "Raster_exc": Raster_exc, 
        "Raster_inh": Raster_inh,
        "amp_exc": amp_exc, 
        "phase_exc": phase_exc, 
        "offset_exc": offset_exc,
        "amp_inh": amp_inh, 
        "phase_inh": phase_inh, 
        "offset_inh": offset_inh,
        "average_exc_rate": average_exc_rate,
        "average_inh_rate": average_inh_rate
    }

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="HH impulse simulation with sinusoidal drive")

    parser.add_argument("--tstop", type=float, default=5000)
    parser.add_argument("--DT", type=float, default=0.1)
    parser.add_argument("--ext_drive", type=float, default=4.0)
    parser.add_argument("--Qe_ext", type=float, default=1.5)
    parser.add_argument("--osc_amp", type=float, default=2.0)
    parser.add_argument("--osc_period", type=float, default=500)
    parser.add_argument("--osc_onset", type=float, default=2500)
    parser.add_argument("--El_exc", type=float, default=None)
    parser.add_argument("--El_inh", type=float, default=None)
    parser.add_argument("--SEED", type=int, default=12)
    parser.add_argument("--file", type=str, default='hh_impulse.npy')
    parser.add_argument("--NRN_exc", type=str, default='HH_RS')
    parser.add_argument("--NRN_inh", type=str, default='HH_FS')
    parser.add_argument("--NTWK", type=str, default='CONFIG1')

    args = parser.parse_args()

    run_hh_impulse_sim_parallel(
        NRN_exc=args.NRN_exc,
        NRN_inh=args.NRN_inh,
        NTWK=args.NTWK,
        DT=args.DT,
        tstop=args.tstop,
        ext_drive=args.ext_drive,
        Qe_ext=args.Qe_ext,
        osc_amplitude=args.osc_amp,
        osc_period=args.osc_period,
        osc_onset=args.osc_onset,
        El_exc=args.El_exc,
        El_inh=args.El_inh,
        SEED=args.SEED,
        save_file=True,
        show_plots=True,
        filename=args.file
    )

from gpaw.lcaotddft import LCAOTDDFT
from gpaw.lcaotddft.frequencydensitymatrix import FrequencyDensityMatrix
from gpaw.tddft.folding import frequencies
import numpy as np
from matplotlib import pyplot as plt
from gpaw import GPAW
from gpaw.tddft.units import au_to_eV
from gpaw.lcaotddft.ksdecomposition import KohnShamDecomposition
from gpaw.lcaotddft.densitymatrix import DensityMatrix
from gpaw.lcaotddft.frequencydensitymatrix import FrequencyDensityMatrix
from gpaw.lcaotddft.tcm import TCMPlotter

# Read the ground-state file
td_calc = LCAOTDDFT('../../gpaw/TaskTypes.GROUND_STATE/gs.gpw', txt=None)

frequency_list = [3.75, 4.26]

# Attach analysis tools
dmat = DensityMatrix(td_calc)
freqs = frequencies(frequency_list, 'Gauss', 0.1)
fdm = FrequencyDensityMatrix(td_calc, dmat, frequencies=freqs)

# Replay the propagation
td_calc.replay(name='../../gpaw/TaskTypes.RT_TDDFT/wf.ulm', update='none')

# Store the density matrix
fdm.write('fdm.ulm')


# Calculate ground state with full unoccupied space
calc = GPAW('../../gpaw/TaskTypes.GROUND_STATE/gs.gpw', txt=None).fixed_density(nbands='nao', txt='unocc.out')
calc.write('unocc.gpw', mode='all')

# Construct KS electron-hole basis
ksd = KohnShamDecomposition(calc)
ksd.initialize(calc)
ksd.write('ksd.ulm')

# Load the objects
calc = GPAW('unocc.gpw', txt=None)
ksd = KohnShamDecomposition(calc, 'ksd.ulm')
dmat = DensityMatrix(calc)
fdm = FrequencyDensityMatrix(calc, dmat, 'fdm.ulm')

plt.figure(figsize=(8, 8))


def do(w):
    # Select the frequency and the density matrix
    rho_uMM = fdm.FReDrho_wuMM[w]
    freq = fdm.freq_w[w]
    frequency = freq.freq * au_to_eV
    print(f'Frequency: {frequency:.2f} eV')
    print(f'Folding: {freq.folding}')

    # Transform the LCAO density matrix to KS basis
    rho_up = ksd.transform(rho_uMM)

    # Photoabsorption decomposition
    dmrho_vp = ksd.get_dipole_moment_contributions(rho_up)
    weight_p = 2 * freq.freq / np.pi * dmrho_vp[0].imag / au_to_eV * 1e5
    print(f'Total absorption: {np.sum(weight_p):.2f} eV^-1')

    # Print contributions as a table
    table = ksd.get_contributions_table(weight_p, minweight=0.1)
    print(table)
    with open(f'table_{frequency:.2f}.txt', 'w') as f:
        f.write(f'Frequency: {frequency:.2f} eV\n')
        f.write(f'Folding: {freq.folding}\n')
        f.write(f'Total absorption: {np.sum(weight_p):.2f} eV^-1\n')
        f.write(table)

    # Plot the decomposition as a TCM
    de = 0.01
    energy_o = np.arange(-5.00, 0.1 + 1e-6, de)
    energy_u = np.arange(-0.1, 5.00 + 1e-6, de)
    plt.clf()
    plotter = TCMPlotter(ksd, energy_o, energy_u, sigma=0.1)
    plotter.plot_TCM(weight_p)
    plotter.plot_DOS(fill={'color': '0.8'}, line={'color': 'k'})
    plotter.plot_TCM_diagonal(freq.freq * au_to_eV, color='k')
    plotter.set_title(f'Photoabsorption TCM at {frequency:.2f} eV')

    # Check that TCM integrates to correct absorption
    tcm_ou = ksd.get_TCM(weight_p, ksd.get_eig_n()[0],
                         energy_o, energy_u, sigma=0.1)
    print(f'TCM absorption: {np.sum(tcm_ou) * de ** 2:.2f} eV^-1')

    # Save the plot
    plt.savefig(f'tcm_{frequency:.2f}.png')

def run(frequency_list):
    for i, item in enumerate(frequency_list):
        do(i)
run(frequency_list)

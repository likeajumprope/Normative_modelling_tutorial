"""Plotting helpers for the normative modelling tutorial.

These functions only draw figures; all the calculations happen in the notebook.
"""

import numpy as np
import matplotlib.pyplot as plt


def plot_dataset(train, sites):
    # Four panels: (1) age coverage of each site, (2) a region with symmetric noise,
    # (3) a region with strongly skewed noise, (4) another skewed region. Colours = sites.
    fig, axes = plt.subplots(1, 4, figsize=(15, 4))
    for site in sites:
        d = train[train["site"] == site]
        axes[0].hist(d["age"], bins=30, alpha=0.6, label=site)
        axes[1].scatter(d["age"], d["precuneus"], s=4, alpha=0.5, label=site)
        axes[2].scatter(d["age"], d["entorhinal"], s=4, alpha=0.5, label=site)
        axes[3].scatter(d["age"], d["cingulate"], s=4, alpha=0.5, label=site)

    axes[0].set_title("Age distribution per site")
    axes[1].set_title("precuneus (symmetric noise)")
    axes[2].set_title("entorhinal (skewed noise)")
    axes[3].set_title("cingulate")
    for ax in axes:
        ax.set_xlabel("age")
    axes[1].set_ylabel("thickness (mm)")
    axes[0].legend()
    plt.tight_layout()
    plt.show()


def plot_patient_heatmap(Z_sorted, rois):
    # Heatmap of patients' z-scores: rows = regions, columns = patients (already sorted).
    # Red = thinner than expected, blue = thicker.
    plt.figure(figsize=(8, 4))
    plt.imshow(Z_sorted.T, aspect="auto", cmap="RdBu", vmin=-5, vmax=5, interpolation="nearest")
    plt.colorbar(label="z")
    plt.yticks(range(len(rois)), rois)
    plt.xlabel("patient (sorted)")
    plt.title("(a) Patient z-scores")
    plt.show()


def plot_extreme_counts(ext_ctrl, ext_pat):
    # Histogram: in how many regions is each person extreme? Controls vs. patients.
    n_regions = ext_pat.shape[1]
    bins = np.arange(-0.5, n_regions + 0.5)        # one bar per whole number: 0, 1, 2, ...

    plt.figure(figsize=(6, 4))
    plt.hist(ext_ctrl.sum(axis=1), bins=bins, density=True, alpha=0.6, label="controls (test)")
    plt.hist(ext_pat.sum(axis=1), bins=bins, density=True, alpha=0.6, label="patients")
    plt.xlabel("number of regions with an extreme deviation")
    plt.ylabel("proportion of people")
    plt.title("(b) Extreme deviations per person")
    plt.legend()
    plt.show()


def plot_extreme_by_region(ext_ctrl, ext_pat, rois):
    # Bar chart: in each region, what % of controls and of patients is extreme?
    x = np.arange(len(rois))                        # one position per region

    plt.figure(figsize=(8, 4))
    plt.bar(x - 0.2, 100 * ext_ctrl.mean(axis=0), width=0.4, label="controls")
    plt.bar(x + 0.2, 100 * ext_pat.mean(axis=0), width=0.4, label="patients")
    plt.xticks(x, rois, rotation=45, ha="right")
    plt.ylabel("% with an extreme deviation")
    plt.title("(c) Where are the deviations?")
    plt.legend()
    plt.show()

"""Simulated multi-site cortical thickness data for the normative modelling tutorial.

The notebook only imports the results:
    from simulate_data import ROIS, SITES, N_ROI, n_pat, train, test, patients, truth

What is built in:
- a non-linear lifespan trajectory (early thinning, then slower decline),
- heteroscedasticity: the variance grows with age,
- site effects on both location and scale,
- skewed noise in some regions,
- heterogeneous patients: each has abnormal thinning in a different 1-3 regions (and some have none).
"""

import numpy as np
import pandas as pd
from scipy import stats
from sklearn.model_selection import train_test_split

# A single seeded random generator makes every run produce exactly the same
# simulated data, so everyone in the room sees the same numbers.
rng = np.random.default_rng(2026)

# ===========================================================================
# 1. Study design: regions, sites and how many subjects each site contributes
# ===========================================================================
ROIS = ["frontal_pole", "precentral", "sup_temporal", "insula",
        "precuneus", "lat_occipital", "entorhinal", "cingulate"]
SITES = ["site_A", "site_B", "site_C", "site_D"]

# Each site recruits a different age range -> site and age are CONFOUNDED,
# which is realistic (e.g. a paediatric cohort vs. an ageing cohort).
SITE_AGE = {"site_A": (6, 25), "site_B": (18, 60), "site_C": (40, 88), "site_D": (6, 88)}
SITE_N = {"site_A": 700, "site_B": 800, "site_C": 700, "site_D": 800}
N_ROI = len(ROIS)

# ===========================================================================
# 2. Ground-truth parameters (the "true" normative model we try to recover)
# ===========================================================================
# One row per region. Rows = regions, columns = parameters of the true curve.
P = pd.DataFrame({
    "base":    rng.uniform(2.4, 3.0, N_ROI),    # thickness level (mm) in young adulthood
    "growth":  rng.uniform(0.15, 0.35, N_ROI),  # extra thickness in childhood that is lost quickly
    "decline": rng.uniform(0.35, 0.65, N_ROI),  # total thinning across the adult lifespan
    "sd0":     rng.uniform(0.08, 0.12, N_ROI),  # between-subject SD at age 6
    "skew_a":  [0, 1, 2, 3, 0, 4, 8, 6],        # noise skewness: 0 = symmetric, larger = long upper tail
}, index=ROIS)

# Scanner/site effects: each site shifts the mean (offset) and stretches the
# spread (scale) of every region differently. Shape: (n_sites, n_regions).
site_offset = rng.normal(0, 0.06, (len(SITES), N_ROI))
site_scale = rng.uniform(0.85, 1.25, (len(SITES), N_ROI))


def true_mu(age, p):
    # True mean trajectory: fast childhood thinning (exponential term)
    # plus accelerating adult decline (power term). Deliberately NON-linear.
    return p.base + p.growth * np.exp(-(age - 6) / 5) - p.decline * ((age - 6) / 80) ** 1.5


def true_sd(age, p):
    # True SD grows linearly with age (up to +80% by age 86) -> HETEROSCEDASTIC data.
    return p.sd0 * (1 + 0.8 * (age - 6) / 80)


def std_skewnorm(a, size):
    # Draw skew-normal noise and rescale it to mean 0, SD 1, so that the
    # skewness parameter `a` changes only the SHAPE of the distribution,
    # not its location or spread.
    delta = a / np.sqrt(1 + a ** 2)
    m = delta * np.sqrt(2 / np.pi)                  # theoretical mean of a skew-normal
    return (stats.skewnorm.rvs(a, size=size, random_state=rng) - m) / np.sqrt(1 - m ** 2)


def simulate(age, sex, site_idx):
    # Returns an (n_subjects x n_regions) matrix of cortical thickness values:
    #   y = true mean(age) + sex effect + site offset  +  true SD(age) * site scale * noise
    Y = np.zeros((len(age), N_ROI))
    for j, roi in enumerate(ROIS):
        p = P.loc[roi]
        mu = true_mu(age, p) + 0.03 * sex + site_offset[site_idx, j]
        sd = true_sd(age, p) * site_scale[site_idx, j]
        Y[:, j] = mu + sd * std_skewnorm(p.skew_a, len(age))
    return Y


# ===========================================================================
# 3. Healthy controls (the reference cohort for the normative model)
# ===========================================================================
rows = []
for s_idx, s in enumerate(SITES):
    n = SITE_N[s]
    age = rng.uniform(*SITE_AGE[s], n)              # ages uniformly spread within the site's range
    sex = rng.integers(0, 2, n)                     # 0/1 coding
    rows.append(pd.DataFrame({"age": age, "sex": sex, "site": s, "site_idx": s_idx}))
controls = pd.concat(rows, ignore_index=True)
controls[ROIS] = simulate(controls.age.values, controls.sex.values, controls.site_idx.values)
controls["dx"] = "control"

# ===========================================================================
# 4. Patients: same generative model PLUS heterogeneous regional thinning
# ===========================================================================
n_pat = 240
pat_site = rng.choice([1, 2, 3], n_pat)            # patients come from the adult sites (B, C, D)
pat_age = np.array([rng.uniform(max(18, SITE_AGE[SITES[i]][0]), SITE_AGE[SITES[i]][1]) for i in pat_site])
patients = pd.DataFrame({"age": pat_age, "sex": rng.integers(0, 2, n_pat),
                         "site": [SITES[i] for i in pat_site], "site_idx": pat_site})
patients[ROIS] = simulate(patients.age.values, patients.sex.values, patients.site_idx.values)

# `truth[i, j]` records whether patient i really has an abnormality in region j.
# The notebook uses it in Section 5 to check how well deviation scores recover the truth
# (a luxury we never have with real data).
truth = np.zeros((n_pat, N_ROI), dtype=bool)
roi_prob = np.array([1, 1, 1, 2, 1, 1, 2.5, 1])   # insula & entorhinal are affected more often
roi_prob /= roi_prob.sum()
for i in range(n_pat):
    if rng.random() < 0.35:                         # 35% of patients have NO abnormality at all
        continue
    k = rng.choice([1, 2, 3], p=[0.6, 0.3, 0.1])    # the rest have 1-3 affected regions...
    for j in rng.choice(N_ROI, k, replace=False, p=roi_prob):   # ...and WHICH regions varies per patient
        # Thin the region by 3-4.5 SDs of the healthy variation for that person's age and site
        sd = true_sd(patients.age[i], P.iloc[j]) * site_scale[patients.site_idx[i], j]
        patients.iloc[i, patients.columns.get_loc(ROIS[j])] -= rng.uniform(3, 4.5) * sd
        truth[i, j] = True
patients["dx"] = "patient"

# ===========================================================================
# 5. Split controls into training (fit the model) and test (evaluate it)
# ===========================================================================
# Stratifying by site guarantees every site is represented in both sets.
# Evaluating on held-out controls is essential: training-set z-scores look
# better calibrated than they really are.
train, test = train_test_split(controls, test_size=0.3, stratify=controls.site, random_state=0)
train, test = train.reset_index(drop=True), test.reset_index(drop=True)

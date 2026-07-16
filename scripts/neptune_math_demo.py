#!/usr/bin/env python3
"""The Neptune arc's mathematics, run (engine/perturbation.py).

What neptune-discovery.ttl narrates, computed:

  1. THE ANOMALY -- Uranus integrated 1750-1850 with and without Neptune;
     the longitude residuals grow to ~+86 arcsec, peaking at the computed
     1821.6 conjunction: the year Bouvard published the tables that were
     about to fail.
  2. THE CIRCLE REFUSED -- a circular perturber at the Titius-Bode radius
     fits the residual curve only by sitting tens of degrees behind
     Neptune's true position: the residuals themselves reject the naive
     ex:BodesLaw orbit.
  3. THE DIRECTION RECOVERED -- give the fit Le Verrier's actual freedom
     (Bode-neighborhood axis, eccentricity, free perihelion: his published
     a=36.15, e=0.1076 is exactly this shape) and the discovery-night
     direction lands, on an orbit still ~25% too large. Wrong ORBIT, right
     DIRECTION -- the fixture's sentence, as a number.

Takes ~1 minute: a few hundred pure-Python RK4 integrations.
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from engine import perturbation as pt


def main() -> int:
    t0 = time.time()
    print("=" * 72)
    print("1. THE ANOMALY -- Uranus with and without Neptune (1750-1850)")
    print("=" * 72)
    res = pt.uranus_residuals()
    for yr in (1770, 1790, 1810, 1821, 1830, 1840, 1846):
        v = next(v for t, v in res if abs(t - yr) < 0.51)
        bar = "#" * min(60, int(abs(v) / 2))
        print(f"  {yr}:  {v:+8.1f} arcsec  {bar}")
    peak_t, peak_v = max(res, key=lambda tv: abs(tv[1]))
    conj = pt.conjunction_epoch()
    print(f"\n  peak residual: {peak_v:+.1f} arcsec at {peak_t:.0f}")
    print(f"  computed Uranus-Neptune conjunction: {conj:.1f}")
    print(f"  (Bouvard's tables: 1821. They never had a chance.)")

    print()
    print("=" * 72)
    print("2./3. LE VERRIER'S MOVE -- the inverse fit, two stages")
    print("=" * 72)
    fit = pt.leverrier_fit()
    truth = fit["neptune_longitude_1846_deg"]
    c, l = fit["circular"], fit["leverrier"]
    print(f"  Neptune's true heliocentric longitude, 1846-09-23: {truth:.1f} deg")
    print()
    print(f"  stage 1 -- circular at Bode radius {pt.BODE_RADIUS_AU} AU:")
    print(f"    fit rms {c['fit_rms_arcsec']:.1f} arcsec;  predicted "
          f"{c['predicted_longitude_1846_deg']:.1f} deg;  error {c['error_deg']:.1f} deg")
    print(f"    the residuals REFUSE the circle: pinned behind, at "
          f"{c['fit_rms_arcsec'] / l['fit_rms_arcsec']:.1f}x the eccentric rms")
    print()
    e2 = l["elements"]
    print(f"  stage 2 -- Le Verrier's freedom "
          f"(a={e2['a']}, e={e2['e']}, varpi={e2['varpi']:.0f}):")
    print(f"    fit rms {l['fit_rms_arcsec']:.1f} arcsec;  predicted "
          f"{l['predicted_longitude_1846_deg']:.1f} deg;  error {l['error_deg']:.1f} deg")
    print(f"    (his 33-equation fit reached ~1 deg; this coarse grid claims")
    print(f"     only the ZONE -- and the zone is what a sweep search covers)")

    print()
    print("=" * 72)
    out = {
        "anomaly_material": 30.0 <= abs(peak_v) <= 5000.0,
        "conjunction_near_1821": 1815.0 <= conj <= 1830.0,
        "circle_refused": c["error_deg"] >= 30.0
                          and c["fit_rms_arcsec"] > 2.0 * l["fit_rms_arcsec"],
        "direction_recovered": l["error_deg"] <= 25.0,
    }
    for k, v in out.items():
        print(f"  [{'OK ' if v else 'FAIL'}] {k}")
    print(f"  ({time.time() - t0:.0f}s)")
    print("=" * 72)
    return 0 if all(out.values()) else 1


if __name__ == "__main__":
    sys.exit(main())

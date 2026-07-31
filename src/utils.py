import numpy as np
import pyfar as pf
from across import ERA


REDUCED_ORDER = 70


def dB(x, ref=None):
    magnitude = np.abs(np.asarray(x))
    if not np.issubdtype(magnitude.dtype, np.inexact):
        magnitude = magnitude.astype(float)
    if ref is not None:
        magnitude = magnitude / np.abs(ref)
    return 20 * np.log10(np.maximum(magnitude, np.finfo(magnitude.dtype).eps))


def delay_shifts(impulse_response, delay_removal=None):
    """Return delays extracted before ERA for the requested policy."""
    if delay_removal is None:
        return 0

    starts = pf.dsp.find_impulse_response_start(impulse_response)
    if delay_removal == "common":
        return starts.min()
    if delay_removal == "individual":
        return starts
    raise ValueError(f"Unknown delay-removal strategy: {delay_removal}")


def prepare_impulse_response(impulse_response, delay_removal=None):
    """Remove delays and normalize HRIR energy to the number of channels."""
    if delay_removal is not None:
        impulse_response = pf.dsp.fractional_time_shift(
            impulse_response, -delay_shifts(impulse_response, delay_removal)
        )
    scale = np.sqrt(np.prod(impulse_response.cshape)) / np.linalg.norm(impulse_response.time)
    return impulse_response * scale


def make_era(impulse_response, delay_removal=None):
    """Return ERA plus its non-direct Markov-parameter and virtual-input counts."""
    era = ERA(prepare_impulse_response(impulse_response, delay_removal), pad_zero=True)
    s, p, m = era.reductor.data.shape
    retained_samples = s - int(np.min(delay_shifts(impulse_response, delay_removal)))
    n_virtual = min(p * retained_samples, m)
    return era, s, n_virtual


def restore_delays(impulse_response, reference, delay_removal=None):
    """Restore delays removed from ``reference`` after ERA reconstruction."""
    if delay_removal is None:
        return impulse_response
    return pf.dsp.fractional_time_shift(
        impulse_response, delay_shifts(reference, delay_removal)
    )

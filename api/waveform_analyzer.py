import numpy as np
from scipy.signal import find_peaks

class WaveformAnalyzer:
    def __init__(self, time, amplitude):
        self.time = np.array(time)
        self.amplitude = np.array(amplitude)
        self.peaks = None
        self.troughs = None
        self._find_extrema()
    
    def _find_extrema(self, prominence_factor=0.05):
        max_amp = np.max(np.abs(self.amplitude))
        prominence = max_amp * prominence_factor
        
        self.peaks, _ = find_peaks(self.amplitude, prominence=prominence)
        self.troughs, _ = find_peaks(-self.amplitude, prominence=prominence)
    
    def get_rise_fall_times(self, threshold_percent=10):
        results = []
        cycle_count = 0
        
        for i in range(len(self.peaks) - 1):
            peak_idx = self.peaks[i]
            next_peak_idx = self.peaks[i + 1]
            
            troughs_between = [t for t in self.troughs if peak_idx < t < next_peak_idx]
            
            if not troughs_between:
                continue
            
            trough_idx = troughs_between[0]
            cycle_count += 1
            
            peak_amp = self.amplitude[peak_idx]
            trough_amp = self.amplitude[trough_idx]
            peak_time = self.time[peak_idx]
            trough_time = self.time[trough_idx]
            
            rise_low = trough_amp + (peak_amp - trough_amp) * (threshold_percent / 100)
            rise_high = trough_amp + (peak_amp - trough_amp) * ((100 - threshold_percent) / 100)
            
            rise_indices = np.where(
    (self.time >= trough_time) &
    (self.time <= self.time[next_peak_idx])
)[0]
            
            rise_cross_low = None
            rise_cross_high = None
            
            for idx in rise_indices:
                if self.amplitude[idx] >= rise_low and rise_cross_low is None:
                    rise_cross_low = idx
                if self.amplitude[idx] >= rise_high:
                    rise_cross_high = idx
            
            rise_time = (
    self.time[rise_cross_high] - self.time[rise_cross_low]
) if (
    rise_cross_high is not None and rise_cross_low is not None
) else None
            fall_high = peak_amp - (peak_amp - trough_amp) * (threshold_percent / 100)
            fall_low = peak_amp - (peak_amp - trough_amp) * ((100 - threshold_percent) / 100)
            
            fall_indices = np.where(
    (self.time >= peak_time) &
    (self.time <= self.time[next_peak_idx])
)[0]
            
            fall_cross_high = None
            fall_cross_low = None
            
            for idx in fall_indices:
                if self.amplitude[idx] <= fall_high and fall_cross_high is None:
                    fall_cross_high = idx
                if self.amplitude[idx] <= fall_low and fall_cross_low is None:
                    fall_cross_low = idx
            
            fall_time = (
    self.time[fall_cross_low] - self.time[fall_cross_high]
) if (
    fall_cross_low is not None and fall_cross_high is not None
) else None
            
            results.append({
                'cycle_number': int(cycle_count),
                'peak_time': float(peak_time),
                'peak_amplitude': float(peak_amp),
                'trough_time': float(trough_time),
                'trough_amplitude': float(trough_amp),
                'rise_time': float(rise_time) if rise_time is not None else None,
                'fall_time': float(fall_time) if fall_time is not None else None
            })
        
        return results
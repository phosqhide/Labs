import plotly.graph_objects as go
import numpy as np


a0, f0, phi0 = 5, 3, 0
noise_mean0, noise_covariance0 = 0, 0.2
time = np.linspace(0, 1, 1000)

np.random.seed(42)
base_noise = np.random.normal(noise_mean0, noise_covariance0, len(time))

def harmonic_with_noise(amplitude, frequency, phase, noise_mean, noise_covariance, show_noise, time, noise=None):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * time + phase)
    if show_noise and noise is not None:
        noisy = harmonic + noise
    else:
        noisy = harmonic
    return harmonic, noisy

def custom_filter(signal, window_size=5):
    filtered = np.copy(signal)
    for i in range(window_size, len(signal) - window_size):
        filtered[i] = np.mean(signal[i - window_size:i + window_size + 1])
    return filtered

harmonic, noisy_signal = harmonic_with_noise(a0, f0, phi0, noise_mean0, noise_covariance0, True, time, base_noise)
filtered_signal = custom_filter(noisy_signal)

fig = go.Figure()

fig.add_trace(go.Scatter(x=time, y=harmonic, name="Harmonic", line=dict(color="blue", width=2), visible=True))
fig.add_trace(go.Scatter(x=time, y=noisy_signal, name="With Noise", line=dict(color="red", width=2), visible=False))
fig.add_trace(go.Scatter(x=time, y=filtered_signal, name="Filtered", line=dict(color="green", width=2, dash='dot'), visible=False))

fig.update_layout(
    updatemenus=[
        dict(
            type="buttons",
            direction="down",
            buttons=[
                dict(label="Показати шум", method="restyle",
                     args=[{"visible": [True, True, False]}]),
                dict(label="Показати фільтр", method="restyle",
                     args=[{"visible": [True, True, True]}]),
                dict(label="Скинути", method="restyle",
                     args=[{"visible": [True, False, False]}])
            ],
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.2,
            yanchor="top"
        )
    ]
)

sliders = []

amp_steps = []
for amp in np.linspace(1, 10, 10):
    h, n = harmonic_with_noise(amp, f0, phi0, noise_mean0, noise_covariance0, True, time, base_noise)
    f = custom_filter(n)
    amp_steps.append(dict(method="restyle", args=[{"y": [h, n, f]}], label=f"{amp:.1f}"))
sliders.append(dict(active=4, currentvalue={"prefix": "Amplitude: "}, pad={"t": 50}, steps=amp_steps))

freq_steps = []
for freq in np.linspace(1, 10, 10):
    h, n = harmonic_with_noise(a0, freq, phi0, noise_mean0, noise_covariance0, True, time, base_noise)
    f = custom_filter(n)
    freq_steps.append(dict(method="restyle", args=[{"y": [h, n, f]}], label=f"{freq:.1f}"))
sliders.append(dict(active=2, currentvalue={"prefix": "Frequency: "}, pad={"t": 150}, steps=freq_steps))

phase_steps = []
for phase in np.linspace(0, 2 * np.pi, 10):
    h, n = harmonic_with_noise(a0, f0, phase, noise_mean0, noise_covariance0, True, time, base_noise)
    f = custom_filter(n)
    phase_steps.append(dict(method="restyle", args=[{"y": [h, n, f]}], label=f"{phase:.2f}"))
sliders.append(dict(active=0, currentvalue={"prefix": "Phase: "}, pad={"t": 250}, steps=phase_steps))

mean_steps = []
for mean in np.linspace(-1, 1, 10):
    noise = np.random.normal(mean, noise_covariance0, len(time))
    h, n = harmonic_with_noise(a0, f0, phi0, mean, noise_covariance0, True, time, noise)
    f = custom_filter(n)
    mean_steps.append(dict(method="restyle", args=[{"y": [h, n, f]}], label=f"{mean:.2f}"))
sliders.append(dict(active=5, currentvalue={"prefix": "Noise Mean: "}, pad={"t": 350}, steps=mean_steps))

cov_steps = []
for cov in np.linspace(0.01, 1, 10):
    noise = np.random.normal(noise_mean0, cov, len(time))
    h, n = harmonic_with_noise(a0, f0, phi0, noise_mean0, cov, True, time, noise)
    f = custom_filter(n)
    cov_steps.append(dict(method="restyle", args=[{"y": [h, n, f]}], label=f"{cov:.2f}"))
sliders.append(dict(active=2, currentvalue={"prefix": "Noise Covariance: "}, pad={"t": 450}, steps=cov_steps))

fig.update_layout(
    height=1800,
    sliders=sliders
)

fig.show()

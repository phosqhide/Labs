import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, CheckButtons
from scipy import signal


a0 = 5
f0 = 3
phi0 = 0
noise_mean0 = 0
noise_std0 = 0.2
show_noise0 = False
filter_noise0 = False


t = np.linspace(0, 1, 1000)


def compute_signal(amplitude, frequency, phase, noise_mean, noise_std, show_noise, filter_noise):
    clean_signal = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, noise_std, len(t))
        noise_signal = noise + clean_signal
        if filter_noise:
            b, a = signal.iirfilter(10, 0.1, btype='low')  
            noise_signal = signal.filtfilt(b, a, noise_signal)
        return noise_signal
    else:
        return clean_signal


fig, ax = plt.subplots()
fig.subplots_adjust(left=0.25, bottom=0.45)
initinal_signal = compute_signal(a0, f0, phi0, noise_mean0, noise_std0, show_noise0, filter_noise0)
line_noise, = ax.plot(t, initinal_signal, lw=2, color='blue')
line_clean, = ax.plot(t, compute_signal(a0, f0, phi0, 0, 0, False, False), lw=2, color='green')

ax.set_title("Гармонічний сигнал з шумом")


ax_amp = fig.add_axes([0.25, 0.35, 0.65, 0.03])
s_amp = Slider(ax_amp, "Amplitude", 0.1, 10.0, valinit=a0)

ax_freq = fig.add_axes([0.25, 0.30, 0.65, 0.03])
s_freq = Slider(ax_freq, "Frequency", 0.1, 10.0, valinit=f0)

ax_phase = fig.add_axes([0.25, 0.25, 0.65, 0.03])
s_phase = Slider(ax_phase, "Phase", 0, 2*np.pi, valinit=phi0)

ax_mean = fig.add_axes([0.25, 0.20, 0.65, 0.03])
s_mean = Slider(ax_mean, "Noise Mean", -1.0, 1.0, valinit=noise_mean0)

ax_std = fig.add_axes([0.25, 0.15, 0.65, 0.03])
s_std = Slider(ax_std, "Noise Std", 0.0, 1.0, valinit=noise_std0)


ax_check = fig.add_axes([0.025, 0.6, 0.15, 0.15])
check_noise = CheckButtons(ax_check, ["Show noise"], [show_noise0])

ax_filter = fig.add_axes([0.025, 0.5, 0.15, 0.15])
check_filter = CheckButtons(ax_filter, ["Filter noise"], [filter_noise0])


ax_button = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button = Button(ax_button, "Reset", hovercolor='0.975')

def update(val=None):
    amp = s_amp.val
    freq = s_freq.val
    phase = s_phase.val
    noise_mean = s_mean.val
    noise_std = s_std.val
    show_noise = check_noise.get_status()[0]
    filter_noise = check_filter.get_status()[0]

    line_noise.set_ydata(compute_signal(amp, freq, phase, noise_mean, noise_std, show_noise, filter_noise))
    line_clean.set_ydata(compute_signal(amp, freq, phase, 0, 0, False, False))
    fig.canvas.draw_idle()



s_amp.on_changed(update)
s_freq.on_changed(update)
s_phase.on_changed(update)
s_mean.on_changed(update)
s_std.on_changed(update)
check_noise.on_clicked(update)
check_filter.on_clicked(update)


def reset(event):
    s_amp.reset()
    s_freq.reset()
    s_phase.reset()
    s_mean.reset()
    s_std.reset()
    check_noise.set_active(0)  
    check_filter.set_active(0)
    update()

button.on_clicked(reset)

plt.show()

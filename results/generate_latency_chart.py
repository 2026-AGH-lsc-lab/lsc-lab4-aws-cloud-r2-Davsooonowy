# Run from project root: python3 results/generate_latency_chart.py
# Generates latency-decomposition stacked bar chart for Assignment 2
# Data from: CloudWatch REPORT lines + curl TCP connect time measurement

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ── Measured data ────────────────────────────────────────────────────────────
# Network RTT: measured via `curl -s -w '%{time_connect}' -o /dev/null <lambda-url>`
NETWORK_RTT = 199  # ms

# Cold start Init Duration: avg of CloudWatch REPORT lines (Init Duration field)
# Zip: 4 cold starts → avg 624 ms
# Container typical (excl. first image pull): 2 events → avg 627 ms
ZIP_INIT        = 624
CONTAINER_INIT  = 627

# Handler Duration: avg of cold-start REPORT lines
ZIP_COLD_HANDLER       = 58   # ms (avg across 4 cold-start invocations)
CONTAINER_COLD_HANDLER = 44   # ms (avg across 2 typical cold-start invocations)

# Warm handler duration: avg of 20 warm invocations via aws lambda invoke
ZIP_WARM_HANDLER       = 76   # ms
CONTAINER_WARM_HANDLER = 79   # ms

# ── Bar data ─────────────────────────────────────────────────────────────────
labels   = ['Zip\n(Cold Start)', 'Container\n(Cold Start)', 'Zip\n(Warm)', 'Container\n(Warm)']
network  = [NETWORK_RTT,  NETWORK_RTT,  NETWORK_RTT,  NETWORK_RTT]
init     = [ZIP_INIT,     CONTAINER_INIT, 0,            0]
handler  = [ZIP_COLD_HANDLER, CONTAINER_COLD_HANDLER, ZIP_WARM_HANDLER, CONTAINER_WARM_HANDLER]

x = np.arange(len(labels))
width = 0.5

# ── Plot ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))

bars_net  = ax.bar(x, network, width, label='Network RTT (~199 ms, client outside AWS)',
                   color='#5B9BD5', zorder=3)
bars_init = ax.bar(x, init,    width, bottom=network,
                   label='Init Duration (cold start only)', color='#ED7D31', zorder=3)
bars_hand = ax.bar(x, handler, width,
                   bottom=[n + i for n, i in zip(network, init)],
                   label='Handler Duration', color='#70AD47', zorder=3)

# Total labels on top of each bar
totals = [n + i + h for n, i, h in zip(network, init, handler)]
for xi, total in zip(x, totals):
    ax.text(xi, total + 10, f'{total} ms', ha='center', va='bottom', fontsize=10, fontweight='bold')

# SLO line
ax.axhline(500, color='red', linewidth=1.5, linestyle='--', zorder=4)
ax.text(x[-1] + 0.35, 505, 'SLO: p99 < 500 ms', color='red', fontsize=9, va='bottom')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=11)
ax.set_ylabel('Latency (ms)', fontsize=11)
ax.set_title('Lambda Latency Decomposition — Cold Start vs. Warm\n'
             '(us-east-1, 512 MB; data from CloudWatch REPORT lines + TCP connect time)',
             fontsize=11)
ax.legend(fontsize=9)
ax.set_ylim(0, max(totals) * 1.18)
ax.yaxis.grid(True, alpha=0.4, zorder=0)
ax.set_axisbelow(True)

plt.tight_layout()
out = 'results/figures/latency-decomposition.png'
plt.savefig(out, dpi=150)
print(f'Saved to {out}')

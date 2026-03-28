# Run from project root: python3 results/generate_cost_chart.py
import numpy as np
import matplotlib.pyplot as plt

rps = np.linspace(0, 15, 300)
seconds_per_month = 30 * 24 * 3600

lambda_cost = rps * 2.16
ec2_cost = np.full_like(rps, 14.98)
fargate_cost = np.full_like(rps, 17.78)

fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(rps, lambda_cost, label='Lambda', color='#FF9900', linewidth=2)
ax.axhline(14.98, label='EC2 t3.small', color='#232F3E', linewidth=2, linestyle='--')
ax.axhline(17.78, label='Fargate (0.5 vCPU / 1 GB)', color='#1A73E8', linewidth=2, linestyle='-.')

ax.axvline(6.93, color='#232F3E', linewidth=1, linestyle=':', alpha=0.7)
ax.axvline(8.23, color='#1A73E8', linewidth=1, linestyle=':', alpha=0.7)
ax.axvline(3.23, color='gray', linewidth=1, linestyle=':', alpha=0.7)

ax.annotate('Break-even\nLambda=EC2\n~6.93 RPS', xy=(6.93, 14.98),
            xytext=(7.5, 10), arrowprops=dict(arrowstyle='->', color='#232F3E'),
            fontsize=8, color='#232F3E')
ax.annotate('Break-even\nLambda=Fargate\n~8.23 RPS', xy=(8.23, 17.78),
            xytext=(9.5, 13), arrowprops=dict(arrowstyle='->', color='#1A73E8'),
            fontsize=8, color='#1A73E8')
ax.annotate('This model\n3.23 RPS avg\n$6.97/mo', xy=(3.23, 3.23 * 2.16),
            xytext=(1, 12), arrowprops=dict(arrowstyle='->', color='#FF9900'),
            fontsize=8, color='#FF9900')

ax.set_xlabel('Average RPS (sustained over month)')
ax.set_ylabel('Monthly cost (USD)')
ax.set_title('Cost vs. Average RPS — Lambda vs. EC2 vs. Fargate\n(us-east-1, 512 MB, p50 handler 76 ms)')
ax.legend()
ax.set_xlim(0, 15)
ax.set_ylim(0, 35)
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('results/figures/cost-vs-rps.png', dpi=150)
print('Saved to results/figures/cost-vs-rps.png')
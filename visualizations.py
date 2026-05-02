import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

try:
    flask_df = pd.read_csv("results_flask.csv")
    flask_df["Server"] = "Flask (Sync)"

    aio_df = pd.read_csv("results_aiohttp.csv")
    aio_df["Server"] = "aiohttp (Async)"

    df = pd.concat([flask_df, aio_df])
except FileNotFoundError:
    print("CSV files not found! Make sure you have run the benchmarks first.")
    exit()

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (10, 6)

# --- GRAPH 1: Throughput (RPS) vs Concurrency ---
plt.figure()
sns.lineplot(data=df, x="concurrency", y="throughput_rps", hue="Server", marker="o")
plt.title("Throughput Analysis: Requests Per Second", fontsize=14)
plt.xlabel("Concurrent Users", fontsize=12)
plt.ylabel("RPS (Success Rate)", fontsize=12)
plt.savefig("GRAPH1_(throughput_comparison).png")

# --- GRAPH 2: Latency (P95) vs Concurrency ---
plt.figure()
sns.lineplot(data=df, x="concurrency", y="p95_lat", hue="Server", marker="s")
plt.title("95th Percentile Latency", fontsize=14)
plt.xlabel("Concurrent Users", fontsize=12)
plt.ylabel("Latency (Seconds)", fontsize=12)
plt.savefig("GRAPH2_(latency_p95_comparison).png")

# --- GRAPH 3: CPU Efficiency ---
plt.figure()
sns.barplot(data=df, x="concurrency", y="cpu_percent", hue="Server")
plt.title("CPU Resource Consumption", fontsize=14)
plt.xlabel("Concurrent Users", fontsize=12)
plt.ylabel("CPU Usage %", fontsize=12)
plt.savefig("GRAPH3_(cpu_usage_comparison).png")

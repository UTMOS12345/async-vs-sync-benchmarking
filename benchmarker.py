import asyncio
import csv
import time

import aiohttp
import numpy as np
import psutil

# --- SETTINGS ---
# Change PORT to 5000 for Flask, 5001 for aiohttp
PORT = 5001
URL = f"http://127.0.0.1:{PORT}/test"
CONCURRENCY_LEVELS = [10, 50, 100, 200, 500]
REQUESTS_PER_LEVEL = 1000


def get_server_process(port):
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            for conn in proc.net_connections(kind="inet"):
                if conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None


async def send_request(session):
    start = time.perf_counter()
    try:
        async with session.get(URL, timeout=10) as response:
            await response.read()
            return time.perf_counter() - start
    except:
        return None


async def run_test(concurrency, server_proc):
    print(f"Testing {concurrency} concurrent users...")

    if server_proc:
        server_proc.cpu_percent(interval=None)

    latencies = []
    # Limit concurrency using a Semaphore
    sem = asyncio.Semaphore(concurrency)
    start_test_time = time.perf_counter()

    async with aiohttp.ClientSession() as session:

        async def limited_task():
            async with sem:
                return await send_request(session)

        tasks = [limited_task() for _ in range(REQUESTS_PER_LEVEL)]
        results = await asyncio.gather(*tasks)

    total_duration = time.perf_counter() - start_test_time
    latencies = [r for r in results if r is not None]

    cpu_usage = server_proc.cpu_percent(interval=None) if server_proc else 0
    ram_usage = server_proc.memory_info().rss / (1024 * 1024) if server_proc else 0

    return {
        "concurrency": concurrency,
        "avg_lat": np.mean(latencies) if latencies else 0,
        "p95_lat": np.percentile(latencies, 95) if latencies else 0,
        "throughput_rps": len(latencies) / total_duration,
        "cpu_percent": cpu_usage,
        "ram_mb": ram_usage,
        "success_rate": (len(latencies) / REQUESTS_PER_LEVEL) * 100,
    }


async def main():
    server_proc = get_server_process(PORT)
    if not server_proc:
        print(f"Error no server found on Port:{PORT}. Start your server first.")

    all_data = []
    for level in CONCURRENCY_LEVELS:
        data = await run_test(level, server_proc)
        all_data.append(data)
        await asyncio.sleep(2)

    #  CSV
    filename = f"results_{'flask' if PORT == 5000 else 'aiohttp'}.csv"
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
        writer.writeheader()
        writer.writerows(all_data)
    print(f"Saved to {filename}.")


if __name__ == "__main__":
    asyncio.run(main())

# async-vs-sync-benchmarking
Comparing Flask (Sync) and aiohttp (Async) performance using custom load testing and hardware resource monitoring.

## Async vs Sync Benchmark

A performance comparison between **Synchronous (Flask)** and **Asynchronous (aiohttp)** web architectures. This project analyzes how different concurrency models handle high load and system resource consumption.

---

### Key Features
*   **Load Generation:** Custom asynchronous script to simulate hundreds of concurrent users.
*   **Hardware Telemetry:** Real-time tracking of **CPU %** and **RAM (MB)** usage during tests.
*   **Data Analysis:** Automated calculation of **P95 Latency** and throughput (RPS).
*   **Visualization:** Built-in plotting using Seaborn to compare performance metrics.

---

### Project Structure
*   `flask_server.py`: Multi-threaded synchronous baseline.
*   `aio_server.py`: Event-loop based asynchronous server.
*   `ee_benchmarker.py`: The testing engine that collects performance data.
*   `generate_graphs.py`: Script to process results into visual charts.
*   `requirements.txt`: Core dependencies.

---

### Quick Start

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Benchmark:**
   * Start your chosen server (e.g., `python flask_server.py`).
   * In a second terminal, run: `python ee_benchmarker.py`.
   * Repeat for the second server (update the port in the script).

3. **Generate Graphs:**
   ```bash
   python generate_graphs.py
   ```

---

### Skills Demonstrated
*   **Backend:** Python (Asyncio, Flask, aiohttp).
*   **Systems:** Linux process monitoring and resource management.
*   **Data Science:** Statistical performance analysis and data visualization.
```

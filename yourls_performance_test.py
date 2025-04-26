import gevent.monkey
gevent.monkey.patch_all()

import sys
# Safeguard crashing
sys.setrecursionlimit(5000)

import requests
import time
import json
import subprocess
import psutil
import csv
import os
import random
from locust import HttpUser, task, between

# Configuration
YOURLS_API_URL = "http://localhost:8080/yourls-api.php"
YOURLS_SIGNATURE = os.getenv("YOURLS_SIGNATURE", "") # Place signature here!
LOG_FILE = "yourls_test_results.csv" # Change this as needed for different deployments!
SHORT_URLS = []

def fetch_random_wikipedia_url():
    try:
        response = requests.get("https://en.wikipedia.org/api/rest_v1/page/random/summary", timeout=5)
        if response.status_code == 200:
            wiki_url = response.json()["content_urls"]["desktop"]["page"]
            print(f"SUCCESS: Fetched Wikipedia URL: {wiki_url}")
            return wiki_url
    except requests.RequestException as e:
        print(f"ERROR: Issue fetching Wikipedia URL: {e}")
    return "https://example.com"

def shorten_url():
    long_url = fetch_random_wikipedia_url()
    if random.random() < 0.3 and SHORT_URLS:
        long_url = random.choice(SHORT_URLS)
    long_url = f"{long_url}?t={int(time.time())}"
    start_time = time.time()

    response = requests.get(YOURLS_API_URL, params={
        "signature": YOURLS_SIGNATURE,
        "action": "shorturl",
        "url": long_url,
        "format": "json"
    })

    duration = time.time() - start_time

    if response.status_code == 200:
        data = response.json()
        short_url = data.get("shorturl", None)
        if short_url:
            SHORT_URLS.append(short_url)
            print(f"SUCCESS: Shortened: {long_url} -> {short_url} in {duration:.4f}s")
            return short_url, duration
    print(f"ERROR: Failed to shorten URL: {response.status_code} - {response.text}")
    return None, duration

def test_redirection(short_url):
    start_time = time.time()
    response = requests.get(short_url, allow_redirects=False)
    duration = time.time() - start_time

    if response.status_code in [301, 302]:
        print(f"SUCCESS: Redirected in {duration:.4f}s: {short_url}")
    else:
        print(f"ERROR: Failed redirection: {response.status_code}")
    return duration

def monitor_resources():
    cpu_usage = psutil.cpu_percent(interval=1)
    mem_usage = psutil.virtual_memory().percent
    return cpu_usage, mem_usage

def run_locust_test():
    print("TRIAL: Running Locust Load Test...")
    os.system("locust -f yourls_locust_test.py --headless -u 300 -r 50 --run-time 2m --host=http://localhost:8080")

def run_tests():
    num_requests = 500
    success_count = 0
    total_shorten_latency = 0

    print("TRIAL: Running URL Shortening Test...")
    start_time = time.time()
    for _ in range(num_requests):
        short_url, duration = shorten_url()
        if short_url:
            total_shorten_latency += duration
            success_count += 1
    end_time = time.time()

    avg_shorten_latency = total_shorten_latency / success_count if success_count else 0
    throughput = success_count / (end_time - start_time) if success_count else 0

    print("TRIAL: Running Redirection Test...")
    total_redirect_latency = 0
    redirect_count = 0
    for short_url in SHORT_URLS:
        redir_duration = test_redirection(short_url)
        total_redirect_latency += redir_duration
        redirect_count += 1
    avg_redirect_latency = total_redirect_latency / redirect_count if redirect_count else 0

    if SHORT_URLS:
        run_locust_test()

    print("TRIAL: Monitoring System Usage...")
    cpu_total = 0
    mem_total = 0
    samples = 5
    for _ in range(samples):
        cpu, mem = monitor_resources()
        print(f"During Load - CPU Usage: {cpu}%, Memory Usage: {mem}%")
        cpu_total += cpu
        mem_total += mem
        time.sleep(1)
    avg_cpu = cpu_total / samples
    avg_mem = mem_total / samples

    print("\nTEST SUMMARY:")
    print(f" Successful Requests: {success_count}/{num_requests}")
    print(f" Average Shorten Time: {avg_shorten_latency:.4f}s")
    print(f" Average Redirect Time: {avg_redirect_latency:.4f}s")
    print(f" Average CPU Usage: {avg_cpu:.2f}%")
    print(f" Average Memory Usage: {avg_mem:.2f}%")
    print(f" Throughput: {throughput:.2f} requests/sec")

    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Metric", "Value"])
        writer.writerow(["Average Shorten Time (s)", round(avg_shorten_latency, 4)])
        writer.writerow(["Average Redirect Time (s)", round(avg_redirect_latency, 4)])
        writer.writerow(["Average CPU Usage (%)", round(avg_cpu, 2)])
        writer.writerow(["Average Memory Usage (%)", round(avg_mem, 2)])
        writer.writerow(["Throughput (requests/sec)", round(throughput, 2)])

    print(f"Results saved to {LOG_FILE}")

if __name__ == "__main__":
    run_tests()

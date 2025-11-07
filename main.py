import time
import multiprocessing

def cpu_load(duration=10):
    """Generate CPU load for a specified duration"""
    start_time = time.time()
    while time.time() - start_time < duration:
        # Perform intensive calculations
        _ = sum(i * i for i in range(1000000000000))

def main():
    print("Starting CPU load test...")
    
    # Get CPU count
    cpu_count = multiprocessing.cpu_count()
    processes = []

    # Create processes for each CPU core
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=cpu_load)
        processes.append(p)
        p.start()

    # Wait for all processes to complete
    for p in processes:
        p.join()

    print("Load test complete")

if __name__ == "__main__":
    main()
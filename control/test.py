import time

def measure_response_time(delay):

    start_cpu = time.ticks_cpu()  # CPU cycle count

    time.sleep_ms(delay)

    # Get CPU end time
    end_cpu = time.ticks_cpu()
    cpu_cycles = time.ticks_diff(end_cpu, start_cpu)

    # Convert cycles to microseconds (125MHz → 8ns per cycle)
    cpu_time_us = cpu_cycles * 0.001  # CPU time in us

    return "{:0.4f}".format(cpu_time_us)
    return cpu_time_us

######################### MAIN #########################

for i in range(0, 1100, 100):
    teststr = measure_response_time(i)
    print(teststr)

print()

print("title")
print("    subtitle")

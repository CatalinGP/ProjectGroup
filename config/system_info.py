import os
import psutil

def get_system_info():

    # Get RAM details
    ram_details = os.popen('wmic memorychip get capacity').read().split('\n')
    total_ram = sum(int(x) for x in ram_details[1:] if x)
    total_ram_gb = total_ram / (1024 ** 3)

    # Get CPU count
    cpu_count = os.cpu_count()

    # Get available memory
    disk_details = dict()
    partitions = psutil.disk_partitions()
    for partition in partitions:
        disk_usage = psutil.disk_usage(partition.mountpoint)
        free_space_gb = disk_usage.free / (1024 * 1024 * 1024)
        disk_details[partition.mountpoint] = free_space_gb
        disk_details[partition.mountpoint] = round(free_space_gb, 2)

    return total_ram_gb, cpu_count, disk_details

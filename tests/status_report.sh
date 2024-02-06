#!/bin/bash

echo "VM Status Report"
echo "-----------------"
echo "Date and Time:"
date
echo ""

echo "Uptime:"
uptime
echo ""

echo "Current Users:"
who
echo ""

echo "Memory Usage:"
free -h
echo ""

echo "Disk Usage:"
df -h
echo ""

echo "CPU Load:"
top -bn1 | grep load | awk '{printf "CPU Load: %.2f\n", $(NF-2)}'
echo ""

echo "Network Interfaces and IP Addresses:"
ip addr

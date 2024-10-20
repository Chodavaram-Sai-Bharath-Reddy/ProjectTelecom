# SD-WAN Python Simulation

## Overview

This Python program simulates key features of an SD-WAN (Software-Defined Wide Area Network) solution, focusing on failover, load balancing, and SLA-compliant routing across multiple WAN links. The program provides a framework for managing multiple WAN options and ensures traffic is routed efficiently to maintain performance and reliability.

### Key Features:

1. **Conventional Failover**: Automatically shifts traffic to a backup link if a primary link fails, ensuring business continuity.
2. **Load Balancing**: Distributes traffic across multiple WAN links using either simple round-robin or weighted round-robin methods.
3. **SLA-Compliant Routing**: Routes application traffic based on Service Level Agreement (SLA) parameters (latency, jitter, and packet loss). Traffic is rerouted if these parameters are violated.

## Prerequisites

- Python 3.x
- No external dependencies

## Usage

### 1. Defining WAN Links

Each WAN link has attributes such as `latency`, `jitter`, and `loss`. You can create multiple WAN links to represent different connectivity options (e.g., Internet, MPLS, Cellular).

```python
linkA = WANLink("Internet", latency=10, jitter=5, loss=1, weight=3)
linkB = WANLink("MPLS", latency=20, jitter=10, loss=2, weight=2)
linkC = WANLink("Cellular", latency=30, jitter=15, loss=3, weight=1)
backup_link = WANLink("Backup MPLS", latency=50, jitter=30, loss=5, weight=0)
```

### 2. Initializing the SD-WAN Router

Create an SD-WAN router that manages multiple WAN links and an optional backup link.

```python
router = SDWANRouter([linkA, linkB, linkC], backup_link)
```

### 3. Load Balancing

Use round-robin or weighted round-robin techniques to distribute traffic across all active links:

- **Round-Robin**:
```python
router.round_robin(6)  # Distribute 6 sessions using round-robin
```

- **Weighted Round-Robin**:
```python
router.weighted_round_robin(6)  # Distribute 6 sessions using weights
```

### 4. SLA-Compliant Routing

Ensure that traffic is routed only through links that meet specific performance thresholds, defined by SLA parameters (e.g., max latency, jitter, and loss).

```python
sla_requirements = (20, 10, 2)  # max_latency, max_jitter, max_loss
router.sla_compliant_routing(sla_requirements)
```

### 5. Simulating Link Failures

Simulate a link failure and test how the system handles failover:

```python
linkA.fail()  # Simulate failure of the Internet link
router.failover()  # Traffic will shift to backup link
```

You can also recover the link and test again:
```python
linkA.recover()  # Recover Internet link
router.failover()  # Check if the system shifts back to primary links
```

## Example

Here's a brief example that showcases the core functionality of the SD-WAN simulation:

```python
# Setup WAN Links and Backup Link
linkA = WANLink("Internet", latency=10, jitter=5, loss=1, weight=3)
linkB = WANLink("MPLS", latency=20, jitter=10, loss=2, weight=2)
linkC = WANLink("Cellular", latency=30, jitter=15, loss=3, weight=1)
backup_link = WANLink("Backup MPLS", latency=50, jitter=30, loss=5, weight=0)

# Setup Router with WAN Links and Backup Link
router = SDWANRouter([linkA, linkB, linkC], backup_link)

# Run tests
router.round_robin(6)  # Round-robin load balancing for 6 sessions
router.weighted_round_robin(6)  # Weighted round-robin load balancing for 6 sessions

# SLA-based routing
sla_requirements = (20, 10, 2)  # max_latency, max_jitter, max_loss
router.sla_compliant_routing(sla_requirements)

# Simulate Link Failures and Failover
linkA.fail()  # Fail Internet link
router.failover()  # Shift traffic to backup link
linkA.recover()  # Recover Internet link
router.failover()  # Return to normal
```

## Customization

You can modify the `latency`, `jitter`, `loss`, and `weight` parameters of each WAN link to simulate various network conditions. The load balancing methods and SLA checks can also be adapted to fit more complex scenarios or more advanced SD-WAN algorithms.

## Future Enhancements

- **Dynamic Weight Adjustment**: Modify link weights based on real-time performance monitoring.
- **More Load Balancing Techniques**: Implement additional strategies like least-latency routing or adaptive routing.
- **Traffic Simulation**: Add functionality to simulate traffic load or congestion to stress-test the WAN links.

---

By following the above steps, you can simulate a robust SD-WAN solution for managing multiple WAN links while ensuring compliance with business-critical SLAs.

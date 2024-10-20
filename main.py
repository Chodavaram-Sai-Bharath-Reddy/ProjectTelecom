import random


# Define a class for WAN links with attributes like latency, jitter, and loss
class WANLink:
    def __init__(self, name, latency, jitter, loss, weight=1):
        self.name = name
        self.latency = latency  # in ms
        self.jitter = jitter  # in ms
        self.loss = loss  # in percentage
        self.weight = weight  # for weighted load balancing
        self.active = True

    # Method to simulate link failure
    def fail(self):
        self.active = False
        print(f"{self.name} has failed.")

    # Method to simulate link recovery
    def recover(self):
        self.active = True
        print(f"{self.name} has recovered.")

    # Method to check if the link meets SLA requirements
    def check_sla(self, max_latency, max_jitter, max_loss):
        return (self.latency <= max_latency and
                self.jitter <= max_jitter and
                self.loss <= max_loss and
                self.active)

    def __repr__(self):
        return f"WANLink(name={self.name}, latency={self.latency}, jitter={self.jitter}, loss={self.loss}, active={self.active})"


# Define a class for an SD-WAN router with multiple WAN links
class SDWANRouter:
    def __init__(self, links, backup_link=None):
        self.links = links
        self.backup_link = backup_link

    # Conventional backup: Shift all traffic to backup link when primary fails
    def failover(self):
        for link in self.links:
            if not link.active:
                print(f"Primary link {link.name} has failed! Shifting to backup link {self.backup_link.name}.")
                return self.backup_link
        print("All links are operational, no need for failover.")
        return None

    # Load balancing with round-robin technique
    def round_robin(self, sessions):
        link_index = 0
        for session in range(sessions):
            link = self.links[link_index]
            if link.active:
                print(f"Session {session + 1} is routed to {link.name}")
            else:
                print(f"Session {session + 1} cannot use {link.name}, link is down!")
            link_index = (link_index + 1) % len(self.links)

    # Load balancing with weighted round-robin technique
    def weighted_round_robin(self, sessions):
        total_weight = sum([link.weight for link in self.links if link.active])
        weights = [link.weight / total_weight for link in self.links if link.active]
        link_pool = []
        for i, link in enumerate(self.links):
            if link.active:
                link_pool.extend([link] * int(weights[i] * 100))

        for session in range(sessions):
            chosen_link = random.choice(link_pool)
            print(f"Session {session + 1} is routed to {chosen_link.name}")

    # SLA-based routing example: latency <= 20ms, jitter <= 10ms, loss <= 2%
    def sla_compliant_routing(self, application_sla):
        for link in self.links:
            if link.check_sla(*application_sla):
                print(f"Application routed to {link.name} (SLA-compliant)")
                return link
        print("No link meets the SLA requirements, shifting to backup or best available link.")
        if self.backup_link and self.backup_link.active:
            return self.backup_link
        return self.get_best_available_link()

    # Method to get the best available link based on lowest latency
    def get_best_available_link(self):
        available_links = [link for link in self.links if link.active]
        if available_links:
            best_link = min(available_links, key=lambda link: link.latency)
            print(f"Rerouted to {best_link.name} (best latency available)")
            return best_link
        print("No available links.")
        return None


# Example of setting up WAN links and backup
linkA = WANLink("Internet", latency=10, jitter=5, loss=1, weight=3)
linkB = WANLink("MPLS", latency=20, jitter=10, loss=2, weight=2)
linkC = WANLink("Cellular", latency=30, jitter=15, loss=3, weight=1)
backup_link = WANLink("Backup MPLS", latency=50, jitter=30, loss=5, weight=0)

# Setup SD-WAN router with these links and a backup link
router = SDWANRouter([linkA, linkB, linkC], backup_link)

# Test 1: Round-robin load balancing
print("Round-robin load balancing for 6 sessions:")
router.round_robin(6)

# Test 2: Weighted round-robin load balancing
print("\nWeighted round-robin load balancing for 6 sessions:")
router.weighted_round_robin(6)

# Test 3: SLA-based routing
sla_requirements = (20, 10, 2)
print("\nSLA-based routing for an application:")
router.sla_compliant_routing(sla_requirements)

# Test 4: Fail over to back up when a link fails
print("\nSimulating link failure and failover:")
linkA.fail()
router.failover()

# Test 5: Recover link and retest failover
print("\nSimulating link recovery:")
linkA.recover()
router.failover()

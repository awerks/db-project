import matplotlib.pyplot as plt
import datetime
<<<<<<< HEAD
from collections import defaultdict
import matplotlib.lines as mlines


=======
import matplotlib.lines as mlines
from collections import defaultdict
>>>>>>> fc93d8d (Added autocomplete)
log_file = "app.log"
logs = []

with open(log_file, "r") as file:
    logs = file.readlines()


access_details = defaultdict(list)
errors = []


exclude_keywords = ["logo", "icon", "css"]


for log in logs:
    parts = log.split(" - ")
    timestamp_str = parts[0]
    ip_address = parts[1].strip()
    endpoint = parts[3].strip()
    browser_info = parts[4].strip()

    if any(keyword in endpoint.lower() for keyword in exclude_keywords):
        continue

    timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

    access_details[endpoint].append((timestamp, ip_address, browser_info))


unique_ips = set(ip for _, ip, _ in errors + [entry for details in access_details.values() for entry in details])
ip_color_map = {ip: plt.cm.jet(i / len(unique_ips)) for i, ip in enumerate(unique_ips)}


unique_browsers = set(
    browser for _, _, browser in errors + [entry for details in access_details.values() for entry in details]
)
browser_color_map = {browser: plt.cm.viridis(i / len(unique_browsers)) for i, browser in enumerate(unique_browsers)}


plt.figure(figsize=(12, 6))
timestamps = []
labels = []
ip_colors = []
browser_colors = []

for endpoint, details in access_details.items():
    for timestamp, ip, browser in details:
        timestamps.append(timestamp)
        labels.append(f"[{ip}]: {endpoint}\n")
        ip_colors.append(ip_color_map[ip])
        browser_colors.append(browser_color_map[browser])


plt.scatter(timestamps, range(len(timestamps)), color=browser_colors)


for i, (timestamp, label) in enumerate(zip(timestamps, labels)):
    plt.text(timestamp, i, label, fontsize=9, verticalalignment="bottom")


ip_handles = [
    mlines.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=8, label=ip)
    for ip, color in ip_color_map.items()
]
browser_handles = [
    mlines.Line2D([0], [0], marker="o", color="w", markerfacecolor=color, markersize=8, label=browser)
    for browser, color in browser_color_map.items()
]
plt.legend(handles=browser_handles, title="Browsers", loc="upper left", fontsize="small")

plt.xlabel("Time")
plt.title("Timeline Diagram of Page Accesses")
plt.yticks([])
plt.grid(axis="x")
plt.tight_layout()

plt.savefig("timeline.png")

plt.show()

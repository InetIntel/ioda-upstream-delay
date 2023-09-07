import matplotlib.pyplot as plt
import numpy as np
from Analysis.bundleAnalysis import bgp_data_overview


def bundle_data_plot(as_bundle_prefix_as_paths):
    data = bgp_data_overview(as_bundle_prefix_as_paths)
    bundle_sizes_distribution = data["bundle_sizes_distribution"]

    sizes, counts = zip(*bundle_sizes_distribution.items())

    plt.bar(sizes, counts)
    plt.xlabel("Bundle Size")
    plt.ylabel("Count")
    plt.title("Bundle Size Distribution")
    plt.xlim(0, 200)
    plt.yscale("log")
    plt.show()
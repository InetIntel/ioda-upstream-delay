"""
AS - Prefix - AS path
AS - Bundle - Prefixes : AS paths
	3D Map int[int[string[string]]]
	AS number int[]
		Bundle ID AS_path[]
			Val: string[]
            1. Prefixes string

Bundle: Groups of Prefixes in AS that with shared AS path
"""
def compute_as_bundle_prefix_as_paths(as_prefix_mapping, prefix_path_mapping):

    as_bundle_prefix_as_paths = {}
    
    for as_number, prefixes in as_prefix_mapping.items():
        as_bundle_map = {}
        
        for prefix in prefixes:
            as_path = prefix_path_mapping.get(prefix, [])
            as_path_str = ' '.join(as_path)
            bundle_id = as_path_str
            if bundle_id in as_bundle_map:
                if prefix not in as_bundle_map[bundle_id]:
                    as_bundle_map[bundle_id].append(prefix)
            else:
                as_bundle_map[bundle_id] = [prefix]
        
        as_bundle_prefix_as_paths[as_number] = as_bundle_map
    
    return as_bundle_prefix_as_paths


"""
Bundle change: 

	Basic info calculation
    
	1. If one prefix has a different AS path (how different it is?) how many other prefixes in the original bundle also have changed AS path
		Iterate through the ASes (now AS - Bundle - Prefix : AS path)
        
    Capture multiple snapshots::
    Pick two consecutive snapshots:
		1. Compare basic info (call above function)
		Iterate through ASes
			Iterate through bundle id
            compare the prefixes
				is it different? if so which prefix changes to which bundle
            
            How many bundle are the same for this AS
            If different, how does the difference look like
"""

def calculate_bundle_changes_per_VP(snapshot_series):
    common_bundle_prefixes_list = []
    seen_bundle_prefixes = None 
    
    for i in range(len(snapshot_series)):
        if seen_bundle_prefixes is None:
            seen_bundle_prefixes = snapshot_series[i]
            continue
        
        snapshot = snapshot_series[i]

        common_bundle_prefixes = {}

        common_as_numbers = set(seen_bundle_prefixes.keys()) & set(snapshot.keys())
        for as_number in common_as_numbers:
            bundle_map_all = seen_bundle_prefixes[as_number]
            bundle_map = snapshot[as_number]
            common_bundle_ids = set(bundle_map.keys()) & set(bundle_map_all.keys())

            for bundle_id in common_bundle_ids:
                prefixes_curr = set(prefix for prefix in bundle_map[bundle_id])
                prefixes_all = set(prefix for prefix in bundle_map_all[bundle_id])
                if len(prefixes_curr) <= 1 or len(prefixes_all) <= 1:
                    continue
                common_prefixes = prefixes_curr & prefixes_all

                if common_prefixes:
                    common_bundle_prefixes.setdefault(as_number, {})
                    common_bundle_prefixes[as_number][bundle_id] = list(common_prefixes)

                    seen_bundle_prefixes.setdefault(as_number, {}).setdefault(bundle_id, set()).extend(prefixes_curr)

        common_bundle_prefixes_list.append(common_bundle_prefixes)
    
    return common_bundle_prefixes_list



def capture_peresistant_bundle(snapshot_series):
    pass

def snapshot_analysis(snapshot):
    pass


"""
Examine the bgp data:
    how many AS?
    how many prefixes?
    how many bundles?
    how many bundle has only one prefix?
    how many prefix has multiple AS path to reach?
    also want to see the distribution of bundle sizes
"""

def bgp_data_overview(as_bundle_prefix_as_paths):
    num_as = len(as_bundle_prefix_as_paths)
    num_prefixes = sum(len(prefixes) for bundle_map in as_bundle_prefix_as_paths.values() for prefixes in bundle_map.values())
    num_bundles = sum(len(bundle_map) for bundle_map in as_bundle_prefix_as_paths.values())
    #num_single_prefix_bundles = sum(1 for bundle_map in as_bundle_prefix_as_paths.values() if len(prefixes) == 1 for prefixes in bundle_map.values())
    #TODO: how many bundles contains duplicate prefixes?
    prefix_as_paths = {} 
    bundle_sizes = {}

    for as_number, bundle_map in as_bundle_prefix_as_paths.items():
        for bundle_id, prefixes in bundle_map.items():

            bundle_size = len(prefixes)
            
            if bundle_size not in bundle_sizes:
                bundle_sizes[bundle_size] = 1
            else:
                bundle_sizes[bundle_size] += 1


            for prefix in prefixes:
                if prefix not in prefix_as_paths:
                    prefix_as_paths[prefix] = set()

                prefix_as_paths[prefix].add(bundle_id)

    num_prefixes_with_multiple_as_paths = sum(1 for prefix in prefix_as_paths if len(prefix_as_paths[prefix]) > 1)
    num_single_prefix_bundles = bundle_sizes[1]
    return {
        "num_as": num_as,
        "num_prefixes": num_prefixes,
        "num_bundles": num_bundles,
        "num_single_prefix_bundles": num_single_prefix_bundles,
        "num_prefixes_with_multiple_as_paths": num_prefixes_with_multiple_as_paths,
        "bundle_sizes_distribution": bundle_sizes
    }
"""
result = bgp_data_overview(as_bundle_prefix_as_paths)

print("Number of AS numbers:", result["num_as"])
print("Number of prefixes:", result["num_prefixes"])
print("Number of bundles:", result["num_bundles"])
print("Number of bundles with only one prefix:", result["num_single_prefix_bundles"])
print("Number of prefixes with multiple AS paths to reach:", result["num_prefixes_with_multiple_as_paths"])
"""


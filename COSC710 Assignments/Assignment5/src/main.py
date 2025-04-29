import math
from typing import List, Tuple
# [ [(source, destination, weight), ...] , [(source, destination, weight), ...] ]
#  ie [cluster1 , cluster2,...]
def calculateEntropy(clusters: List[List[Tuple]]):
    validate_clusters(clusters)
    total_size = 0
    for cluster in clusters:
        total_size += len(cluster)


    entropy = 0
    for cluster in clusters:
        p = len(cluster)/total_size
        entropy += p * math.log(p,2)

    return -1*entropy

def calculateMutualInformation(clusters1: List[List[Tuple]], clusters2:List[List[Tuple]]):
    
    validate_between_clusters(clusters1, clusters2)
    n = sum(len(cluster) for cluster in clusters1)  # total number of elements

    # Convert clusters to sets for fast intersection
    sets1 = [set(cluster) for cluster in clusters1]
    sets2 = [set(cluster) for cluster in clusters2]

    mi = 0.0
    for i in range(len(sets1)):
        for j in range(len(sets2)):
            # Set intersection is so nice to have in python ughh
            intersection_size = len(sets1[i].intersection(sets2[j]))
            if intersection_size == 0:
                continue
            pij = intersection_size / n
            pi = len(sets1[i]) / n
            pj = len(sets2[j]) / n
            mi += pij * math.log(pij / (pi * pj), 2)
    return mi


def calculateNMI(clusters1: List[List[Tuple]], clusters2:List[List[Tuple]]):
    validate_between_clusters(clusters1, clusters2)
    mi = calculateMutualInformation(clusters1, clusters2)
    entropy1 = calculateEntropy(clusters1)
    entropy2 = calculateEntropy(clusters2)

    nmi = (2*mi)/(entropy1 + entropy2)
    return nmi

def calculateVI(cluster1:List[List[Tuple]], cluster2:List[List[Tuple]]):
    validate_between_clusters(cluster1, cluster2)
    entropy1 = calculateEntropy(cluster1)
    entropy2 = calculateEntropy(cluster2)
    mi = calculateMutualInformation(cluster1, cluster2)

    # Found this on wikipedia stating its the same as the formula on the slides, im assuming
    # wikipedia is valid because the diagram on the slides is from the wikipedia article:
    #  https://en.wikipedia.org/wiki/Variation_of_information

    vi = (entropy1+entropy2)-(2*mi)
    return vi

def validate_clusters(clusters:List[List[Tuple]]):
    cluster_len = len(clusters[0])
    edge_len = 3
    for cluster in clusters:
        if(cluster_len != len(cluster)):
            raise Exception("One of the cluster lengths is not like the rest")
        for edge in cluster:
            if(len(edge) != edge_len):
                    raise Exception(f"The edge:{edge} does not contain {edge_len} values")

            for val in edge:
                if(not isinstance(val, int)):
                    raise Exception(f"One of the values {val} is not an int, they must all be ints")
        if(cluster[0] == cluster[1]):
            raise Exception("No self-edges!!!!!")

def validate_between_clusters(clusters1:List[List[Tuple]], clusters2:List[List[Tuple]]):
    validate_clusters(clusters1)
    validate_clusters(clusters2)
    # Each are valid on their own at this point, but now check if they are valid with each other

    # Making usre every edge in one, is also in another
    all_edges1 = set( edge for cluster in clusters1  for edge in cluster)
    all_edges2 = set( edge for cluster in clusters2  for edge in cluster)

    if(all_edges1 != all_edges2):
        raise Exception("The two clusters contain differeing edges")


identical_clusters1 = [
    [(0,1,1), (1,2,1)],
    [(2,3,1), (3,4,1)],
    [(4,5,1), (5,6,1)]
]

identical_clusters2 = [
    [(0,1,1), (1,2,1)],
    [(2,3,1), (3,4,1)],
    [(4,5,1), (5,6,1)]
]


shuffled_clusters = [
    [(0,1,1), (4,5,1)],
    [(1,2,1), (2,3,1)],
    [(3,4,1), (5,6,1)]
]


partial_match_clusters = [
    [(0,1,1), (1,2,1)],
    [(2,3,1), (5,6,1)],
    [(3,4,1), (4,5,1)]
]

if __name__ == '__main__':
    passed = True
    log2_3 = math.log(3, 2)
    entropy = calculateEntropy(identical_clusters1)
    if abs(entropy - log2_3) < 1e-6:
        print(f"Entropy test passed: {entropy=}, expected={log2_3}")
    else:
        print(f"Entropy test failed: {entropy=}, expected={log2_3}")
        passed = False

    # MI identical
    mi_identical = calculateMutualInformation(identical_clusters1, identical_clusters2)
    if abs(mi_identical - log2_3) < 1e-6:
        print(f"Mutual Information (identical) test passed: mi={mi_identical}, expected={log2_3}")
    else:
        print(f"Mutual Information (identical) test failed: mi={mi_identical}, expected={log2_3}")
        passed = False

    # NMI identical
    nmi_identical = calculateNMI(identical_clusters1, identical_clusters2)
    excpected = 1.0
    if abs(nmi_identical - 1.0) < 1e-6:
        print(f"Normalized Mutual Information (identical) test passed: nmi={nmi_identical}, expected=1.0")
    else:
        print(f"Normalized Mutual Information (identical) test failed: nmi={nmi_identical}, expected=1.0")
        passed = False

    # VI identical
    vi_identical = calculateVI(identical_clusters1, identical_clusters2)
    if abs(vi_identical - 0.0) < 1e-6:
        print(f"Variation of Information (identical) test passed: vi={vi_identical}, expected=0.0")
    else:
        print(f"Variation of Information (identical) test failed: vi={vi_identical}, expected=0.0")
        passed = False

    # VI partial
    vi_partial = calculateVI(identical_clusters1, partial_match_clusters)
    if 0.0 < vi_partial < 2 * log2_3:
        print(f"Variation of Information (partial) test passed: vi={vi_partial}")
    else:
        print(f"Variation of Information (partial) test failed: vi={vi_partial}")
        passed = False

    # MI partial
    mi_partial = calculateMutualInformation(identical_clusters1, partial_match_clusters)
    if 0.0 < mi_partial < log2_3:
        print(f"Mutual Information (partial) test passed: mi={mi_partial}")
    else:
        print(f"Mutual Information (partial) test failed: mi={mi_partial}")
        passed = False

    print()
    if passed:
        print(f"\nAll tests passed.")
    else:
        print(f"\nSome tests failed.")
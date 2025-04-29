
# Assignment 5 clustering metrics 

This module provides a way to calculate the Entropy, Mutual Information, Normalized Mutual Information, and the Variance of Information for a given set of clusters.


## Clusters Format

Each cluster needs to be a List of List of Tuple.

The outer List, is a collection of clusters of a graph

The inner list is a collection of tuples to represent each edge within a cluster

The edges take on the format: (source, destination, weight)
## Overview of the Functions

#### calculateEntropy()

Input: clusters: List[List[Tuple[int,int,int]]] - a singular list of clusters 
Output: entropy: float - the entropy score of this set of clusters

#### calculateMutualInformation()
Input: cluster1: List[List[Tuple[int,int,int]]],  clusters2: List[List[Tuple[int,int,int]]] - two different clusterings of the same graph
Output: mutual information score: float

#### calculateNMI()
Input: cluster1: List[List[Tuple[int,int,int]]],  clusters2: List[List[Tuple[int,int,int]]] - two different clusterings of the same graph
Output: normalized mutual information score: float

#### calculateVI()
Input: clusters1: List[List[Tuple[int,int,int]]],  clusters2: List[List[Tuple[int,int,int]]] - two different clusterings of the same graph
Output: Variation of Information score: float - different algorithm from the one on the slides, but using the same wikipedia source, so they should be the same 

#### validate_clusters()
Input: clusters: List[List[Tuple[int,int,int]]]] - list of clusters of a graph
Output: void - raises an exception if the clusters is invalid

    Invalid Reasons
        1. "One of the cluster lengths is not like the rest" - invalid number of clusters
        2. "The edge:{edge} does not contain {edge_len} values" - invalid number of edges within a cluster 
        3. "One of the values {val} is not an int, they must all be ints"- one value in a given edge was not an int
        4. "No self-edges!!!!!" - we do not allow for edges whwere the source and destination are the same

#### validate_between_clusters()
Input: clusters: clusters1: List[List[Tuple[int,int,int]]],  clusters2: List[List[Tuple[int,int,int]]] - two different clusterings of the same graph
Output: void - raises an exception if the clusters are either individually invalid, or invalid with respect to one another

    Invalid Reasons
        1. "The two clusters contain differing edges" - one of the clusterings did not have the same exact edges as the other one

#### Notes
In each non-validate function call, the clusterings given will be validated using either validate_clusters or validate_between_clusters 
## Clustering Input Examples
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

partial_match_clusters = [
    [(0,1,1), (1,2,1)],
    [(2,3,1), (5,6,1)],
    [(3,4,1), (4,5,1)]
]



## Running Tests
Built in are some test cases for the previous clustering inputs set. To run, run the following __main.py__ using python

The tests will run:
* Entropy Tests
* Mi Tests
* NMI Tests
* Vi Tests

The output will tell us if the tests failed or not. 
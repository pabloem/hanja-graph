from collections import Counter
from collections import deque
import networkx as nx

def single_source_number_of_walks(G, source, walk_length):
    """Returns a dictionary whose keys are the vertices of `G` and whose values
    are the numbers of walks of length exactly `walk_length` joining `source`
    to that node.

    Raises :exc:`ValueError` if `walk_length` is negative.

    """
    if walk_length < 0:
        raise ValueError('walk length must be a positive integer')
    # Create a counter to store the number of walks of length
    # `walk_length`. Ensure that even unreachable vertices have count zero.
    result = Counter({v: 0 for v in G})
    queue = deque()
    queue.append((source, 0))
    # TODO We could reduce the number of iterations in this loop by performing
    # multiple `popleft()` calls at once, since the queue is partitioned into
    # slices in which all enqueued vertices in the slice are at the same
    # distance from the source. In other words, if we keep track of the
    # *number* of vertices at each distance, we could just immediately dequeue
    # all of those vertices.
    while queue:
        (u, distance) = queue.popleft()
        if distance == walk_length:
            result[u] += 1
        else:
            # Using `nx.edges()` accounts for multiedges as well.
            queue.extend((v, distance + 1) for u_, v in nx.edges(G, u))
    # Return the result as a true dictionary instead of a Counter object.
    return dict(result)


def all_pairs_number_of_walks(G, walk_length):
    """Returns a dictionary of dictionaries, each with keys that are vertices
    in `G`, representing the number of walks of length `walk_length` joining
    two nodes in `G`.

    Raises :exc:`ValueError` if `walk_length` is negative.

    """
    # TODO This algorithm can certainly be parallelized.
    return {v: single_source_number_of_walks(G, v, walk_length) for v in G}

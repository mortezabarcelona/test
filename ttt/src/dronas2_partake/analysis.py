from typing import TypeVar

from dronas2_partake.model import PartakeConflict, PartakeMission


class Cluster:
    def __init__(self):
        self.missions: set[PartakeMission] = set()
        self.conflicts: list[PartakeConflict] = []

_T = TypeVar('_T', bound=Cluster)

def execute_analysis(
        conflicts: list[PartakeConflict],
        instanceable_class: type[_T] = Cluster
) -> set[_T]:
    clustermap: dict[PartakeMission, Cluster] = {}

    for conflict in conflicts:
        cluster1: Cluster = clustermap.get(conflict.mission1)
        cluster2: Cluster = clustermap.get(conflict.mission2)

        if cluster1 is not None:
            if cluster2 is not None:
                if cluster1 is not cluster2:
                    # Merge
                    cluster1.missions.update(cluster2.missions)
                    cluster1.conflicts.extend(cluster2.conflicts)
                    for m in cluster2.missions:
                        clustermap[m] = cluster1
                # else, they already are in the same cluster
                cluster1.conflicts.append(conflict)
            else:
                # cluster1 exists, cluster2 not
                cluster1.missions.add(conflict.mission2)
                cluster1.conflicts.append(conflict)
                clustermap[conflict.mission2] = cluster1
        else:
            if cluster2 is not None:
                # cluster2 exists, cluster1 not
                cluster2.missions.add(conflict.mission1)
                cluster2.conflicts.append(conflict)
                clustermap[conflict.mission1] = cluster2
            else:
                # none of them exists, create a cluster with them
                cluster1 = instanceable_class()
                cluster1.missions.add(conflict.mission1)
                cluster1.missions.add(conflict.mission2)
                cluster1.conflicts.append(conflict)
                clustermap[conflict.mission1] = cluster1
                clustermap[conflict.mission2] = cluster1

    return set(clustermap.values())

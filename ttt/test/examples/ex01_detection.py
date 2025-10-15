
import logging
from datetime import datetime
from math import floor

## These two lines must go before importing partake detection
# noinspection PyUnusedImports
import import_me_to_start_jvm_with_partake_java_bundle

from dronas2.api.broker import Operation
from dronas2.api.registry import RegistryCache
from dronas2.io import operations
from dronas2_partake import detection, mitigation, analysis
from dronas2_partake.model import PartakeMissionDetection

INPUT_DIR = "../data/"
OUTPUT_DIR = "../../test-out/"

if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.root
    logger.setLevel(logging.DEBUG)
    logger.getChild('MitigationAlgorithm_Batch').setLevel(logging.WARNING)

    operations = operations.read_operations(INPUT_DIR + 'castelldefels.corusxuam.v9.C.1.traffic.json', dependencies=RegistryCache(None).external_retriever)
    operations = operations[:100]

    def op_to_partake(op: Operation):
        return PartakeMissionDetection(
            op.geometry,
            op.tolerance_upper if op.tolerance_upper is not None else 2*60,
            op.tolerance_lower if op.tolerance_lower is not None else 0,
            op.launch_window_upper if op.launch_window_upper is not None else 1*60*15,
            op.launch_window_lower if op.launch_window_lower is not None else 0,
            None,
            True,
            0,
            floor(datetime.timestamp(op.request)),
            None
        )
    operations.sort(key=lambda o: o.request)
    partake_missions = [op_to_partake(op) for i, op in enumerate(operations)]# if i < 1 or 500 < i < 700 or i >= 1300]

    print(f'Detection ({len(partake_missions)} missions)')
    conflicts = detection.execute_detection(partake_missions)

    print(f'Analysis ({len(conflicts)} conflicts)')
    clusters = analysis.execute_analysis(conflicts)

    summation = 0
    print(f'Mitigation ({len(clusters)} clusters)')
    for i, cluster in enumerate(clusters):
        print(f'Cluster {i}')
        summation += len(cluster.missions)

        mitigation_algorithm: mitigation.MitigationAlgorithm_Batch = mitigation.MitigationAlgorithm_Batch(
            cluster.missions,
            cluster.conflicts,
            60,
            None
        )

        with mitigation_algorithm.run_single(10) as runner:
            if runner.is_solved():
                approved = 0
                for k, v in runner.delays.items():
                    if v is not None:
                        approved += 1

                print(f'    Total: {len(runner.delays)} == {len(cluster.missions)}')
                print(f'    Approved: {approved}')
            else:
                print('    Not solved')

        # for j, runner in enumerate(mitigation_algorithm.run_multiple(30)):
        #     runner: MultipleRunner_Abstract = runner
        #
        #     print(f'    Solution {i}-{j}')
        #     if runner.is_solved():
        #         approved = 0
        #         for k, v in runner.delays.items():
        #             if v is not None:
        #                 approved += 1
        #         print(f'        Approved: {sum(1 for k, v in runner.delays.items() if v is not None)}')
        #     else:
        #         print(f'    Not solved')

        print(f'Out of conflict: {len(partake_missions) - summation}')



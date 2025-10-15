import datetime
import json
import logging

import dronas2_partake
## These two lines must go before importing partake detection
# noinspection PyUnusedImports
import import_me_to_start_jvm_with_partake_java_bundle
from dronas2.api.broker import Operation
from dronas2.api.models.dcb_analysis_traffic_set_model import Mission
from dronas2.api.registry import RegistryCache
from dronas2.io import operations
from dronas2_partake.tools.dcb_simulation import DcbSimulator

INPUT_DIR = "../data/"
OUTPUT_DIR = "../../test-out/"

if __name__ == '__main__':

    logging.basicConfig()
    logger = logging.root
    logger.setLevel(logging.DEBUG)
    logger.getChild('MitigationAlgorithm_Batch').setLevel(logging.WARNING)

    # Read all missions from file
    missions: list[Mission] = [
        dronas2_partake.io.missions.convert_operation_into_dcbmission(
            op,
            overwrite_minimum_separation_horizontal=30,
            overwrite_minimum_separation_vertical=30,
            overwrite_tolerance_lower=0,
            overwrite_tolerance_upper=2*60,
            overwrite_launch_window_lower=0,
            overwrite_launch_window_upper=45*60,
            overwrite_confirmation_window=5*60,
            overwrite_submission_window=25*60
        )
        for op
        in operations.read_operations(INPUT_DIR + 'mesh_operations.json', dependencies=RegistryCache(None).external_retriever)
        # in operations.read_operations(INPUT_DIR + 'castelldefels.corusxuam.v9.C.1.traffic.json', dependencies=RegistryCache(None).external_retriever)
    ]

    sim_missions: list[Mission] = [*missions[:50]]

    simulation = DcbSimulator(
        sim_missions,
        logger=logger
    )

    while simulation.run_step(
            batch_time_interval_seconds=5 * 60,
            precision_seconds=30,
            max_compute_time_seconds=30,
    ):
        simulation.apply_parameters_to_not_submitted_missions()

        pass

    to_export = []

    for m in sim_missions:
        delay = simulation.get_mission_delay(m)
        if delay is not None:
            operation: Operation = m.user_object
            operation.request = operation.request + datetime.timedelta(seconds=delay)
            to_export.append(operation.to_json({}))

    with open(OUTPUT_DIR + 'exported_simulation.json', 'w') as file:
        json.dump(to_export, file)

    logger.info(f"Accepted: {len(simulation.accepted_partake_missions)}")
    logger.info(f"Rejected: {len(simulation.rejected_partake_missions)}")


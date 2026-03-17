# Copyright 2026 Enactic, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""dora-rs node that mimics classifier for testing."""

import dora
import pyarrow as pa
import random


def main():
    """Mimics classifier."""
    phase_names = [
        "Outside",
        "Picking",
        "Inside",
        "Rescue",
        "Dropped",
    ]

    node = dora.Node()
    for event in node:
        if event["type"] != "INPUT":
            continue

        # Main process
        event_id = event["id"]
        if event_id != "observation":
            # Run with the interval of the observation
            continue

        phase_name = random.choice(phase_names)
        success = phase_name == phase_names[0]
        phase_id = phase_names.index(phase_name)
        confidence = 0.9
        status = "SUCCESS" if success else "FAILURE"

        # Send outputs
        # - phase      Int32: 0=Outside, 1=Picking, 2=Inside, 3=Rescue, 4=Dropped
        # - phase_name String: "Outside", "Picking", "Inside", "Rescue", "Dropped"
        # - confidence Float32: Model confidence [0.0-1.0]
        # - success    Boolean: Task completed successfully
        # - status     String: "SUCCESS" or "FAILURE"
        arrays = []
        names = []
        arrays.append(pa.array([phase_id], type=pa.int32()))
        names.append("phase")
        arrays.append(pa.array([phase_name], type=pa.string()))
        names.append("phase_name")
        arrays.append(pa.array([confidence], type=pa.float32()))
        names.append("confidence")
        arrays.append(pa.array([success], type=pa.bool_()))
        names.append("success")
        arrays.append(pa.array([status], type=pa.string()))
        names.append("status")
        node.send_output("result", pa.StructArray.from_arrays(arrays, names))


if __name__ == "__main__":
    main()

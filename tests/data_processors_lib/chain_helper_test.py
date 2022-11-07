from __future__ import annotations

import pandas as pd

from src.eventstream.eventstream import Eventstream
from src.eventstream.schema import EventstreamSchema, RawDataSchema


class TestChainHelper:
    def test_chain_helper(self) -> None:
        source_df = pd.DataFrame(
            [
                [1, "event1", "2022-01-01 00:00:00"],
                [1, "event2", "2022-01-01 00:00:01"],
                [1, "event3", "2022-01-01 00:00:02"],
                [2, "event4", "2022-01-02 00:00:00"],
            ],
            columns=["user_id", "event", "timestamp"],
        )

        correct_result_columns = ["user_id", "event_name", "event_type", "event_timestamp"]
        correct_result = pd.DataFrame(
            [
                [1, "start", "start", "2022-01-01 00:00:00"],
                [1, "new_user", "new_user", "2022-01-01 00:00:00"],
                [1, "event1", "raw", "2022-01-01 00:00:00"],
                [1, "event2", "raw", "2022-01-01 00:00:01"],
                [1, "event3", "raw", "2022-01-01 00:00:02"],
                [1, "end", "end", "2022-01-01 00:00:02"],
                [2, "start", "start", "2022-01-02 00:00:00"],
                [2, "new_user", "new_user", "2022-01-02 00:00:00"],
                [2, "event4", "raw", "2022-01-02 00:00:00"],
                [2, "end", "end", "2022-01-02 00:00:00"],
            ],
            columns=correct_result_columns,
        )

        stream = Eventstream(
            raw_data_schema=RawDataSchema(event_name="event", event_timestamp="timestamp", user_id="user_id"),
            raw_data=source_df,
            schema=EventstreamSchema(),
        )

        result = stream.add_start_end().add_new_users(new_users_list="all")
        result_df = result.to_dataframe()[correct_result_columns].reset_index(drop=True)

        assert result_df.compare(correct_result).shape == (0, 0)

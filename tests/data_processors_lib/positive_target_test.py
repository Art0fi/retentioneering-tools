from __future__ import annotations

import pandas as pd

from retentioneering.data_processors_lib import PositiveTarget, PositiveTargetParams
from retentioneering.eventstream.eventstream import Eventstream
from retentioneering.eventstream.schema import RawDataSchema
from retentioneering.eventstream.types import EventstreamType
from tests.data_processors_lib.common import ApplyTestBase, GraphTestBase
from tests.data_processors_lib.fixtures.positive_target_corr import (
    apply__1_event_corr,
    apply__2_events_corr,
    apply__custom_func_corr,
    graph__1_event_corr,
    graph__2_events_corr,
    graph__custom_func_corr,
)
from tests.data_processors_lib.fixtures.positive_target_input import test_stream


class TestPositiveTarget(ApplyTestBase):

    _Processor = PositiveTarget
    _source_df = pd.DataFrame(
        [
            [1, "path_start", "path_start", "2022-01-01 00:01:00"],
            [1, "event1", "raw", "2022-01-01 00:01:00"],
            [1, "event2", "raw", "2022-01-01 00:01:02"],
            [1, "event1", "raw", "2022-01-01 00:02:00"],
            [1, "event1", "raw", "2022-01-01 00:03:00"],
            [1, "event1", "synthetic", "2022-01-01 00:03:00"],
            [1, "session_start", "session_start", "2022-01-01 00:03:30"],
            [1, "event3", "raw", "2022-01-01 00:03:30"],
            [1, "event1", "raw", "2022-01-01 00:04:00"],
            [1, "event3", "raw", "2022-01-01 00:04:30"],
            [1, "event1", "raw", "2022-01-01 00:05:00"],
            [2, "event1", "raw", "2022-01-02 00:00:00"],
            [2, "event3", "raw", "2022-01-02 00:00:05"],
            [2, "event2", "raw", "2022-01-02 00:01:05"],
            [2, "path_end", "path_end", "2022-01-02 00:01:05"],
            [3, "event1", "raw", "2022-01-02 00:01:10"],
            [3, "event1", "raw", "2022-01-02 00:02:05"],
            [3, "event4", "raw", "2022-01-02 00:03:05"],
            [3, "path_end", "path_end", "2022-01-02 00:03:05"],
        ],
        columns=["user_id", "event", "event_type", "timestamp"],
    )
    _raw_data_schema = RawDataSchema(
        user_id="user_id",
        event_name="event",
        event_type="event_type",
        event_timestamp="timestamp",
    )

    def test_positive_target_apply__1_event(self, apply__1_event_corr):
        actual = self._apply(
            PositiveTargetParams(
                positive_target_events=["event3"],
            )
        )
        expected = apply__1_event_corr
        assert pd.testing.assert_frame_equal(actual[expected.columns], expected) is None

    def test_positive_target_apply__2_events(self, apply__2_events_corr):
        actual = self._apply(
            PositiveTargetParams(
                positive_target_events=["event3", "event2"],
            )
        )
        expected = apply__2_events_corr
        assert pd.testing.assert_frame_equal(actual[expected.columns], expected) is None

    def test_positive_target_apply__custom_func(self, apply__custom_func_corr):
        def custom_func(eventstream: EventstreamType, events: list[str]) -> pd.DataFrame:
            user_col = eventstream.schema.user_id
            time_col = eventstream.schema.event_timestamp
            event_col = eventstream.schema.event_name
            df = eventstream.to_dataframe()
            events_index_1 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmin()  # type: ignore
            events_index_2 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmax()  # type: ignore
            events_index = pd.concat([events_index_1, events_index_2], axis=0)

            return df.loc[events_index]

        actual = self._apply(PositiveTargetParams(positive_target_events=["event1"], func=custom_func))
        expected = apply__custom_func_corr

        assert pd.testing.assert_frame_equal(actual[expected.columns], expected) is None


class TestPositiveTargetGraph(GraphTestBase):
    _Processor = PositiveTarget
    _source_df = pd.DataFrame(
        [
            [1, "path_start", "path_start", "2022-01-01 00:01:00"],
            [1, "event1", "raw", "2022-01-01 00:01:00"],
            [1, "event2", "raw", "2022-01-01 00:01:02"],
            [1, "event1", "raw", "2022-01-01 00:02:00"],
            [1, "event1", "raw", "2022-01-01 00:03:00"],
            [1, "event1", "synthetic", "2022-01-01 00:03:00"],
            [1, "session_start", "session_start", "2022-01-01 00:03:30"],
            [1, "event3", "raw", "2022-01-01 00:03:30"],
            [1, "event1", "raw", "2022-01-01 00:04:00"],
            [1, "event3", "raw", "2022-01-01 00:04:30"],
            [1, "event1", "raw", "2022-01-01 00:05:00"],
            [2, "event1", "raw", "2022-01-02 00:00:00"],
            [2, "event3", "raw", "2022-01-02 00:00:05"],
            [2, "event2", "raw", "2022-01-02 00:01:05"],
            [2, "path_end", "path_end", "2022-01-02 00:01:05"],
            [3, "event1", "raw", "2022-01-02 00:01:10"],
            [3, "event1", "raw", "2022-01-02 00:02:05"],
            [3, "event4", "raw", "2022-01-02 00:03:05"],
            [3, "path_end", "path_end", "2022-01-02 00:03:05"],
        ],
        columns=["user_id", "event", "event_type", "timestamp"],
    )
    _raw_data_schema = RawDataSchema(
        user_id="user_id",
        event_name="event",
        event_type="event_type",
        event_timestamp="timestamp",
    )

    def test_positive_target_graph__1_event(self, graph__1_event_corr):
        actual = self._apply(
            PositiveTargetParams(
                positive_target_events=["event3"],
            )
        )
        expected = graph__1_event_corr
        assert pd.testing.assert_frame_equal(actual[expected.columns], expected) is None

    def test_positive_target_graph__2_events(self, graph__2_events_corr):
        actual = self._apply(
            PositiveTargetParams(
                positive_target_events=["event3", "event2"],
            )
        )
        expected = graph__2_events_corr

        assert pd.testing.assert_frame_equal(actual[expected.columns], expected) is None

    def test_positive_target_graph__custom_func(self, graph__custom_func_corr) -> bool:
        def custom_func(eventstream: EventstreamType, events: list[str]) -> pd.DataFrame:
            user_col = eventstream.schema.user_id
            time_col = eventstream.schema.event_timestamp
            event_col = eventstream.schema.event_name
            df = eventstream.to_dataframe()
            events_index_1 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmin()  # type: ignore
            events_index_2 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmax()  # type: ignore
            events_index = pd.concat([events_index_1, events_index_2], axis=0)

            return df.loc[events_index]

        correct_result = graph__custom_func_corr
        result = self._apply(PositiveTargetParams(positive_target_events=["event1"], func=custom_func))

        assert pd.testing.assert_frame_equal(result[correct_result.columns], correct_result) is None


class TestPositiveTargetHelper:
    def test_positive_target_graph__1_event(self, test_stream, graph__1_event_corr):
        source = test_stream
        correct_result = graph__1_event_corr
        result = source.positive_target(positive_target_events=["event3"])
        result_df = result.to_dataframe()[correct_result.columns].reset_index(drop=True)

        assert pd.testing.assert_frame_equal(result_df, correct_result) is None

    def test_positive_target_graph__2_events(self, test_stream, graph__2_events_corr):
        source = test_stream
        correct_result = graph__2_events_corr
        result = source.positive_target(positive_target_events=["event3", "event2"])
        result_df = result.to_dataframe()[correct_result.columns].reset_index(drop=True)

        assert pd.testing.assert_frame_equal(result_df, correct_result) is None

    def test_positive_target_graph__custom_func(self, test_stream, graph__custom_func_corr):
        def custom_func(eventstream: EventstreamType, events: list[str]) -> pd.DataFrame:
            user_col = eventstream.schema.user_id
            time_col = eventstream.schema.event_timestamp
            event_col = eventstream.schema.event_name
            df = eventstream.to_dataframe()
            events_index_1 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmin()  # type: ignore
            events_index_2 = df[df[event_col].isin(events)].groupby(user_col)[time_col].idxmax()  # type: ignore
            events_index = pd.concat([events_index_1, events_index_2], axis=0)
            result = df.loc[events_index]
            return result

        source = test_stream
        correct_result = graph__custom_func_corr
        actual = source.positive_target(positive_target_events=["event1"], func=custom_func)
        result_df = actual.to_dataframe()[correct_result.columns].reset_index(drop=True)

        assert pd.testing.assert_frame_equal(result_df, correct_result) is None

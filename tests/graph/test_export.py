import pandas as pd

from retentioneering.data_processors_lib import (
    CollapseLoops,
    CollapseLoopsParams,
    DeleteUsersByPathLength,
    DeleteUsersByPathLengthParams,
    LostUsersEvents,
    LostUsersParams,
    NegativeTarget,
    NegativeTargetParams,
    NewUsersEvents,
    NewUsersParams,
    PositiveTarget,
    PositiveTargetParams,
    SplitSessions,
    SplitSessionsParams,
    StartEndEvents,
    StartEndEventsParams,
    TruncatedEvents,
    TruncatedEventsParams,
    TruncatePath,
    TruncatePathParams,
)
from retentioneering.eventstream.eventstream import Eventstream
from retentioneering.eventstream.schema import RawDataSchema
from retentioneering.preprocessing_graph.nodes import EventsNode
from retentioneering.preprocessing_graph.preprocessing_graph import PreprocessingGraph


class TestPreprocessingGraphExportImport:
    def create_graph(self) -> PreprocessingGraph:
        source_df = pd.DataFrame(
            [
                {"event_name": "pageview", "event_timestamp": "2021-10-26 12:00", "user_id": "1"},
                {"event_name": "cart_btn_click", "event_timestamp": "2021-10-26 12:02", "user_id": "1"},
                {"event_name": "pageview", "event_timestamp": "2021-10-26 12:03", "user_id": "1"},
                {"event_name": "trash_event", "event_timestamp": "2021-10-26 12:03", "user_id": "1"},
                {"event_name": "exit_btn_click", "event_timestamp": "2021-10-26 12:04", "user_id": "2"},
                {"event_name": "plus_icon_click", "event_timestamp": "2021-10-26 12:05", "user_id": "1"},
            ]
        )

        source = Eventstream(
            raw_data_schema=RawDataSchema(
                event_name="event_name", event_timestamp="event_timestamp", user_id="user_id"
            ),
            raw_data=source_df,
        )
        graph = PreprocessingGraph(source)

        return graph

    def test_start_end__export(self) -> None:
        graph = self.create_graph()
        node = EventsNode(processor=StartEndEvents(params=StartEndEventsParams(**{})))
        node.description = "description"
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]

        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {"values": {}, "name": "StartEndEvents"},
                    "description": "description",
                },
            ],
        } == export_data

    def test_start_end__import(self) -> None:
        graph = self.create_graph()

        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "a911d6de-48a9-4898-8d4f-c123efc84498"},
                    {
                        "name": "EventsNode",
                        "pk": "81e5ead2-c0ed-43c5-a522-9d2484a1607e",
                        "processor": {"values": {}, "name": "StartEndEvents"},
                    },
                ],
                "links": [
                    {"source": "a911d6de-48a9-4898-8d4f-c123efc84498", "target": "81e5ead2-c0ed-43c5-a522-9d2484a1607e"}
                ],
            }
        )

        export_data = graph.export(payload={})

        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]

        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {"name": "EventsNode", "processor": {"values": {}, "name": "StartEndEvents"}},
            ],
        } == export_data

    def test_truncated__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(
            processor=TruncatedEvents(params=TruncatedEventsParams(left_cutoff=(1, "h"), right_cutoff=(1, "h")))
        )
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "TruncatedEvents",
                        "values": {"left_cutoff": (1.0, "h"), "right_cutoff": (1.0, "h")},
                    },
                },
            ],
        } == export_data

    def test_truncated__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "values": {"left_cutoff": (1.0, "h"), "right_cutoff": (1.0, "h")},
                            "name": "TruncatedEvents",
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "TruncatedEvents",
                        "values": {"left_cutoff": (1.0, "h"), "right_cutoff": (1.0, "h")},
                    },
                },
            ],
        } == export_data

    def test_new_users__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=NewUsersEvents(params=NewUsersParams(new_users_list=[2])))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "NewUsersEvents",
                        "values": {"new_users_list": [2]},
                    },
                },
            ],
        } == export_data

    def test_new_users__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "NewUsersEvents",
                            "values": {"new_users_list": [2]},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "NewUsersEvents",
                        "values": {"new_users_list": [2]},
                    },
                },
            ],
        } == export_data

    def test_collapse_loops__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=CollapseLoops(params=CollapseLoopsParams(**{"suffix": "count", "time_agg": "min"})))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "CollapseLoops",
                        "values": {"suffix": "count", "time_agg": "min"},
                    },
                },
            ],
        } == export_data

    def test_collapse_loops__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "CollapseLoops",
                            "values": {"suffix": "count", "time_agg": "min"},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "CollapseLoops",
                        "values": {"suffix": "count", "time_agg": "min"},
                    },
                },
            ],
        } == export_data

    def test_delete_user__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=DeleteUsersByPathLength(params=DeleteUsersByPathLengthParams(min_time=(1.5, "m"))))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "DeleteUsersByPathLength",
                        "values": {"min_time": (1.5, "m"), "min_steps": None},
                    },
                },
            ],
        } == export_data

    def test_delete_user__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "DeleteUsersByPathLength",
                            "values": {"min_time": (1.5, "m")},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "DeleteUsersByPathLength",
                        "values": {"min_time": (1.5, "m"), "min_steps": None},
                    },
                },
            ],
        } == export_data

    def test_lost_users__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=LostUsersEvents(params=LostUsersParams(lost_users_list=None, timeout=(4, "h"))))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "LostUsersEvents",
                        "values": {"lost_users_list": None, "timeout": (4.0, "h")},
                    },
                },
            ],
        } == export_data

    def test_lost_users__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "LostUsersEvents",
                            "values": {"lost_users_list": None, "timeout": (4.0, "h")},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "LostUsersEvents",
                        "values": {"lost_users_list": None, "timeout": (4.0, "h")},
                    },
                },
            ],
        } == export_data

    def test_negative_target__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=NegativeTarget(params=NegativeTargetParams(**{"targets": ["event3", "event2"]})))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "NegativeTarget",
                        "values": {
                            "targets": ["event3", "event2"],
                            "func": "def _default_func(eventstream: EventstreamType, "
                            "targets: List[str]) -> pd.DataFrame:\n"
                            '    """\n'
                            "    Filter rows with target events from the input eventstream.\n"
                            "\n"
                            "    Parameters\n"
                            "    ----------\n"
                            "    eventstream : Eventstream\n"
                            "        Source eventstream or output from previous nodes.\n"
                            "\n"
                            "    targets : list of str\n"
                            "        Each event from that list is associated with the bad result (scenario)\n"
                            "        of user's behaviour (experience) in the product.\n"
                            "        If there are several target events in user path - the event with minimum "
                            "timestamp is taken.\n"
                            "\n"
                            "    Returns\n"
                            "    -------\n"
                            "    pd.DataFrame\n"
                            "        Filtered DataFrame with targets and its timestamps.\n"
                            '    """\n'
                            "    user_col = eventstream.schema.user_id\n"
                            "    time_col = eventstream.schema.event_timestamp\n"
                            "    event_col = eventstream.schema.event_name\n"
                            "    df = eventstream.to_dataframe()\n"
                            "\n"
                            "    targets_index = "
                            "df[df[event_col].isin(targets)]."
                            "groupby(user_col)[time_col].idxmin()  # type: ignore\n"
                            "\n"
                            "    return df.loc[targets_index]  # type: ignore\n",
                        },
                    },
                },
            ],
        } == export_data

    def test_negative_target__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "NegativeTarget",
                            "values": {
                                "targets": ["event3", "event2"],
                                "func": "def _default_func(eventstream, "
                                "targets) -> pd.DataFrame:\n"
                                "    user_col = eventstream.schema.user_id\n"
                                "    time_col = eventstream.schema.event_timestamp\n"
                                "    event_col = eventstream.schema.event_name\n"
                                "    df = eventstream.to_dataframe()\n"
                                "\n"
                                "    targets_index = "
                                "df[df[event_col].isin(targets)].groupby"
                                "(user_col)[time_col].idxmin()\n"
                                "\n"
                                "    return df.iloc[targets_index]",
                            },
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "NegativeTarget",
                        "values": {
                            "targets": ["event3", "event2"],
                            "func": "def _default_func(eventstream, "
                            "targets) -> pd.DataFrame:\n"
                            "    user_col = eventstream.schema.user_id\n"
                            "    time_col = eventstream.schema.event_timestamp\n"
                            "    event_col = eventstream.schema.event_name\n"
                            "    df = eventstream.to_dataframe()\n"
                            "\n"
                            "    targets_index = "
                            "df[df[event_col].isin(targets)].groupby"
                            "(user_col)[time_col].idxmin()\n"
                            "\n"
                            "    return df.iloc[targets_index]",
                        },
                    },
                },
            ],
        } == export_data

    def test_positive_events__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(processor=PositiveTarget(params=PositiveTargetParams(**{"targets": ["event3", "event2"]})))
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "PositiveTarget",
                        "values": {
                            "targets": ["event3", "event2"],
                            "func": "def _default_func("
                            "eventstream: EventstreamType, targets: list[str]) "
                            "-> pd.DataFrame:\n"
                            '    """\n'
                            "    Filter rows with target events from the input eventstream.\n"
                            "\n"
                            "    Parameters\n"
                            "    ----------\n"
                            "    eventstream : Eventstream\n"
                            "        Source eventstream or output from previous nodes.\n"
                            "\n"
                            "    targets : list of str\n"
                            "        Condition for eventstream filtering.\n"
                            "        Each event from that list is associated with a conversion goal "
                            "of the user behaviour in the product.\n"
                            "        If there are several target events in user path - the event with minimum "
                            "timestamp is taken.\n"
                            "\n"
                            "    Returns\n"
                            "    -------\n"
                            "    pd.DataFrame\n"
                            "        Filtered DataFrame with targets and its timestamps.\n"
                            '    """\n'
                            "    user_col = eventstream.schema.user_id\n"
                            "    time_col = eventstream.schema.event_timestamp\n"
                            "    event_col = eventstream.schema.event_name\n"
                            "    df = eventstream.to_dataframe()\n\n    "
                            "targets_index = "
                            "df[df[event_col].isin(targets)]."
                            "groupby(user_col)[time_col].idxmin()  # type: ignore\n"
                            "\n"
                            "    return df.loc[targets_index]  # type: ignore\n",
                        },
                    },
                },
            ],
        } == export_data

    def test_positive_events__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "PositiveTarget",
                            "values": {"targets": ["event3", "event2"]},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "PositiveTarget",
                        "values": {
                            "targets": ["event3", "event2"],
                            "func": "def _default_func("
                            "eventstream: EventstreamType, targets: list[str]) "
                            "-> pd.DataFrame:\n"
                            '    """\n'
                            "    Filter rows with target events from the input eventstream.\n"
                            "\n"
                            "    Parameters\n"
                            "    ----------\n"
                            "    eventstream : Eventstream\n"
                            "        Source eventstream or output from previous nodes.\n"
                            "\n"
                            "    targets : list of str\n"
                            "        Condition for eventstream filtering.\n"
                            "        Each event from that list is associated with a conversion goal "
                            "of the user behaviour in the product.\n"
                            "        If there are several target events in user path - the event with minimum "
                            "timestamp is taken.\n"
                            "\n"
                            "    Returns\n"
                            "    -------\n"
                            "    pd.DataFrame\n"
                            "        Filtered DataFrame with targets and its timestamps.\n"
                            '    """\n'
                            "    user_col = eventstream.schema.user_id\n"
                            "    time_col = eventstream.schema.event_timestamp\n"
                            "    event_col = eventstream.schema.event_name\n"
                            "    df = eventstream.to_dataframe()\n\n    "
                            "targets_index = "
                            "df[df[event_col].isin(targets)]."
                            "groupby(user_col)[time_col].idxmin()  # type: ignore\n"
                            "\n"
                            "    return df.loc[targets_index]  # type: ignore\n",
                        },
                    },
                },
            ],
        } == export_data

    def test_split_sesssion__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(
            processor=SplitSessions(
                params=SplitSessionsParams(timeout=(30, "m"), session_col="session_id", mark_truncated=True)
            )
        )
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "SplitSessions",
                        "values": {"timeout": (30.0, "m"), "session_col": "session_id", "mark_truncated": True},
                    },
                },
            ],
        } == export_data

    def test_split_sesssion__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "SplitSessions",
                            "values": {
                                "timeout": (30.0, "m"),
                                "session_col": "session_id",
                                "mark_truncated": True,
                            },
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "SplitSessions",
                        "values": {"timeout": (30.0, "m"), "session_col": "session_id", "mark_truncated": True},
                    },
                },
            ],
        } == export_data

    def test_truncated_path__export(self) -> None:
        graph = self.create_graph()

        node = EventsNode(
            processor=TruncatePath(
                params=TruncatePathParams(drop_before="event3", occurrence_before="last", shift_before=2)
            )
        )
        graph.add_node(node=node, parents=[graph.root])

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "TruncatePath",
                        "values": {
                            "drop_before": "event3",
                            "occurrence_before": "last",
                            "shift_before": 2,
                            "drop_after": None,
                            "occurrence_after": "first",
                            "shift_after": 0,
                        },
                    },
                },
            ],
        } == export_data

    def test_truncated_path__import(self) -> None:
        graph = self.create_graph()
        graph._set_graph(
            payload={
                "directed": True,
                "nodes": [
                    {"name": "SourceNode", "pk": "0ad30844-66f8-47db-b5f0-221679296fe7"},
                    {
                        "name": "EventsNode",
                        "pk": "f45f7390-d2b4-4414-bcd2-94532ede375d",
                        "processor": {
                            "name": "TruncatePath",
                            "values": {"drop_before": "event3", "occurrence_before": "last", "shift_before": 2},
                        },
                    },
                ],
                "links": [
                    {"source": "0ad30844-66f8-47db-b5f0-221679296fe7", "target": "f45f7390-d2b4-4414-bcd2-94532ede375d"}
                ],
            }
        )

        export_data = graph.export(payload={})
        assert 1 == len(export_data["links"])
        del export_data["links"]
        del export_data["nodes"][0]["pk"]
        del export_data["nodes"][1]["pk"]
        assert {
            "directed": True,
            "nodes": [
                {"name": "SourceNode"},
                {
                    "name": "EventsNode",
                    "processor": {
                        "name": "TruncatePath",
                        "values": {
                            "drop_before": "event3",
                            "occurrence_before": "last",
                            "shift_before": 2,
                            "drop_after": None,
                            "occurrence_after": "first",
                            "shift_after": 0,
                        },
                    },
                },
            ],
        } == export_data

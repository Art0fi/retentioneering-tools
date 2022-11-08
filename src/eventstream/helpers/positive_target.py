from __future__ import annotations

from typing import Callable, List, Optional

from ..types import EventstreamType


class PositiveTargetHelperMixin:
    def positive_target(
        self, positive_target_events: List[str], positive_function: Optional[Callable] = None
    ) -> EventstreamType:

        # avoid circular import
        from src.data_processors_lib.rete import PositiveTarget, PositiveTargetParams
        from src.graph.nodes import EventsNode
        from src.graph.p_graph import PGraph

        p = PGraph(source_stream=self)  # type: ignore

        params: dict[str, list[str] | Callable] = {"positive_target_events": positive_target_events}
        if positive_function:
            params["positive_function"] = positive_function

        node = EventsNode(processor=PositiveTarget(params=PositiveTargetParams(**params)))  # type: ignore
        p.add_node(node=node, parents=[p.root])
        result = p.combine(node)
        del p
        return result

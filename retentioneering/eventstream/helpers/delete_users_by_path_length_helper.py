from __future__ import annotations

from typing import Tuple

from retentioneering.constants import DATETIME_UNITS

from ..types import EventstreamType


class DeleteUsersByPathLengthHelperMixin:
    def delete_users(
        self, events_num: int | None = None, cutoff: Tuple[float, DATETIME_UNITS] | None = None
    ) -> EventstreamType:
        """
        Method of ``Eventstream Class`` which deletes entire user's paths if they are shorter than the specified
        number of events or cut_off.

        Returns
        -------
        Eventstream
             Input ``eventstream`` with deleted short user's paths.

        Notes
        -----
        See parameters and details of dataprocessor functionality
        :py:class:`.DeleteUsersByPathLength`
        """

        # avoid circular import
        from retentioneering.data_processors_lib import (
            DeleteUsersByPathLength,
            DeleteUsersByPathLengthParams,
        )
        from retentioneering.graph.nodes import EventsNode
        from retentioneering.graph.p_graph import PGraph

        p = PGraph(source_stream=self)  # type: ignore

        node = EventsNode(
            processor=DeleteUsersByPathLength(
                params=DeleteUsersByPathLengthParams(events_num=events_num, cutoff=cutoff)  # type: ignore
            )
        )
        p.add_node(node=node, parents=[p.root])
        result = p.combine(node)
        del p
        return result

from __future__ import annotations

import logging
from typing import Callable, Any, List

from pandas import DataFrame

from src.data_processor.data_processor import DataProcessor
from src.eventstream.eventstream import Eventstream
from src.eventstream.schema import EventstreamSchema
from src.params_model import ParamsModel

log = logging.getLogger(__name__)

EventstreamFilter = Callable[[DataFrame, EventstreamSchema], Any]


class CutPathAfterEventParams(ParamsModel):
    cutoff_events: List[str]
    cut_shift: int
    min_cjm: int


class CutPathAfterEvent(DataProcessor):
    params: CutPathAfterEventParams

    def __init__(self, params: CutPathAfterEventParams = None):
        super().__init__(params=params)

    def apply(self, eventstream: Eventstream) -> Eventstream:
        user_col = eventstream.schema.user_id
        time_col = eventstream.schema.event_timestamp
        type_col = eventstream.schema.event_type
        event_col = eventstream.schema.event_name
        id_col = eventstream.schema.event_id

        cutoff_events = self.params.cutoff_events
        min_cjm = self.params.min_cjm
        cut_shift = self.params.cut_shift

        df = eventstream.to_dataframe()

        df['_point'] = 0
        df.loc[df[event_col].isin(cutoff_events), '_point'] = 1
        df['_point'] = df.groupby([user_col, time_col])._point.transform(max)
        df['_cumsum'] = df.groupby([user_col])._point.cumsum()

        df['num_groups'] = df.groupby([user_col])[time_col].transform(lambda x: x.diff().ne(0).astype(int).cumsum())
        df['num_groups'] = df.groupby([user_col])[time_col].transform(
            lambda x: x.diff().dt.total_seconds().ne(0).cumsum())

        df['find_1'] = df.groupby([user_col, 'num_groups'])['_cumsum'].transform(lambda x: x.eq(1).any().astype(int))

        mask = ((df['_cumsum'] == 0) | ((df['_cumsum'] > 0) & (df['_point'] == 1) & (df['find_1'] == 1)))

        df_cut = df[mask]
        ids_to_del = df[~mask][id_col].to_list()
        df_cut['rw_cumsum'] = df_cut.loc[::-1].groupby([user_col])[time_col].transform(
            lambda x: x.diff().ne(0).astype(int).cumsum())
        if cut_shift > 0:
            ids_to_del = ids_to_del + df_cut[df_cut['rw_cumsum'] <= cut_shift][id_col].to_list()
            df_cut = df_cut[df_cut['rw_cumsum'] > cut_shift]

        if min_cjm > 0:
            df_cut = df_cut.groupby([user_col])[['num_groups']].max().reset_index()
            users_to_del = df_cut[df_cut['num_groups'] < min_cjm][user_col].to_list()
            # TODO dasha - после fix поменять на soft
            df.query(f'{user_col}.isin({users_to_del})', engine='python', inplace=True)

        # TODO dasha - после fix поменять на soft
        # df.query(f'{id_col}.isin({ids_to_del})', engine='python', inplace=True)
        df = df.loc[df[id_col].apply(lambda x: x in ids_to_del)]
        df['ref'] = df[eventstream.schema.event_id]

        eventstream = Eventstream(
            raw_data=df,
            raw_data_schema=eventstream.schema.to_raw_data_schema(),
            relations=[{"raw_col": "ref", "evenstream": eventstream}],
        )
        return eventstream

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 17:44
@Author  : alexanderwu
@File    : __init__.py
"""
from enum import Enum

from metagpt.actions.action import Action
from metagpt.actions.action_output import ActionOutput
from metagpt.actions.add_requirement import BossRequirement
from metagpt.actions.create_personas import CreatePersonas
from metagpt.actions.create_needs import CreateNeeds
from metagpt.actions.synthesise_need import SynthesiseNeed
from metagpt.actions.innovate import CreateInitiatives
from metagpt.actions.solutions import CreateSolutions
from metagpt.actions.feasibility import AnalyseFeasibility
from metagpt.actions.marketability import AnalyseMarketViability
from metagpt.actions.create_journey_maps import CreateJourneyMaps

class ActionType(Enum):
    """All types of Actions, used for indexing."""

    ADD_REQUIREMENT = BossRequirement
    CREATE_PERSONAS = CreatePersonas
    CREATE_NEEDS = CreateNeeds
    SYNTHESISE_NEED = SynthesiseNeed
    CREATE_INTIATIVES = CreateInitiatives
    CREATE_SOLUTIONS = CreateSolutions
    ANALYSE_FEASIBILITY = AnalyseFeasibility
    ANALYSE_MARKET_VIABILITY = AnalyseMarketViability
    CREATE_JOURNEY_MAPS = CreateJourneyMaps


__all__ = [
    "ActionType",
    "Action",
    "ActionOutput",
]

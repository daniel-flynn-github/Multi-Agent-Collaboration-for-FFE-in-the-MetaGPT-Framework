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
from data.MetaGPT.metagpt.actions.ideas import CreateIdeas
from metagpt.actions.feasibility import AnalyseFeasibility
from metagpt.actions.marketability import AnalyseMarketViability
from metagpt.actions.create_journey_maps import CreateJourneyMaps
from metagpt.actions.summarise import Summarise

class ActionType(Enum):
    """All types of Actions, used for indexing."""

    ADD_REQUIREMENT = BossRequirement
    CREATE_PERSONAS = CreatePersonas
    CREATE_NEEDS = CreateNeeds
    SYNTHESISE_NEED = SynthesiseNeed
    CREATE_INTIATIVES = CreateInitiatives
    CREATE_IDEAS = CreateIdeas
    ANALYSE_FEASIBILITY = AnalyseFeasibility
    ANALYSE_MARKET_VIABILITY = AnalyseMarketViability
    CREATE_JOURNEY_MAPS = CreateJourneyMaps
    SUMMARISE = Summarise


__all__ = [
    "ActionType",
    "Action",
    "ActionOutput",
]

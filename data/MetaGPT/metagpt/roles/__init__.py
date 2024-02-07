#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2023/5/11 14:43
@Author  : alexanderwu
@File    : __init__.py
"""

from metagpt.roles.role import Role
from metagpt.roles.user_researcher import UserResearcher
from metagpt.roles.needs_analyst import NeedsAnalyst
from metagpt.roles.design_manager import DesignManager
from metagpt.roles.innovator import Innovator
from data.MetaGPT.metagpt.roles.innovator import Innovator
from metagpt.roles.feasability_analyst import FeasibilityAnalyst
from metagpt.roles.experience_analyst import ExperienceAnalyst
from metagpt.roles.demonstator import Demonstrator


__all__ = [
    "Role",
    "UserResearcher",
    "NeedsAnalyst",
    "DesignManager",
    "Innovator",
    "Innovator",
    "FeasibilityAnalyst",
    "ExperienceAnalyst",
    "Demonstrator",
]

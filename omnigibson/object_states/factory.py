import networkx as nx

from omnigibson.object_states import *

_ABILITY_TO_STATE_MAPPING = {
    "attachable": [AttachedTo],
    "burnable": [Burnt],
    "particleApplier": [ParticleApplier],
    "particleRemover": [ParticleRemover],
    "particleSource": [ParticleSource],
    "particleSink": [ParticleSink],
    "coldSource": [HeatSourceOrSink],
    "cookable": [Cooked],
    "coverable": [Covered],
    "freezable": [Frozen],
    "heatable": [Heated],
    "heatSource": [HeatSourceOrSink],
    "meltable": [],
    "openable": [Open],
    "flammable": [OnFire],
    "saturable": [Saturated],
    "sliceable": [],
    "slicer": [],
    "toggleable": [ToggledOn],
    "fillable": [Filled, Contains],
    "foldable": [Folded],
    "unfoldable": [Unfolded],
}

_DEFAULT_STATE_SET = frozenset(
    [
        Inside,
        NextTo,
        OnTop,
        Overlaid,
        Touching,
        Under,
        Covered,
    ]
)

_FIRE_STATE_SET = frozenset(
    [
        HeatSourceOrSink,
        OnFire,
    ]
)

_STEAM_STATE_SET = frozenset(
    [
        Heated,
    ]
)

_TEXTURE_CHANGE_STATE_SET = frozenset(
    [
        Frozen,
        Burnt,
        Cooked,
        Saturated,
        ToggledOn,
    ]
)

_VISUAL_STATE_SET = frozenset(_FIRE_STATE_SET | _STEAM_STATE_SET | _TEXTURE_CHANGE_STATE_SET)

_TEXTURE_CHANGE_PRIORITY = {
    Frozen: 4,
    Burnt: 3,
    Cooked: 2,
    Saturated: 1,
    ToggledOn: 0,
}


def get_fire_states():
    return _FIRE_STATE_SET


def get_steam_states():
    return _STEAM_STATE_SET


def get_texture_change_states():
    return _TEXTURE_CHANGE_STATE_SET


def get_texture_change_priority():
    return _TEXTURE_CHANGE_PRIORITY


def get_visual_states():
    return _VISUAL_STATE_SET


def get_default_states():
    return _DEFAULT_STATE_SET


def get_state_name(state):
    # Get the name of the class.
    return state.__name__


def get_states_for_ability(ability):
    if ability not in _ABILITY_TO_STATE_MAPPING:
        return []
    return _ABILITY_TO_STATE_MAPPING[ability]


def get_state_dependency_graph():
    """
    Returns:
        nx.DiGraph: State dependency graph of supported object states
    """
    dependencies = {state: state.get_dependencies() + state.get_optional_dependencies()
                    for state in REGISTERED_OBJECT_STATES.values()}
    return nx.DiGraph(dependencies)


def get_states_by_dependency_order():
    """
    Returns:
        list: all states in topological order of dependency
    """
    return list(reversed(list(nx.algorithms.topological_sort(get_state_dependency_graph()))))

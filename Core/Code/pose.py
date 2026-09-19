"""
From bone transforms to skinning matrices.

A model's vertices are stored in its bind pose. To draw it in any other pose
each bone needs one matrix that takes a bind-pose point into that bone's
space (`pose_to_bone`, stored in the .mdl) and then out again through the
bone's new world transform. That product is what the vertex shader multiplies
by, weighted per vertex.

Source Filmmaker never shows the bind pose: a game model in a session carries
its own bone transforms (local to the parent bone, in the model's bone order),
and that is what this turns into matrices. Some models store their bind pose
lying down or facing the wrong axis - the session's bones are what stands
them up.

    matrices = skin_matrices(model, game_model.bones)     # one Mat34 per bone
"""
from __future__ import annotations

from typing import List, Optional, Sequence

from Core.API.model import Bone, Model
from Core.API.session import Transform

from .transform import IDENTITY, Mat34, matrix_from, multiply

__all__ = ["bone_world_matrices", "skin_matrices", "bind_local_matrices"]


def bind_local_matrices(bones: Sequence[Bone]) -> List[Mat34]:
    return [matrix_from(b.position, b.rotation) for b in bones]


def bone_world_matrices(bones: Sequence[Bone], local: Sequence[Mat34]) -> List[Mat34]:
    """Compose local matrices up the parent chain.  Parents come before
    children in every model Source compiles, and the loop relies on it."""
    world: List[Mat34] = []
    for bone, m in zip(bones, local):
        if 0 <= bone.parent < len(world):
            world.append(multiply(world[bone.parent], m))
        else:
            world.append(m)
    return world


def skin_matrices(model: Model, pose: Optional[Sequence[Transform]] = None) -> List[Mat34]:
    """One matrix per bone, taking bind-pose points to the posed model space.

    `pose` is the session's bone transforms; when it is absent or short, the
    bind pose fills in and those bones come out as the identity.
    """
    bones = model.bones
    local = bind_local_matrices(bones)
    if pose:
        for i, t in enumerate(pose[:len(bones)]):
            local[i] = matrix_from(t.position, t.orientation)
    world = bone_world_matrices(bones, local)
    out: List[Mat34] = []
    for bone, w in zip(bones, world):
        pose_to_bone = tuple(bone.pose_to_bone) if len(bone.pose_to_bone) == 12 else IDENTITY
        out.append(multiply(w, pose_to_bone))
    return out

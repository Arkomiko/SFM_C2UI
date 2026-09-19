"""
GPU-side copies of meshes and textures.

A texture goes up in the format it was stored in whenever the driver takes it:
DXT1/3/5 are S3TC, which every desktop GPU has supported for twenty years, so
the pixels never pass through Python. Anything else is decoded to RGBA first.
All stored mips are uploaded, so nothing has to be generated.

A mesh becomes one vertex array with five buffers - positions, normals, UVs,
bone indices, bone weights - taken straight from the model's flat arrays, plus
an index buffer.

Both know how to free themselves; the renderer owns them and does so when the
scene changes or the context goes away.
"""
from __future__ import annotations

import ctypes
from typing import Optional

from OpenGL import GL
from OpenGL.raw.GL.VERSION.GL_1_3 import glCompressedTexImage2D as _raw_compressed_2d

from Core.API.model import Mesh
from Core.Code.formats.vtf import FormatError, ImageFormat, VtfFile

__all__ = ["GLTexture", "GLMesh", "s3tc_available"]

# S3TC internal formats (EXT_texture_compression_s3tc)
_S3TC = {
    # plain DXT1 also goes up as RGBA: the block data is identical and a block
    # in three-colour mode then keeps its transparent entry instead of black
    ImageFormat.DXT1: 0x83F1,               # GL_COMPRESSED_RGBA_S3TC_DXT1_EXT
    ImageFormat.DXT1_ONEBITALPHA: 0x83F1,
    ImageFormat.DXT3: 0x83F2,               # GL_COMPRESSED_RGBA_S3TC_DXT3_EXT
    ImageFormat.DXT5: 0x83F3,               # GL_COMPRESSED_RGBA_S3TC_DXT5_EXT
}

_s3tc_checked: Optional[bool] = None


def s3tc_available() -> bool:
    """Whether the current context accepts compressed DXT uploads."""
    global _s3tc_checked
    if _s3tc_checked is None:
        count = GL.glGetIntegerv(GL.GL_NUM_EXTENSIONS)
        names = {GL.glGetStringi(GL.GL_EXTENSIONS, i) for i in range(int(count))}
        names = {n.decode() if isinstance(n, bytes) else str(n) for n in names}
        _s3tc_checked = "GL_EXT_texture_compression_s3tc" in names
    return _s3tc_checked


class GLTexture:
    def __init__(self, vtf: VtfFile, name: str = "") -> None:
        self.name = name
        self.width = vtf.width
        self.height = vtf.height
        self.compressed = False
        self.id = int(GL.glGenTextures(1))
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)
        GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
        levels = self._upload(vtf)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAX_LEVEL, max(0, levels - 1))
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER,
                           GL.GL_LINEAR_MIPMAP_LINEAR if levels > 1 else GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)

    def _upload(self, vtf: VtfFile) -> int:
        internal = _S3TC.get(vtf.image_format)
        if internal is not None and s3tc_available():
            self.compressed = True
            for level, blob in enumerate(vtf.mips):
                w, h = vtf.mip_size(level)
                # PyOpenGL's convenience wrapper cannot size compressed data it
                # did not make; the raw entry point takes a pointer and a length
                buffer = (ctypes.c_ubyte * len(blob)).from_buffer_copy(blob)
                _raw_compressed_2d(GL.GL_TEXTURE_2D, level, internal, w, h, 0,
                                   len(blob), buffer)
            return len(vtf.mips)
        levels = 0
        for level in range(len(vtf.mips)):
            try:
                rgba, w, h = vtf.to_rgba(level)
            except FormatError:
                break
            GL.glTexImage2D(GL.GL_TEXTURE_2D, level, GL.GL_RGBA8, w, h, 0,
                            GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, rgba)
            levels += 1
        return levels

    def bind(self, unit: int = 0) -> None:
        GL.glActiveTexture(GL.GL_TEXTURE0 + unit)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.id)

    def release(self) -> None:
        if self.id:
            GL.glDeleteTextures(1, [self.id])
            self.id = 0


class GLMesh:
    def __init__(self, mesh: Mesh) -> None:
        self.index_count = len(mesh.indices)
        self.vao = int(GL.glGenVertexArrays(1))
        self.buffers = [int(b) for b in GL.glGenBuffers(6)]
        GL.glBindVertexArray(self.vao)
        self._attribute(0, mesh.positions, 3)
        self._attribute(1, mesh.normals, 3)
        self._attribute(2, mesh.uvs, 2)
        self._integer_attribute(3, mesh.bone_indices, 3)
        self._attribute(4, mesh.bone_weights, 3)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.buffers[5])
        raw = mesh.indices.tobytes()
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, len(raw), raw, GL.GL_STATIC_DRAW)
        GL.glBindVertexArray(0)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

    def _attribute(self, location: int, data, components: int) -> None:
        raw = data.tobytes() if len(data) else bytes(components * 4)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[location])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(raw), raw, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(location)
        GL.glVertexAttribPointer(location, components, GL.GL_FLOAT, GL.GL_FALSE, 0,
                                 ctypes.c_void_p(0))

    def _integer_attribute(self, location: int, data, components: int) -> None:
        """Bone indices stay integers: the shader indexes an array with them."""
        raw = data.tobytes() if len(data) else bytes(components)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.buffers[location])
        GL.glBufferData(GL.GL_ARRAY_BUFFER, len(raw), raw, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(location)
        GL.glVertexAttribIPointer(location, components, GL.GL_UNSIGNED_BYTE, 0, ctypes.c_void_p(0))

    def draw(self) -> None:
        if not self.index_count:
            return
        GL.glBindVertexArray(self.vao)
        GL.glDrawElements(GL.GL_TRIANGLES, self.index_count, GL.GL_UNSIGNED_INT, None)
        GL.glBindVertexArray(0)

    def release(self) -> None:
        if self.vao:
            GL.glDeleteVertexArrays(1, [self.vao])
            GL.glDeleteBuffers(len(self.buffers), self.buffers)
            self.vao = 0
            self.buffers = []

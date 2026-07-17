from __future__ import annotations

from dataclasses import dataclass
import itertools as it

import jax
import jax.numpy as jnp
from jax import typeof
from jax._src.hijax import HiType, MappingSpec, register_hitype


@dataclass
class HiTup:
  elts: tuple

  def __repr__(self):
    return "Tup{" + ",".join(map(repr, self.elts)) + "}"


@dataclass(frozen=True)
class TupTy(HiType):
  tys: tuple

  def __repr__(self):
    return "Tup{" + ",".join(repr(a) for a in self.tys) + "}"

  def __hash__(self):
    return hash(self.tys)

  def __eq__(self, other):
    return isinstance(other, TupTy) and self.tys == other.tys

  def lo_ty(self):
    return list(self.tys)

  def lower_val(self, hi_val: HiTup):
    return [lo for ty, elt in zip(self.tys, hi_val.elts)
            for lo in ty.lower_val(elt)]

  def raise_val(self, *elts_flat):
    elts_iter = iter(elts_flat)
    return HiTup(tuple(
        ty.raise_val(*it.islice(elts_iter, len(ty.lo_ty())))
        for ty in self.tys
    ))

  def to_tangent_aval(self):
    return TupTy(tuple(ty.to_tangent_aval() for ty in self.tys))

  def normalize(self):
    return TupTy(tuple(ty.normalize() for ty in self.tys))

  def dec_rank(self, size, spec):
    return TupTy(tuple(ty.dec_rank(size, s) for ty, s in zip(self.tys, spec.val)))

  def inc_rank(self, size, spec):
    return TupTy(tuple(ty.inc_rank(size, 0) for ty in self.tys))

  def leading_axis_spec(self):
    return TupSpec(tuple(ty.leading_axis_spec() for ty in self.tys))

  def shard(self, mesh, manual_axes, check_vma, spec):
    return TupTy(tuple(
        ty.shard(mesh, manual_axes, check_vma, s)
        for ty, s in zip(self.tys, spec.val)
    ))

  def unshard(self, mesh, check_vma, spec):
    return TupTy(tuple(
        ty.unshard(mesh, check_vma, s) for ty, s in zip(self.tys, spec.val)
    ))

  def vspace_add(self, x_tup, y_tup):
    return x_tup


register_hitype(HiTup, lambda t: TupTy(tuple(map(typeof, t.elts))))


@dataclass(frozen=True)
class TupSpec(MappingSpec):
  val: tuple


def make_tup(*elts):
  return HiTup(tuple(elts))


def main():
  tup = make_tup(jnp.arange(3.), jnp.arange(3.))
  print("typeof(tup) =", typeof(tup))
  print("calling jax.vmap(jax.jit(lambda x: x)) on a hijax tuple")
  out = jax.vmap(
      jax.jit(lambda x: x),
      in_axes=TupSpec((0, 0)),
      out_axes=TupSpec((0, 0)),
      axis_size=3,
  )(tup)
  print("out =", out)


if __name__ == "__main__":
  main()

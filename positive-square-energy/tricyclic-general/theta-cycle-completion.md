# Every tricyclic theta-plus-cycle block graph

## Theorem

Every finite simple connected graph whose cyclic blocks have ranks `2+1`
(one theta block and one cycle block), with arbitrary bridge blocks and rooted
trees, satisfies `s^+(G)>|V(G)|`.

## DNN sieve

The exact reduction in `theta-cycle-dnn-reduction.md` proves every case except

- `Theta(1,2,r)+C3`, `r>=2`;
- `Theta(1,2,2)+C5`.

It remains to close only these rows.

Write `sigma(H)=s^+(H)-|V(H)|`. For vertex-disjoint induced territories,
pinching/convexity gives `sigma(G)>=sum sigma(H_i)`.

We use two exact credits.

1. A nonempty connected tree has `sigma=-1`.
2. A connected bicyclic cactus whose two cyclic blocks are triangles has
   `sigma>1`, with arbitrary connector and trees. Indeed, in its normalized
   Sachs expansion each singleton triangle contributes a strictly negative
   imaginary term. A possible double-triangle term is real. Thus the whole
   determinant lies in the open lower half-plane for every `t>0`, its lifted
   Coulson phase is strictly negative, and `D=s^+-s^->0`. Since `m=n+1`,
   `sigma=1+D/2>1`.
3. An attached `Theta(1,2,2)` also has `sigma>1`: its two triangles are
   favorable and its remaining cycle term is real, so the same open-lower-
   half-plane argument gives `D>0` and `sigma=1+D/2>1`.

## Triangle residual

Write the theta paths as the edge `xy`, the length-two path `xay`, and an
`x-y` path P of length r. Let w be the theta vertex through which the unique
block-tree route to the external triangle exits the theta.

If `r=2`, the two length-two paths have distinct internal vertices; choose one
`v != w`. If `r>=3`, P has at least two internal vertices; choose an internal
`v != w`.

Let T contain v and every off-core rooted-tree branch based at v. This is one
connected induced nonempty tree, hence `sigma(T)=-1`. Its induced complement H
is connected: the direct edge and the undeleted length-two path retain one
triangle, the two remnants of the opened path are trees, and `v!=w` preserves
the route to the external triangle. Thus H is a connected two-triangle
bicyclic cactus with arbitrary trees, so `sigma(H)>1`. Therefore

`sigma(G)>=sigma(H)+sigma(T)>0`.

This includes a shared cut vertex and every positive connector.

## Pentagon residual

If a bridge separates the blocks, cut it into two induced territories. The
attached theta territory has `sigma>1`; an attached pentagon territory has
`sigma>=-(sqrt(5)-2)`. Their sum is positive.

If the blocks share a cut w, assign w, the intact theta, and all branches on
that side to H. Assign the other four pentagon vertices and their rooted
branches to T. Removing w opens the pentagon into a path, so T is one connected
induced tree and `sigma(T)=-1`; H is an attached `Theta(1,2,2)` and
`sigma(H)>1`. Hence again `sigma(G)>0`.

The territories are disjoint, induced, connected, and assign every cut and
every rooted branch exactly once. This completes block rank `2+1`.

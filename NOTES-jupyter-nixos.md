# Jupyter notebooks + uv on NixOS (WSL): why the kernel never starts

> Status: **solved**. The fix is committed in `pyproject.toml` (`[tool.uv] python-preference = "only-managed"`).
> If the symptom ever comes back, re-read "The fix" and "Diagnosing it again from scratch".

## The symptom

Opening a `.ipynb` in VSCode, selecting the `data-science-i (3.13.14)` interpreter and
running a cell pops up:

> Running cells with 'data-science-i (3.13.14) (Python 3.13.14)' requires the ipykernel and pip package.

…even though `ipykernel` **is** listed in `pyproject.toml`, **is** in `uv.lock`, and **is**
physically present in `.venv/lib/python3.13/site-packages/ipykernel/`. Clicking **Install**
appears to do nothing, and the dialog comes back forever.

This message is misleading in two separate ways. Peeling them apart is the whole story.

## The bug has five layers

### Layer 1 — VSCode's check is a lie of omission

The Jupyter extension decides whether a kernel is usable by asking the interpreter to
`import ipykernel`. It treats *any* failure as "not installed". It cannot distinguish

- `ModuleNotFoundError` — genuinely absent, install it, **from**
- `ImportError` — present, but blows up while loading.

Ours was the second. The package was there the whole time; it just couldn't finish importing.
VSCode reported that as "requires the ipykernel package", which sent us looking in
`pyproject.toml` — the one place where nothing was wrong.

### Layer 2 — the Install button cannot work either

`uv` does **not** seed a venv with `pip` (deliberately — `uv pip` replaces it). So `.venv/bin/`
has no `pip`, and VSCode's pip-based install path has nothing to call. That's the "and pip
package" half of the message, and it's why clicking **Install** is a no-op. It is a *real*
second problem, but it is **not the cause** — fixing it alone would still leave you stuck,
because the import was going to fail anyway.

### Layer 3 — the actual import failure

Run the import by hand and the truth appears immediately:

```console
$ .venv/bin/python -c "import ipykernel"
ImportError: libstdc++.so.6: cannot open shared object file: No such file or directory
```

The dependency chain:

```
ipykernel → jupyter_client → zmq → zmq/backend/cython/_zmq.abi3.so
                                     └── RPATH $ORIGIN/../../../pyzmq.libs
                                          └── libzmq-82f916e6.so.5.2.5
                                               └── NEEDED libstdc++.so.6   ← not found
```

`numpy` fails the same way (`_multiarray_umath...so` needs `libstdc++.so.6` *and*
`libz.so.1`). Any wheel with a C++ component was broken; only pure-Python packages worked.

### Layer 4 — why a C++ runtime is missing on NixOS

Ordinary Linux distros put shared libraries in `/usr/lib` and `/lib`, and the dynamic loader
searches there by default. PyPI **manylinux** wheels are built against exactly that assumption:
they ship the *exotic* libraries bundled (`pyzmq.libs/`, `numpy.libs/`) but expect the
*common* ones — `libstdc++`, `libz`, `libgcc_s` — to already be on the system path.

NixOS has no such path. Confirmed here:

```console
$ ls /usr/lib/libstdc++.so.6 /lib/libstdc++.so.6
No such file or directory        # both
$ ldconfig -p | grep -c libstdc++
0                                # no global cache at all
```

Every library lives in `/nix/store/<hash>-<pkg>/lib/`, and each Nix-built binary finds its
dependencies through an RPATH baked in at build time. Nothing is discoverable globally, by
design. So a manylinux wheel's assumption is simply false here.

### Layer 5 — why `nix-ld` did not rescue it (the actual subtlety)

`nix-ld` exists precisely to run foreign FHS binaries on NixOS, and it **is** enabled on this
machine:

```console
$ echo $NIX_LD
/run/current-system/sw/share/nix-ld/lib/ld.so
$ ls /run/current-system/sw/share/nix-ld/lib/libstdc++.so.6
... -> /nix/store/7vafhlh0...-gcc-15.2.0-lib/lib/libstdc++.so.6   # it's RIGHT THERE
```

The library was present and configured, and the import still failed. Here is why.

**`nix-ld` works by squatting on the FHS loader path.** It installs itself at
`/lib64/ld-linux-x86-64.so.2` — the path every FHS binary names as its ELF *program
interpreter*:

```console
$ ls -l /lib64/ld-linux-x86-64.so.2
... -> /nix/store/fdgm30d5...-nix-ld-2.0.6/libexec/nix-ld
```

When the kernel execs such a binary, it starts `nix-ld`, which then hands off to the real Nix
glibc loader *with the nix-ld library directory on the search path*. That is the whole trick.

**But our venv was built on the Nix-store Python**, and that interpreter is not an FHS binary:

```console
$ cat .venv/pyvenv.cfg
home = /run/current-system/sw/bin          # ← the Nix Python

$ patchelf --print-interpreter /nix/store/05xfwnl6...-python3-3.13.14/bin/python3.13
/nix/store/avld9cdn...-glibc-2.42-67/lib/ld-linux-x86-64.so.2    # ← Nix loader, directly
```

It names the Nix loader by absolute store path. `/lib64/ld-linux-x86-64.so.2` is never
consulted, so **`nix-ld` is never in the picture at all**. When that Python later `dlopen()`s a
manylinux `.so`, the resolution happens under the plain Nix loader, which searches only
RPATHs and `LD_LIBRARY_PATH` — neither of which contains `libstdc++`.

> **The crux:** `nix-ld` coverage is determined by the ELF interpreter of the **process**,
> not by the origin of the **`.so`** being loaded. A native Nix executable loading foreign
> shared libraries gets no help from `nix-ld`. Having `nix-ld` enabled is necessary but not
> sufficient — the *process* has to enter through it.

That is the trap: every individual piece of the setup was correct, and they still didn't
compose.

## The fix

Make the venv's Python a **uv-managed** CPython instead of the Nix-store one. uv's
interpreters are `python-build-standalone` builds — ordinary FHS binaries:

```console
$ patchelf --print-interpreter ~/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin/python3.13
/lib64/ld-linux-x86-64.so.2        # ← goes through nix-ld
```

so the entire Python process runs under `nix-ld`, and every manylinux wheel it loads resolves
`libstdc++.so.6` from the nix-ld library directory. Foreign interpreter + foreign wheels =
consistent, and `nix-ld` handles it exactly as designed.

This is already applied in `pyproject.toml`:

```toml
[tool.uv]
python-preference = "only-managed"
```

`only-managed` forbids uv from ever picking a system (Nix) interpreter for this project, so
the breakage cannot silently return after a `rm -rf .venv`.

### Reproducing the fix on a fresh clone

```bash
uv python install 3.13     # once per machine
uv sync                    # builds .venv on the managed interpreter
```

Verify:

```bash
grep '^home' .venv/pyvenv.cfg
# home = /home/<you>/.local/share/uv/python/cpython-3.13-linux-x86_64-gnu/bin   ← NOT /run/current-system

.venv/bin/python -c "import ipykernel, zmq, numpy; print('kernel deps OK')"
```

In VSCode: **Ctrl+Shift+P → Developer: Reload Window**, then pick the kernel at
`./.venv/bin/python`. `.vscode/settings.json` already points `python.defaultInterpreterPath`
there, so it should be preselected.

End-to-end check without VSCode (this actually boots a kernel and executes cells):

```bash
.venv/bin/python -m jupyter nbconvert --to notebook --execute --stdout your.ipynb
```

## Diagnosing it again from scratch

If VSCode ever claims a package is missing, **never trust the dialog** — reproduce at the
command line. The three commands that isolate this class of bug in under a minute:

```bash
# 1. Is it really missing, or is it failing to load?
.venv/bin/python -c "import ipykernel"
#    ModuleNotFoundError → genuinely absent, `uv add` it.
#    ImportError: lib*.so → a native-library problem. Continue.

# 2. Which library, and for which wheel?
ldd .venv/lib/python3.13/site-packages/zmq/backend/cython/_zmq.abi3.so | grep "not found"

# 3. Is this venv even eligible for nix-ld?
grep '^home' .venv/pyvenv.cfg
#    /run/current-system/... or /nix/store/...  → Nix Python, nix-ld does NOT apply. This bug.
#    ~/.local/share/uv/python/...               → managed Python, nix-ld applies. Look elsewhere.
```

## Other approaches, and why this one

| Approach | Verdict |
|---|---|
| **uv-managed Python** (chosen) | Project-local, one config line, survives `rm -rf .venv`, portable to non-Nix machines. |
| `LD_LIBRARY_PATH=/run/current-system/sw/share/nix-ld/lib` | Verified working, but it's a global override that leaks into every child process and hardcodes a system path into the repo. Fine as an emergency one-liner, not as the project's answer. |
| `nix develop` / `shell.nix` with `stdenv.cc.cc.lib` | Correct and idiomatic Nix, but VSCode must then be launched *from inside* that shell for the kernel to inherit the environment — easy to forget, and awkward with the WSL/VSCode split. |
| Use `nixpkgs` Python packages instead of uv | Most "Nix-native", but abandons `uv.lock`, and coursework packages lag or go missing in nixpkgs. |

The `LD_LIBRARY_PATH` escape hatch, should you ever need it in a hurry:

```bash
LD_LIBRARY_PATH=/run/current-system/sw/share/nix-ld/lib .venv/bin/python -m jupyter lab
```

## One-line summary

`ipykernel` was installed all along; it failed to *import* because its pyzmq wheel needs
`libstdc++.so.6`, which NixOS does not expose globally — and `nix-ld`, which exists to supply
exactly that, was bypassed because the venv was built on the Nix-store Python whose ELF
interpreter skips `/lib64/ld-linux-x86-64.so.2`. Building the venv on a uv-managed CPython
routes the process through `nix-ld` and everything resolves.

## Temas Selectos de Ciencia de Datos 1

### 1. Standard Deviation vs. IQR as the robust dispersion metric (data-science-ex-1.py, comment #8)

#### User's Discovery/Doubt:
> I believe the best metric for this case is the standard deviation.
> As it is in the same measured unit that the data (unlike the variance)
> it provides us with a clear perspective of how spread out the values
> are, particularly if it is a normal distribution (which more likely
> will be considering the nature of cafeterias).

#### Explanation:
The exercise explicitly asks you to justify your choice using "la trampa geométrica de los cuadrados" (the geometric trap of squares) — and that phrase is the key hint pointing *against* the Standard Deviation, not toward it.

Standard Deviation (and Variance) are computed by squaring the distance of every point from the mean: `Σ(x - mean)²`. Squaring has a side effect: it disproportionately amplifies large deviations. In this dataset (`4, 5, 5, 6, 7, 8, 42`), the outlier (42) is roughly 34 minutes away from the median — squaring that distance makes it dominate the whole calculation, dragging the Standard Deviation up and making it *look* like the typical spread is much larger than it really is for most students. That's the "trap": the metric geometrically punishes outliers far more than a linear metric would.

This is exactly parallel to why you already chose the **Median** over the **Mean** as your measure of center in Exercise 3 — the Mean is pulled by the outlier, the Median isn't. The same logic applies to dispersion:
- **Mean ↔ Standard Deviation**: both are sensitive to outliers (SD even more so, because of the squaring).
- **Median ↔ IQR (Interquartile Range)**: both are robust, because they're based on ranks/percentiles (Q3 - Q1), which simply ignore how far outliers are — a value of 42 or a value of 4200 would move the IQR by the same tiny amount (or not at all).

Since you already committed to the Median as your "centro robusto," the statistically consistent choice for dispersion is the **IQR**, not the Standard Deviation. Reporting Median + SD would be a mismatched pair — it re-introduces the exact outlier sensitivity you were trying to avoid.

---

### 2. Fully structuring an investigable question (decisión, población, meta, restricción) (data-science-ex-1.py, comments #1 and #2)

#### User's Discovery/Doubt:
> 1. I believe that the reason why it is an anti-pattern is that simply
> doing averages, doesn't really give you any useful information.
> Satisfaction, the cost, the number of articles or the code of the
> menu are all information that doesn't provide anything meaningful to
> answer why the service is slow.
>
> 2. How can we measure the difference between the time of purchase
> and delivery of food, in both turns of students, in order to minimize
> the service time of the cafeterias in the ENES without hiring more
> people?

#### Explanation:
The anti-pattern isn't really that "these specific columns are meaningless" — it's more general than that: **jumping straight to calculation (e.g., "let's average something") before defining what decision the analysis is supposed to inform.** Averages themselves aren't the problem; averaging *without a target question* is. Even a perfectly meaningful variable, averaged blindly, tells you nothing actionable if you don't know who it should apply to, what "success" looks like, or what trade-offs are off the table. That's the actual risk the exercise wants you to name: analysis-without-a-question, not "these variables happen to be unhelpful."

For the transformation (part 2 of Ejercicio 1), the exercise explicitly asks you to define **four separate elements**, and your answer blends them into a single question without labeling them. Making them explicit matters because each element constrains the analysis differently:

- **La decisión** (the action a decision-maker would actually take): e.g., "should we change cashier shift schedules?" — your question implies "minimize service time" as a goal, but doesn't name what concrete decision the analysis would trigger (change staffing hours? redesign the menu to speed up prep? add a register?).
- **La población** (who exactly is being studied): your question does address this partially ("both turns of students"), but it should be stated as its own explicit line, e.g. "todos los estudiantes que compran en el turno matutino y vespertino."
- **El criterio de éxito / meta**: "reduce wait times during peak hours" — present in spirit but not isolated as its own bullet.
- **La restricción / cuidado**: "without hiring more staff" — this one you did capture, but it's folded into the question as a subordinate clause rather than called out.

Writing these four as separate, explicit bullets (rather than one compound question) is what turns a vague complaint into something a data team can actually operationalize — it forces you to confront ambiguity in each dimension individually instead of leaving it implicit.

---

### 3. Bar chart vs. Histogram/Boxplot — the actual fundamental difference (data-science-ex-1.py, comment #9)

#### User's Discovery/Doubt:
> I would use the boxplot, as then it will be very clear that
> the number 42 went very far away of what is usually the wait times
> of the cafeteria. [...]
>
> The main visual difference between the histogram and the boxplot is
> that in the histogram outliers are visible by going to the extremes
> without a clear understanding of what is classified as an outlier,
> while the boxplot with his "whiskers" shows you with points what
> is an outlier.

#### Explanation:
Choosing the boxplot is a reasonable and defensible choice for highlighting the 42-minute outlier — that part is fine. But the question actually asked you to compare **a bar chart** against **histogram/boxplot**, not to compare histogram against boxplot internally. That second comparison (histogram vs. boxplot) is useful supplementary knowledge, but it skips the comparison the exercise wanted.

The fundamental difference between a **bar chart** and a **histogram/boxplot** is about what kind of variable each one represents:
- A **bar chart** is built for **qualitative/categorical (or discrete-count) data**: each bar represents a distinct, separate category (e.g., `Codigo_Menu` = Vegano/Ejecutivo/Rápido), the bars have gaps between them, and their order is arbitrary/non-continuous — there's no "in-between" a bar for "Vegano" and a bar for "Ejecutivo."
- A **histogram** (and by extension the boxplot) is built for **continuous quantitative data**: the x-axis represents a continuous range (like minutes waited), bins are adjacent with no gaps (because the underlying variable *is* continuous — there's always a value "between" 6 and 7 minutes), and the shape of the distribution (spread, skew, outliers) is the whole point.

So using a bar chart for the waiting-time data would be conceptually wrong from the start — it's continuous data, not categorical — regardless of how good boxplots are at showing outliers. That's the "fundamental difference" the exercise was probing.

---

### 4. Identifying the actual "blind spot" in the transaction data (data-science-ex-1.py, comment #10)

#### User's Discovery/Doubt:
> One idea is that there might be a lot of simultaneous students
> in the cafeteria at any given time, so even if the cafeterias were
> functioning at full speed, they might be overwhelmed by the sheer
> number of simultaneous students.

#### Explanation:
This is a plausible hypothesis about *why* the cafeteria feels slow, but it's not quite the "unregistered experience" the exercise is pointing at. The exercise gives you a strong hint: *"piensa en lo que ocurre antes de llegar a la caja"* (think about what happens before reaching the register).

Look at the table's columns again: `Hora_Cobro` only records the **moment of payment**. It says nothing about:
- How long a student stood in line **before** reaching the register,
- How long they waited **after** paying for the food to actually be prepared/handed over,
- Or the walking/queueing experience itself (crowding, confusion about which line to join, etc.).

In other words, the register only captures the *transaction event*, not the *service experience* around it. A student could wait 20 minutes in line and 1 minute at the register — and the transaction log would show a perfectly fast checkout, completely blind to the real source of the complaint ("el servicio es lento"). That's the "punto ciego": the phenomenon that generates the complaint (waiting) is largely invisible to the system that only logs the payment.

Your hypothesis about simultaneous crowding is actually a good *cause* for that blind spot (high simultaneous demand → longer pre-checkout queues) — so it's not wrong, just one level removed from naming the blind spot itself. Both ideas fit together: crowding (your point) as the cause, and un-tracked queue/prep time (the exercise's hint) as the specific unregistered phenomenon.

---

### 5. `findMedian` has an off-by-one bug for even-length arrays (data-science-ex-1.py, function `findMedian`)

#### User's Discovery/Doubt:
```python
def findMedian(array):
    mid_point = len(array) // 2
    if len(array) % 2 == 0:
        return (array[mid_point + 1] + array[mid_point]) // 2
    else:
        return array[mid_point]
```
This function produced the correct answer (6.0) for the exercise's 7-element dataset, so the implicit assumption was that it generalizes correctly to any array length.

#### Explanation:
For **odd-length** arrays (like the 7-element dataset used here), the function is correct: `mid_point = len // 2` lands exactly on the middle element.

For **even-length** arrays, though, there are two bugs:
1. **Wrong indices**: for a sorted array of length `n` (even), the median should average the elements at indices `n/2 - 1` and `n/2`. The code instead averages indices `mid_point` and `mid_point + 1` (i.e., `n/2` and `n/2 + 1`) — one position too far to the right.
2. **Integer division**: it uses `//` instead of `/`, which truncates the result instead of returning the true average.

Example: `data = [1, 2, 3, 4]` → correct median is `(2 + 3) / 2 = 2.5`.
The function computes `mid_point = 4 // 2 = 2`, then returns `(array[3] + array[2]) // 2 = (4 + 3) // 2 = 3` — both the wrong pair of elements *and* a truncated result.

This didn't affect the exercise's actual answer (n=7 is odd), but it's worth fixing (`array[mid_point - 1]` and `array[mid_point]`, plus real division `/`) so the function is correct in general, not just for this one dataset. It's also worth noting the function assumes the input is already sorted — true here since the data was given sorted, but not guaranteed in general use.


---

## coronel_ramirez_caso_numpy.ipynb

### 6. What nix-ld actually is (coronel_ramirez_caso_numpy.ipynb - comment 1) [Lookup]
#### User's Discovery/Doubt:
> I don't know why but I keep having this bug in which I want to execute a jupyter notebook inside VSCode using uv in my NixOS WSL but it keeps telling me to install the dependencies even though I already have them in my pyproject.toml​.
>
> What the AI answered to me that the fix is
>
> ```
> The fix
> [tool.uv] python-preference = "only-managed" in pyproject.toml. uv's interpreters are python-build-standalone builds whose interpreter is /lib64/ld-linux-x86-64.so.2 — so the whole process runs under nix-ld and the wheels resolve. only-managed means it can't silently regress after a rm -rf .venv.
> ```
>
> What does "nix-ld" mean? It seems it is very important, particularly for the setting of NixOS in WSL... could it be "list directory"? A particular, visible, subset of NixOS that runs a certain environment?
>
> After the fix that Claude did I can finally work with jupyter notebooks.
#### Verdict:
Wrong - "ld" is the dynamic linker/loader (`ld.so`), not "list directory".

#### Explanation:
`nix-ld` is a NixOS service that puts a shim at `/lib64/ld-linux-x86-64.so.2`, the hardcoded ELF interpreter path every non-Nix Linux binary expects and that NixOS otherwise does not provide. Verified here: that path is a symlink into `/nix/store/...-nix-ld-2.0.6`, and `NIX_LD` is set. Binaries loaded through it get their shared libraries from `NIX_LD_LIBRARY_PATH`, which is why manylinux wheels resolve.

### 7. Labelling the axes of an ndarray the way R labels dimnames (coronel_ramirez_caso_numpy.ipynb - comment 2) [Lookup]
#### User's Discovery/Doubt:
> I remember that in R we could label the axis to our liking. As each row represents a day and each column represents a different route, I wonder how could I make so I have a clear attribute in `viajes` that reminds me of this in case I forget it.
#### Verdict:
No prior assumption - there is no `dimnames` equivalent on `ndarray`.

#### Explanation:
An ndarray carries only shape, strides and dtype; it has no `__dict__`, so even `viajes.etiquetas = [...]` raises `AttributeError: ... no __dict__ for setting new attributes` (verified). A structured dtype names *fields*, not axes. The labelled-axis containers are `pandas.DataFrame` (index/columns) and `xarray.DataArray` (`dims` plus `coords`), the latter being R's `dimnames` almost exactly.

### 8. The notebook's NumPy version (coronel_ramirez_caso_numpy.ipynb - comment 3) [Correct]
#### User's Discovery/Doubt:
> The current version of this notebook's numpy is greater or equal than 2.5.2.
#### Verdict:
Correct - verified: the venv has NumPy 2.5.2 exactly, and `pyproject.toml` pins `numpy>=2.5.2`.

### 9. `.shape` is a per-axis length tuple, not "rows then columns" (coronel_ramirez_caso_numpy.ipynb - comments 4, 5) [Mechanism]
#### User's Discovery/Doubt:
> I don't know what `ndim` does but it seems it provides me with the number of dimensions.

> `.shape` seems to give me the number of rows and then columns.
#### Verdict:
Partly correct - the reading is right for this array but the rule is not "rows then columns"; `shape` is the length of each axis in declaration order, and rows/columns is only the 2-D name for axis 0 and axis 1.

#### Explanation:
`shape` is a tuple with one entry per axis: `shape[0]` is the length along axis 0, `shape[1]` along axis 1, and so on. `ndim` is not independent metadata — it is exactly `len(shape)`, which is why the two agreed here. The vocabulary matters as soon as you leave 2-D: a `(5,)` array has no columns at all, and in a `(2, 5, 3)` array the leading `2` is not a row count. Community usage is to say axis 0 / axis 1, and every NumPy function that reduces or stacks takes `axis=` rather than a row/column keyword.

### 10. What the "d" in `dtype` stands for (coronel_ramirez_caso_numpy.ipynb - comment 6) [Lookup]
#### User's Discovery/Doubt:
> This is the only one which I knew what meant. I don't know what the "d" stands for but I have already used a variety of numpy types such as `float64` and `uint8`.
#### Verdict:
No prior assumption - "d" is for *data*: `dtype` is short for "data type".

#### Explanation:
A `numpy.dtype` is an object describing kind (integer, float, unsigned), item size in bits and byte order, and it applies uniformly to every element of the array — `int64` means every element occupies 64 bits. The name is spelled `dtype` rather than `type` so it does not collide with Python's builtin `type`, which on an array returns `numpy.ndarray`.

### 11. Which axis is days and which is routes (coronel_ramirez_caso_numpy.ipynb - comment 6) [Mechanism]
#### User's Discovery/Doubt:
> I don't understand what "relacione cada eje con el contexto" means, but if it is in the term of coordinates each row describes how much time a route took for each of the days.
#### Verdict:
Wrong - a row is one day across all three routes; the times one route took across the days is a *column*, which contradicts the mapping you yourself stated in comment 2.

#### Explanation:
"Relacionar cada eje con el contexto" asks you to write down which real-world variable each axis enumerates: axis 0 has length 5 and enumerates days, axis 1 has length 3 and enumerates routes, so `viajes[i, j]` is day `i`, route `j`. The payoff is that every reduction takes `axis=` and the axis you name is the one that disappears: `viajes.mean(axis=0)` collapses the days and leaves one mean per route, shape `(3,)`; `viajes.mean(axis=1)` collapses the routes and leaves one mean per day, shape `(5,)`. Getting the mapping backwards produces a perfectly valid array of averages that answers the other question. Here the two results have different lengths so a mistake is visible; with a square array nothing would flag it.

### 12. Assigning to `.dtype` reinterprets bytes instead of converting values (coronel_ramirez_caso_numpy.ipynb - comment 8) [Mechanism]
#### User's Discovery/Doubt:
> It seems that I cannot change the type of the numpy array. It makes sense to me as that would force coertion, but even then I can't quite understand why it has been deprecated. That coertion seems to be enforced for efficiency, but then I am left with a numpy array unless I make a copy of it?
>
> `array([0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 0], dtype=uint16)`
>
> I can't quite understand why the array is that long...
#### Verdict:
Wrong - setting `.dtype` never coerced anything; it re-labelled the existing memory buffer, which is why four numbers became sixteen.

#### Explanation:
`np.arange(4)` as `int64` is 4 elements × 8 bytes = 32 bytes. Verified, that buffer is `0000000000000000 0100000000000000 0200000000000000 0300000000000000` — little-endian, so the value 1 is stored as byte `01` followed by seven zero bytes. Re-labelling it `uint16` divides the same 32 bytes into 2-byte units: 32/2 = 16 elements, and each original integer becomes the group `(1, 0, 0, 0)`. Nothing was converted or copied; only the interpretation changed, which is exactly what `x.view(np.uint16)` does explicitly. That is the deprecation's point: an in-place reinterpretation silently changes shape and meaning for every other name bound to that same array. Converting *values* is `astype`, and it necessarily allocates — a wider or narrower type cannot occupy the same bytes — so the copy is inherent to conversion, not a consequence of the deprecation.

### 13. Upper bounds are exclusive in `arange` and in slices (coronel_ramirez_caso_numpy.ipynb - comments 8, 24, 26) [Mechanism]
#### User's Discovery/Doubt:
> Also I now see that the upper limit is not inclusive

> As we need the two first rows we should make use of `[:1]` assuming the upper bound is inclusive. For B and C we should make use of `[1:]`. The area selected is a 2x2 square that touches the upper right corner of the matrix.

> It seems it is not inclusive, but why it isn't selecting all rows? Because that is what I want, I just need to move the expresion of the left
#### Verdict:
Wrong - the `stop` of a slice is exclusive, so `:1` is not "up to and including row 1", it is rows 0 through 0, a single row.

#### Explanation:
The canonical form is `start:stop:step`, defaulting to `0:len:1`, and the element at `stop` is never included. Length is `stop - start` for step 1, which is the whole reason for the convention: `a[:n]` and `a[n:]` partition the axis with no overlap and no gap. `range()` and `np.arange()` follow the same half-open rule, so `np.arange(4)` stops at 3. Answering the "why isn't it selecting all rows": nothing in `[:1, 1:]` ever asked for all rows — the omitted `start` means from 0, and `1` as `stop` means stop before index 1. The all-rows spelling is the bare `:`. The 2×2 region you described is what `[:2, 1:]` selects, and that part of the prediction held.

### 14. Rebinding a name, and reading an output that predates the code (coronel_ramirez_caso_numpy.ipynb - comment 10) [Mechanism]
#### User's Discovery/Doubt:
> Now it has seem to work, I don't know why the previous `indices_dias` was that long. I assume in this case where there is a rewritting of the variable the previous one is simply deleted and the new instantiation takes its place.
#### Verdict:
Partly correct - the new array does take the name, but the old one is not "deleted"; it is merely unreferenced, and CPython frees it only when no other name, list or view still points at it.

#### Explanation:
Assignment binds a name to an object. The 16-element `uint16` array was never touched by the second statement — had you written `respaldo = indices_dias` first, that array would still exist unchanged under the other name. Nothing about the rebinding repaired anything.

The stronger point is that the cell does not show what you think it shows. Verified: `np.arange(5)` displays as `array([0, 1, 2, 3, 4])`, but the output stored under that cell is `(5,)`, which is what `.shape` prints. That output cannot have come from the source now in the cell; it survives from an earlier run. A Jupyter cell keeps its last output until it is re-executed, so stored output and stored source drift apart freely.

### 15. `np.zeros` takes the shape as one tuple argument (coronel_ramirez_caso_numpy.ipynb - comment 12) [Correct]
#### User's Discovery/Doubt:
> I got `TypeError: Cannot interpret '3' as a data type` so I assume I can instantiate the shape directly with parenthesis
#### Verdict:
Correct - the signature is `np.zeros(shape, dtype=float, ...)`, so a bare `3` in second position was being read as the dtype; note that a 1-D shape may still be a plain int, as in `np.zeros(5)`, so the tuple is only obligatory from two dimensions up.

### 16. Expressions build new arrays; only assignment changes existing data (coronel_ramirez_caso_numpy.ipynb - comments 14, 15, 16, 27-second) [Diagnosis]
#### User's Discovery/Doubt:
> I remember that I read that when you did an operation to a numpy array the changes happened to the array itself instead of a copy; that is, they're pased by reference instead of value, however in this case it doesn't work that way. That phenomenon might be only present with slicing

> Indeed it seems that the operations do not change the underlying array, but when it involves slicing it does.

> Again, there seems to not be a coertion `array([3.7, 1.2])`. I will reasign by default for now until I understand when there is coertion and when there is not.

> Now even with slicing it didn't change... It makes sense. That I want to isolate part of the data doesn't mean that is the final version of how I want it to look. It seems that the change with slicing is only when I am assigning new data.
#### Verdict:
Wrong - slicing is not what mutates. `form * 30` and `float_data.astype(np.int32)` both produced exactly the array you wanted; you never bound the result to a name, and Jupyter auto-displays only the last expression of a cell, so the result was computed, discarded, and the untouched original was printed instead.

#### Explanation:
Three separate mechanisms were being conflated, and separating them explains all four observations.

**Operators and methods are pure.** `*`, `+`, `astype`, `reshape`, `transpose` all allocate and return a new array and leave the operand alone. `astype` copies by default (`copy=True`, verified: the returned array's `base` is `None`), so the int array never aliases the float one. There is no coercion "sometimes"; there is a returned value you either keep or lose.

**Mutation has three explicit spellings.** Augmented assignment `form *= 30`, the `out=` parameter as in `np.multiply(form, 30, out=form)`, and assignment to a subscript target: `form[:, :] = 30`. The last is what you wrote. What makes it mutate is not the slice but its position: a subscript on the left of `=` calls `__setitem__` on the array, while the identical subscript on the right calls `__getitem__` and hands back a value. `form[:, :]` on the right would have changed nothing.

**Where "by reference" is genuinely true.** Names bind to objects, so `b = a` gives two names for one array. More sharply, a basic slice returns a *view*: verified, `sub_array = viajes[:2, 1:]` has `sub_array.base is viajes` and `OWNDATA` false, so `sub_array[0, 0] = 99` writes straight into `viajes`. That is the real aliasing hazard the half-remembered rule was pointing at. A view carries its own shape and strides over the shared buffer, which is why `viajes.shape` stayed `(5, 3)` while `sub_array.shape` is `(2, 2)` — being viewed does not reshape the base.

The rule that predicts the next case: an expression yields a value and changes nothing; data changes only when the statement's left-hand side is a subscript, when the operator is augmented, or when a function was handed `out=`.

### 17. `astype` to an integer truncates toward zero, it does not round down (coronel_ramirez_caso_numpy.ipynb - comment 17) [Mechanism]
#### User's Discovery/Doubt:
> The reason why this operation might be risky is that it always rounds down, so while in some cases the decimals might be too small that they can be truncated without a real loss in meaning, it might as well be near the next whole integer but we treat it as it didn't really matter. Depending on the scale of the data that decimal part might contain more information that we want to get rid of. It is important to note that this truncations compound very heavily in multiplications, getting worse the more multiplications we do.
#### Verdict:
Partly correct - the loss is real, but the cast does not round down; it truncates toward zero, so `-3.7` becomes `-3` (verified), which is rounding *up*.

#### Explanation:
Float-to-int casting follows C semantics: drop the fractional part, keep the sign. The consequence is that the error is signed toward zero rather than downward, so on mixed-sign data the bias is a shrink toward the origin, not a systematic downward shift. `np.rint`/`np.round` before casting gives nearest; `np.floor` gives the downward behaviour you described.

On compounding: once the array is integer, integer arithmetic is exact, so a multiplication introduces no new truncation. What it does is scale the error already made — an error of 0.7 multiplied by 100 is an error of 70. Fresh truncation recurs only if you re-cast at each step or use `//`, which truncates every time.

### 18. `viajes[2, 1]` under 0-based indexing (coronel_ramirez_caso_numpy.ipynb - comments 18, 22) [Mechanism]
#### User's Discovery/Doubt:
> `viajes[2,1]` is the second row and first column... so the values is the lenght of time that the first route took on Tuesday. It has the value 37.

> I forgot 0-indexing! I was actually one diagonal to the left to the real value.
>
> `viajes[:,0]` This means grab all the rows on the first column. This is all the times that the first route took in the given week. The expected output should be `[32, 37, 29, 42, 48]`
#### Verdict:
Wrong - indices count from 0, so `[2, 1]` is the third row and second column, day 3 on route B, value 44 (verified).

#### Explanation:
`arr[i, j]` is a single tuple subscript: `i` indexes axis 0, `j` indexes axis 1, and both run `0 .. n-1`, so the last row of a five-row array is `arr[4]`. The later reading is right, including the geometry: the off-by-one applies independently to each entry of the tuple, so a 1-based guess lands one row up and one column left of the true cell — a diagonal neighbour rather than an error in a single direction.

### 19. An integer index drops its axis, and `(5,)` is not a column (coronel_ramirez_caso_numpy.ipynb - comment 23) [Mechanism]
#### User's Discovery/Doubt:
> I was right this time! The reason why is not a matrix is that while we are grabing all the rows by using `:` we are limiting ourselves to a single column by putting an index. A single column with 5 rows is indistinguishable from a 1D vector with 5 values, that is why we got a horizontal layout instead of a vertical one; they confer the same meaning but another makes a more efficient use of space in the screen.
#### Verdict:
Partly correct - the dimension-dropping rule is right, but a 5-row column is *not* indistinguishable from a 1-D vector: `(5, 1)` and `(5,)` are different arrays that behave differently, and the horizontal printing is simply how `ndim == 1` is rendered, not a space-saving choice.

#### Explanation:
In basic indexing each integer index removes its axis and each slice keeps it, even a length-1 slice. Verified: `viajes[:, 0]` has shape `(5,)` while `viajes[:, 0:1]` has shape `(5, 1)`. NumPy has no row-vector/column-vector distinction at one dimension — orientation only exists once there are two axes to order.

The distinction bites in broadcasting. A `(5,)` array combined with a `(5, 1)` array does not pair elementwise; the shapes align from the right, the missing axis is filled with 1, and the result is `(5, 5)` — an outer product where an elementwise operation was intended, with no error raised.

### 20. What "indexación avanzada" names (coronel_ramirez_caso_numpy.ipynb - comment 28) [Mechanism]
#### User's Discovery/Doubt:
> I don't know what it refers to "indexacion avanzada" but I imagine I can concatenate several numpy arrays in order to get the data in the order asked. It is not a continous range for 3 reasons:
> 1. The data in here is intrinsecally discrete (both by the data type of integers and also the mere fact that it jumps from one day to the other; the samples are not being taken constantly)
> 2. We're breaking the chronological order
#### Verdict:
Partly correct - concatenation would reach the same values, but "advanced indexing" (also called fancy indexing) is a specific feature: subscripting with a sequence of integers or a boolean mask; and the reason a slice cannot express the selection is that a slice is an arithmetic progression, not that the underlying data is discrete.

#### Explanation:
The canonical forms are `a[[0, 2, 4]]`, `a[np.array([0, 2, 4])]` and `a[mask]` with a boolean array of matching length. Arbitrary order and repetition are allowed — `a[[4, 0, 4]]` is legal — which is precisely what your reason (2) requires, so no concatenation step is needed. Reason (1) is not operative: slices index positions, and positions are always discrete; `start:stop:step` can only express evenly spaced ones, so anything irregular needs advanced indexing.

One behaviour to keep: advanced indexing always returns a copy (verified), never a view, unlike basic slicing.

## Unprompted correction

### 21. `np.zeros` and `np.ones` produce float64 regardless of the array you are modelling (coronel_ramirez_caso_numpy.ipynb) [Mechanism]
#### Evidence in the code:
`reference = np.zeros((5, 3))` and `form = np.ones((5, 3))`, built as stand-ins for `viajes` immediately after checking that `viajes.dtype` is `int64`, with the outputs read as `0` and `30` when they print as `0.` and `30.`.
#### Verdict:
Wrong - the belief that a shape-constructed array picks up a sensible integer type, or that `30.` and `30` are the same thing here; `zeros`, `ones` and `empty` default to `float64` no matter what they are meant to mirror.

#### Explanation:
`dtype` is the second parameter of these constructors and defaults to `float`, so `np.zeros((5, 3), dtype=np.int64)` is the only way to get integers from them. Two costs follow. First, assignment into an existing array casts to *that array's* dtype and never promotes it, so writing a float array into an int one truncates silently under the same toward-zero rule as `astype` — verified, assigning `30.7` into an `int64` array stores `30` with no warning. Second, float accumulation is inexact, so a counter or a tally built on `ones()` can drift where an integer one cannot.

## Noted
- coronel_ramirez_caso_numpy.ipynb comment 0 - narration of the next step
- coronel_ramirez_caso_numpy.ipynb comment 13 - plan for the following cell, nothing asserted
- coronel_ramirez_caso_numpy.ipynb comment 25 - reaction to a failed prediction
- coronel_ramirez_caso_numpy.ipynb comment 27 (first, after the 2×2 output) - restatement of output already visible

## Not addressed
- none

## coronel_ramirez_caso_numpy.ipynb

### 22. Dimensionality reduction via integer indexing (coronel_ramirez_caso_numpy.ipynb - comments 22, 23) [Partly correct]

#### User's Discovery/Doubt:

> I forgot 0-indexing! I was actually one diagonal to the left to the real value.
> `viajes[:,0]` This means grab all the rows on the first column. This is all the times that the first route took in the given week. The expected output should be `[32, 37, 29, 42, 48]`
> I was right this time! The reason why is not a matrix is that while we are grabing all the rows by using `:` we are limiting ourselves to a single column by putting an index. A single column with 5 rows is indistinguishable from a 1D vector with 5 values, that is why we got a horizontal layout instead of a vertical one; they confer the same meaning but another makes a more efficient use of space in the screen.

#### Verdict:

Partly correct - returning a 1D array instead of a matrix happens specifically because you used an integer index for the column, not just because a single column mathematically resembles a vector.

#### Explanation:

In NumPy, basic indexing reduces the dimensionality of the returned array by one for every integer index used. Since `viajes` is 2D, slicing the rows with `:` keeps that dimension intact, but selecting the column with the integer `0` collapses the column dimension, resulting in a 1D array. If you wanted to extract a single column while preserving the 2D matrix structure, you would use a slice for both axes, such as `viajes[:, 0:1]`.

### 23. Slice upper bounds are exclusive (coronel_ramirez_caso_numpy.ipynb - comments 24, 25, 26) [Correct]

#### User's Discovery/Doubt:

> As we need the two first rows we should make use of `[:1]` assuming the upper bound is inclusive. For B and C we should make use of `[1:]`. The area selected is a 2x2 square that touches the upper right corner of the matrix.
> I got it wrong... Lets check the data again.
> It seems it is not inclusive, but why it isn't selecting all rows? Because that is what I want, I just need to move the expresion of the left

#### Verdict:

Correct - slice syntax in Python always excludes the upper bound limit.

### 24. Slices create views (coronel_ramirez_caso_numpy.ipynb - comments 27, 33) [Correct]

#### User's Discovery/Doubt:

> Indeed it work. It has a shape of (2, 2)
> Now even with slicing it didn't change... It makes sense. That I want to isolate part of the data doesn't mean that is the final version of how I want it to look. It seems that the change with slicing is only when I am assigning new data.
> Indeed this type of "change in the subset determines a change in the set" behavior that confused me deeply before. It seems that there are several mechanisms to why this can happen, but in general, it is simply that numpy instead of creating a whole new copy of an array (which can be extremely expensive to the memory) it simply provides a view of the whole array. I do wonder how could I create a literal copy of an array though

#### Verdict:

Correct - evaluating a slice provides a memory view of the original array, meaning mutations to the slice affect the source, but merely defining the slice does not alter the original data.

### 25. Array addition versus advanced indexing (coronel_ramirez_caso_numpy.ipynb - comments 28, 31, 32) [Partly correct]

#### User's Discovery/Doubt:

> I don't know what it refers to "indexacion avanzada" but I imagine I can concatenate several numpy arrays in order to get the data in the order asked. It is not a continous range for 3 reasons:

1. The data in here is intrinsecally discrete (both by the data type of integers and also the mere fact that it jumps from one day to the other; the samples are not being taken constantly)
2. We're breaking the chronological order...
... as we're putting Friday first, Monday next and Wendesday last.
3. Even if Monday, Wendesday and Friday were in the correct order we still have jumps in the data as we lack Tuesday and Thursday (we might even go that far to say we lack Saturday and Sunday too).

> That was not the output that I expected! `array([109, 137, 115])`. What I want is that the 3 separate rows join in that specific order. Now that I have checked it seems that advanced indexing is a way to obtain particular matrices by making use of integers or a mask. Maybe I can get the matrix requested by simply putting the order in which I want it
> It worked! it is important to note that there must be another square brackets inside the ones that accompany `viajes`, as without them it told me that I was trying to access 3 dimensions where my numpy array just had 2.

#### Verdict:

Partly correct - providing the desired order in a list extracts the rows exactly as you wanted, but the `+` operator failed because it performs element-wise mathematical addition rather than array concatenation.

#### Explanation:

When you added the `friday`, `monday`, and `wednesday` slices using `+`, NumPy broadcasted the arrays together, summing their values coordinate-by-coordinate to produce `[109, 137, 115]`. To combine separate arrays geometrically, you would use functions like `np.concatenate` or `np.vstack`. However, passing a list of integers like `[[4, 0, 2]]` triggers advanced indexing, which directly constructs a new array using the specified row indices in that exact order.

### 26. Boolean masking and indexing behavior (coronel_ramirez_caso_numpy.ipynb - comments 34, 35, 37) [Wrong]

#### User's Discovery/Doubt:

> First of all, `viajes[viajes > 45]` didn't had the behavior I thought it would. I expected a `(5, 3)` matrix (just like the shape of `viajes`) that had only 0s and 1s that represented how each value was compared to `45` and whether it was false or true that they were larger, in other words I expected... Why did I get a 1D array with all the values greater than 45 instead of the previous matrix?
> To be honest I am not sure why the origin doesn't change, but I believe that it is mainly for the reason of the shape change. While a new variable of a subsection is literally a view, with `viajes[viajes > 45]` I am asking a deliberate modification of the data, so in this case it makes sense that I shouldn't modify the origin, as we're talking about an array that completely changed its form and meaning.
> Indeed in this case while I modified the selection it didn't affect its "parent" (`subset`) nor its "grandparent" (`viajes`).

#### Verdict:

Wrong - the expression `viajes > 45` does create the exact boolean matrix you expected, but applying that matrix as an index flattens the matching elements into a 1D copy.

#### Explanation:

There are two separate steps happening. First, the condition `viajes > 45` evaluates the entire matrix, producing a 2D boolean mask of the same shape containing True and False. Second, when you place that mask inside the brackets `viajes[...]`, NumPy applies boolean array indexing. Because a mask can have True values scattered irregularly across dimensions, NumPy cannot guarantee the output will form a neat rectangular grid, so it extracts the matches and flattens them into a 1D array. Furthermore, boolean indexing always returns a fresh copy of the data rather than a view, which is why assigning zeros to `snd_selection` did not modify `subset` or `viajes`.

### 27. Scalar shapes (coronel_ramirez_caso_numpy.ipynb - comment 38) [Correct]

#### User's Discovery/Doubt:

> It selects the fourth row and third column. It has no shape as it is a scalar, it is the data of route C in Thursday and the view is simply 33

#### Verdict:

Correct - extracting a single numerical value via integer indexing on all axes yields a NumPy scalar, which has an empty tuple `()` for its shape.

### 28. Shape of a 1D boolean selection (coronel_ramirez_caso_numpy.ipynb - comment 40) [Partly correct]

#### User's Discovery/Doubt:

> `viajes[viajes > 45]` selects each of the values of the matrix that are greater than 45. Its shape is `(1, )`, it has no axes as it is a 1D vector and its view is `[46, 51, 48, 52]`. Now to test it out.

#### Verdict:

Partly correct - it is a 1D vector with no additional axes, but its shape is `(4,)` to reflect its four elements rather than `(1,)`.

#### Explanation:

In NumPy, the shape tuple indicates the number of items along each dimension. A shape of `(1,)` would mean a 1D array containing exactly one element. Since your boolean mask extracted four values, the size of that single dimension is 4.

### 29. Copying arrays (coronel_ramirez_caso_numpy.ipynb - comment 42) [Correct]

#### User's Discovery/Doubt:

> Indeed it was. This is the final of the first session and I use `.copy()` when I want to have a complete copy of the array in order to modify without cascading the changes to the original array.

#### Verdict:

Correct - calling `.copy()` creates a completely independent array in memory, severing the link to the original data.

## Unprompted correction

## Noted

* coronel_ramirez_caso_numpy.ipynb comments 39, 41 - narration and verification of shape outputs



## Not addressed

8 doubts written, 17 comments merged, 4 Correct, 3 Partly correct, 1 Wrong, 0 No prior assumption, ~600 words estimated, 29 last number used.
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

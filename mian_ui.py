"""
Numpy Analyzer - GUI version (Tkinter)
Run:  python numpy_analyzer_gui.py
Requires: numpy  (tkinter comes with Python)
"""

import tkinter as tk
from tkinter import ttk, messagebox

import numpy as np


class InputError(Exception):
    """Raised for any invalid user input (shown in a popup)."""


# ----------------------------------------------------------------------
# Logic layer (same features as the console version)
# ----------------------------------------------------------------------
class DataAnalytics:
    def __init__(self):
        self.arr = None
        self.result = None

    # ---------- validation helpers ----------
    @staticmethod
    def parse_ints(text):
        tokens = text.replace(",", " ").split()
        if not tokens:
            raise InputError("Please enter some elements.")
        try:
            return [int(t) for t in tokens]
        except ValueError:
            raise InputError("Enter integers only (separated by space or comma).")

    @staticmethod
    def parse_index(text, size, label):
        try:
            index = int(text.strip())
        except ValueError:
            raise InputError(f"{label}: invalid index!")
        if not (-size <= index < size):
            raise InputError(f"{label}: enter index between {-size} and {size - 1}.")
        return index

    @staticmethod
    def parse_range(text, size, label):
        try:
            start, end = map(int, text.strip().split(":"))
        except ValueError:
            raise InputError(f"{label}: invalid range! Example: 0:2")
        if not (-size <= start <= size and -size <= end <= size):
            raise InputError(f"{label}: enter range between {-size} and {size}.")
        if start > end:
            raise InputError(f"{label}: start cannot be greater than end!")
        return start, end

    def require_array(self):
        if self.arr is None:
            raise InputError("Please create an array first!")
        return self.arr

    def second_array(self, text, shape):
        elements = self.parse_ints(text)
        size = int(np.prod(shape))
        if len(elements) != size:
            raise InputError(
                f"Enter exactly {size} elements (you entered {len(elements)})."
            )
        return np.array(elements).reshape(shape)

    # ---------- features ----------
    def create(self, kind, dims, text):
        elements = self.parse_ints(text)
        total = int(np.prod(dims))
        if len(elements) != total:
            raise InputError(
                f"Enter exactly {total} elements (you entered {len(elements)})."
            )
        self.arr = np.array(elements).reshape(dims)
        return self.arr

    def index(self, texts):
        arr = self.require_array()
        names = {1: ["Index"], 2: ["Row", "Column"], 3: ["Layer", "Row", "Column"]}[
            arr.ndim
        ]
        idx = tuple(
            self.parse_index(t, arr.shape[i], names[i]) for i, t in enumerate(texts)
        )
        return arr[idx]

    def slice(self, texts):
        arr = self.require_array()
        names = {1: ["Index"], 2: ["Row", "Column"], 3: ["Layer", "Row", "Column"]}[
            arr.ndim
        ]
        slices = []
        for i, t in enumerate(texts):
            s, e = self.parse_range(t, arr.shape[i], names[i])
            slices.append(slice(s, e))
        return arr[tuple(slices)]


# ----------------------------------------------------------------------
# UI layer
# ----------------------------------------------------------------------
class App(tk.Tk):
    MATH_OPS = {
        "Addition": np.add,
        "Subtraction": np.subtract,
        "Multiplication": np.multiply,
        "Division": np.divide,
        "Dot Product": np.dot,
        "Matrix Multiplication": np.matmul,
    }
    FILTER_OPS = {
        "Greater than": np.greater,
        "Less than": np.less,
        "Equal to": np.equal,
    }
    STAT_OPS = {
        "Sum": np.sum,
        "Mean": np.mean,
        "Median": np.median,
        "Standard Deviation": np.std,
        "Variance": np.var,
        "Minimum": np.min,
        "Maximum": np.max,
        "Percentile": None,
        "Correlation Coefficient": None,
    }

    def __init__(self):
        super().__init__()
        self.title("Numpy Analyzer")
        self.geometry("1000x940")
        self.minsize(860, 760)

        self.engine = DataAnalytics()

        self._setup_style()
        self._build_header()
        self._build_notebook()
        self._build_output()
        self.refresh()

    # ------------------------------------------------------------------
    # Styling / layout
    # ------------------------------------------------------------------
    def _setup_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        self.configure(bg="#f3f4f6")
        style.configure("TFrame", background="#f3f4f6")
        style.configure("Card.TLabelframe", background="#ffffff")
        style.configure(
            "Card.TLabelframe.Label",
            background="#ffffff",
            font=("Segoe UI", 10, "bold"),
            foreground="#1f2937",
        )
        style.configure("Inner.TFrame", background="#ffffff")
        style.configure("TLabel", background="#f3f4f6", font=("Segoe UI", 10))
        style.configure("Inner.TLabel", background="#ffffff", font=("Segoe UI", 10))
        style.configure(
            "Hint.TLabel",
            background="#ffffff",
            foreground="#6b7280",
            font=("Segoe UI", 9, "italic"),
        )
        style.configure(
            "Title.TLabel",
            font=("Segoe UI", 18, "bold"),
            foreground="#111827",
            background="#f3f4f6",
        )
        style.configure("Sub.TLabel", foreground="#6b7280", background="#f3f4f6")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure(
            "Accent.TButton",
            font=("Segoe UI", 10, "bold"),
            foreground="#ffffff",
            background="#2563eb",
        )
        style.map("Accent.TButton", background=[("active", "#1d4ed8")])
        style.configure("TRadiobutton", background="#ffffff", font=("Segoe UI", 10))
        style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=(12, 6))

    def _build_header(self):
        header = ttk.Frame(self, padding=(16, 12, 16, 4))
        header.pack(fill="x")
        ttk.Label(header, text="Numpy Analyzer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            header,
            text="Create arrays, slice them, run maths, sort, filter and get statistics.",
            style="Sub.TLabel",
        ).pack(anchor="w")

        box = ttk.LabelFrame(
            self, text="Current Array", style="Card.TLabelframe", padding=8
        )
        box.pack(fill="x", padx=16, pady=(8, 4))
        self.array_label = tk.Label(
            box,
            text="",
            justify="left",
            anchor="w",
            font=("Consolas", 11),
            bg="#ffffff",
            fg="#111827",
        )
        self.array_label.pack(fill="x")

    def _build_notebook(self):
        self.nb = ttk.Notebook(self)
        self.nb.pack(fill="both", expand=False, padx=16, pady=6)

        self.tab_create = self._tab("1. Create Array")
        self.tab_index = self._tab("2. Index / Slice")
        self.tab_math = self._tab("3. Math Operations")
        self.tab_combine = self._tab("4. Combine / Split")
        self.tab_ssf = self._tab("5. Search / Sort / Filter")
        self.tab_stats = self._tab("6. Aggregates & Stats")

        self._build_create_tab()
        self._build_index_tab()
        self._build_math_tab()
        self._build_combine_tab()
        self._build_ssf_tab()
        self._build_stats_tab()

    def _tab(self, title):
        frame = ttk.Frame(self.nb, padding=12, style="Inner.TFrame")
        self.nb.add(frame, text=title)
        return frame

    def _build_output(self):
        box = ttk.LabelFrame(self, text="Output", style="Card.TLabelframe", padding=8)
        box.pack(fill="both", expand=True, padx=16, pady=(4, 6))

        self.output = tk.Text(
            box,
            height=24,
            wrap="none",
            font=("Consolas", 12),
            bg="#0f172a",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            relief="flat",
            padx=8,
            pady=8,
        )
        ysb = ttk.Scrollbar(box, orient="vertical", command=self.output.yview)
        xsb = ttk.Scrollbar(box, orient="horizontal", command=self.output.xview)
        self.output.configure(
            yscrollcommand=ysb.set, xscrollcommand=xsb.set, state="disabled"
        )
        self.output.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        box.rowconfigure(0, weight=1)
        box.columnconfigure(0, weight=1)

        bar = ttk.Frame(self, padding=(16, 0, 16, 10))
        bar.pack(fill="x")
        ttk.Button(bar, text="Clear Output", command=self.clear_output).pack(
            side="left"
        )
        ttk.Button(bar, text="Exit", command=self.destroy).pack(side="right")

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------
    def log(self, *parts):
        self.output.configure(state="normal")
        self.output.insert("end", " ".join(str(p) for p in parts) + "\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def log_block(self, title, value=None):
        self.log(f"\n--- {title} ---")
        if value is not None:
            self.log(value)

    def clear_output(self):
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.configure(state="disabled")

    def guarded(self, fn):
        """Run fn and show friendly popups on bad input."""
        try:
            fn()
        except InputError as e:
            messagebox.showwarning("Invalid input", str(e))
        except ValueError as e:
            messagebox.showerror("Operation cannot be performed", f"Reason: {e}")

    # ------------------------------------------------------------------
    # Refresh when array changes
    # ------------------------------------------------------------------
    def refresh(self):
        arr = self.engine.arr
        if arr is None:
            self.array_label.config(text="No array yet. Go to 'Create Array' tab.")
        else:
            self.array_label.config(
                text=f"Shape: {arr.shape}   |   {arr.ndim}D   |   Size: {arr.size}\n{arr}"
            )
        self._build_index_fields()
        self._update_math_hint()
        self._update_combine_hint()
        self._update_stats_state()

    # ------------------------------------------------------------------
    # Tab 1: Create array
    # ------------------------------------------------------------------
    def _build_create_tab(self):
        f = self.tab_create
        self.kind = tk.IntVar(value=1)

        row = ttk.Frame(f, style="Inner.TFrame")
        row.pack(anchor="w", pady=(0, 8))
        ttk.Label(row, text="Type of array:", style="Inner.TLabel").pack(
            side="left", padx=(0, 8)
        )
        for val, txt in ((1, "1D"), (2, "2D"), (3, "3D")):
            ttk.Radiobutton(
                row,
                text=txt,
                value=val,
                variable=self.kind,
                command=self._update_create_state,
            ).pack(side="left", padx=6)

        grid = ttk.Frame(f, style="Inner.TFrame")
        grid.pack(anchor="w", pady=4)

        self.sp_n = tk.IntVar(value=3)
        self.sp_layers = tk.IntVar(value=1)
        self.sp_rows = tk.IntVar(value=2)
        self.sp_cols = tk.IntVar(value=2)

        self.w_n = self._spin(grid, "Elements (1-10):", self.sp_n, 1, 10, 0)
        self.w_layers = self._spin(grid, "Layers (1-2):", self.sp_layers, 1, 2, 1)
        self.w_rows = self._spin(grid, "Rows:", self.sp_rows, 2, 6, 2)
        self.w_cols = self._spin(grid, "Columns:", self.sp_cols, 2, 6, 3)

        ttk.Label(
            f, text="Elements (space or comma separated):", style="Inner.TLabel"
        ).pack(anchor="w", pady=(10, 2))
        self.create_entry = ttk.Entry(f, font=("Consolas", 11))
        self.create_entry.pack(fill="x")
        self.create_hint = ttk.Label(f, text="", style="Hint.TLabel")
        self.create_hint.pack(anchor="w", pady=2)

        ttk.Button(
            f,
            text="Create Array",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_create),
        ).pack(anchor="w", pady=8)

        for var in (self.sp_n, self.sp_layers, self.sp_rows, self.sp_cols):
            var.trace_add("write", lambda *_: self._update_create_state())
        self._update_create_state()

    def _spin(self, parent, label, var, lo, hi, col):
        ttk.Label(parent, text=label, style="Inner.TLabel").grid(
            row=0, column=col * 2, padx=(0, 4), sticky="e"
        )
        sp = ttk.Spinbox(parent, from_=lo, to=hi, textvariable=var, width=5)
        sp.grid(row=0, column=col * 2 + 1, padx=(0, 14))
        return sp

    def _read_spin(self, var, lo, hi, label):
        try:
            v = int(var.get())
        except (tk.TclError, ValueError):
            raise InputError(f"{label}: enter a whole number.")
        if not lo <= v <= hi:
            raise InputError(f"{label}: enter value between {lo} and {hi}.")
        return v

    def _update_create_state(self):
        k = self.kind.get()
        self.w_n.configure(state="normal" if k == 1 else "disabled")
        self.w_layers.configure(state="normal" if k == 3 else "disabled")
        self.w_rows.configure(state="normal" if k in (2, 3) else "disabled")
        self.w_cols.configure(state="normal" if k in (2, 3) else "disabled")
        # rows/cols limits differ for 3D
        if k == 3:
            self.w_rows.configure(from_=2, to=4)
            self.w_cols.configure(from_=2, to=4)
        else:
            self.w_rows.configure(from_=2, to=6)
            self.w_cols.configure(from_=2, to=6)
        try:
            dims = self._create_dims(validate=False)
            self.create_hint.config(
                text=f"Enter exactly {int(np.prod(dims))} integers."
            )
        except Exception:
            self.create_hint.config(text="")

    def _create_dims(self, validate=True):
        k = self.kind.get()
        if k == 1:
            return (self._read_spin(self.sp_n, 1, 10, "Elements"),)
        if k == 2:
            return (
                self._read_spin(self.sp_rows, 2, 6, "Rows"),
                self._read_spin(self.sp_cols, 2, 6, "Columns"),
            )
        return (
            self._read_spin(self.sp_layers, 1, 2, "Layers"),
            self._read_spin(self.sp_rows, 2, 4, "Rows"),
            self._read_spin(self.sp_cols, 2, 4, "Columns"),
        )

    def do_create(self):
        dims = self._create_dims()
        arr = self.engine.create(self.kind.get(), dims, self.create_entry.get())
        self.refresh()
        self.log_block("Array created successfully", arr)

    # ------------------------------------------------------------------
    # Tab 2: Index / Slice
    # ------------------------------------------------------------------
    def _build_index_tab(self):
        f = self.tab_index
        self.idx_mode = tk.IntVar(value=1)

        row = ttk.Frame(f, style="Inner.TFrame")
        row.pack(anchor="w", pady=(0, 8))
        ttk.Label(row, text="Operation:", style="Inner.TLabel").pack(
            side="left", padx=(0, 8)
        )
        ttk.Radiobutton(
            row,
            text="Indexing",
            value=1,
            variable=self.idx_mode,
            command=self._build_index_fields,
        ).pack(side="left", padx=6)
        ttk.Radiobutton(
            row,
            text="Slicing",
            value=2,
            variable=self.idx_mode,
            command=self._build_index_fields,
        ).pack(side="left", padx=6)

        self.idx_fields = ttk.Frame(f, style="Inner.TFrame")
        self.idx_fields.pack(anchor="w", fill="x")
        self.idx_entries = []

        ttk.Button(
            f,
            text="Apply",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_index_slice),
        ).pack(anchor="w", pady=8)

    def _build_index_fields(self):
        for w in self.idx_fields.winfo_children():
            w.destroy()
        self.idx_entries = []

        arr = self.engine.arr
        if arr is None:
            ttk.Label(
                self.idx_fields, text="Create an array first.", style="Hint.TLabel"
            ).pack(anchor="w")
            return

        names = {1: ["Index"], 2: ["Row", "Column"], 3: ["Layer", "Row", "Column"]}[
            arr.ndim
        ]
        slicing = self.idx_mode.get() == 2
        for i, name in enumerate(names):
            size = arr.shape[i]
            if slicing:
                label = f"{name} range (start:end), valid {-size}..{size}"
                default = f"0:{size}"
            else:
                label = f"{name} index, valid {-size}..{size - 1}"
                default = "0"
            ttk.Label(self.idx_fields, text=label + ":", style="Inner.TLabel").grid(
                row=i, column=0, sticky="e", padx=(0, 8), pady=3
            )
            e = ttk.Entry(self.idx_fields, width=14, font=("Consolas", 11))
            e.insert(0, default)
            e.grid(row=i, column=1, sticky="w", pady=3)
            self.idx_entries.append(e)

    def do_index_slice(self):
        self.engine.require_array()
        texts = [e.get() for e in self.idx_entries]
        if self.idx_mode.get() == 1:
            value = self.engine.index(texts)
            self.log_block("Indexing", f"Array:\n{self.engine.arr}\nValue: {value}")
        else:
            sliced = self.engine.slice(texts)
            self.log_block(
                "Slicing", f"Array:\n{self.engine.arr}\nSliced Array:\n{sliced}"
            )

    # ------------------------------------------------------------------
    # Tab 3: Math operations
    # ------------------------------------------------------------------
    def _build_math_tab(self):
        f = self.tab_math

        row = ttk.Frame(f, style="Inner.TFrame")
        row.pack(anchor="w", pady=(0, 6))
        ttk.Label(row, text="Operation:", style="Inner.TLabel").pack(
            side="left", padx=(0, 8)
        )
        self.math_choice = ttk.Combobox(
            row, values=list(self.MATH_OPS), state="readonly", width=24
        )
        self.math_choice.current(0)
        self.math_choice.pack(side="left")
        self.math_choice.bind(
            "<<ComboboxSelected>>", lambda _e: self._update_math_hint()
        )

        self.math_cols_var = tk.IntVar(value=2)
        self.math_cols_row = ttk.Frame(f, style="Inner.TFrame")
        ttk.Label(
            self.math_cols_row,
            text="Columns of second array (1-6):",
            style="Inner.TLabel",
        ).pack(side="left", padx=(0, 8))
        ttk.Spinbox(
            self.math_cols_row,
            from_=1,
            to=6,
            textvariable=self.math_cols_var,
            width=5,
            command=self._update_math_hint,
        ).pack(side="left")
        self.math_cols_var.trace_add("write", lambda *_: self._update_math_hint())

        self.math_entry_label = ttk.Label(
            f, text="Second array elements:", style="Inner.TLabel"
        )
        self.math_entry_label.pack(anchor="w", pady=(10, 2))
        self.math_entry = ttk.Entry(f, font=("Consolas", 11))
        self.math_entry.pack(fill="x")
        self.math_hint = ttk.Label(f, text="", style="Hint.TLabel")
        self.math_hint.pack(anchor="w", pady=2)

        ttk.Button(
            f,
            text="Calculate",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_math),
        ).pack(anchor="w", pady=8)

    def _is_matrix_op(self):
        return self.math_choice.get() in ("Dot Product", "Matrix Multiplication")

    def _update_math_hint(self):
        if self._is_matrix_op():
            self.math_cols_row.pack(anchor="w", pady=4, before=self.math_entry_label)
        else:
            self.math_cols_row.pack_forget()

        arr = self.engine.arr
        if arr is None:
            self.math_hint.config(text="Create an array first.")
            return
        if self._is_matrix_op():
            if arr.ndim != 2:
                self.math_hint.config(
                    text="Dot Product / Matrix Multiplication require a 2D array!"
                )
                return
            try:
                cols = int(self.math_cols_var.get())
            except (tk.TclError, ValueError):
                return
            self.math_hint.config(
                text=f"Second array shape: {arr.shape[1]} x {cols} -> enter {arr.shape[1] * cols} integers."
            )
        else:
            self.math_hint.config(
                text=f"Second array has the same shape {arr.shape} -> enter {arr.size} integers."
            )

    def do_math(self):
        arr = self.engine.require_array()
        name = self.math_choice.get()
        operation = self.MATH_OPS[name]

        if self._is_matrix_op():
            if arr.ndim != 2:
                raise InputError(
                    "Dot Product and Matrix Multiplication require 2D arrays!"
                )
            cols = self._read_spin(self.math_cols_var, 1, 6, "Columns")
            second = self.engine.second_array(
                self.math_entry.get(), (arr.shape[1], cols)
            )
        else:
            second = self.engine.second_array(self.math_entry.get(), arr.shape)

        if name == "Division" and np.any(second == 0):
            raise InputError("Division by zero is not allowed!")

        self.engine.result = operation(arr, second)
        self.log_block(
            name,
            f"Original Array:\n{arr}\n\nSecond Array:\n{second}\n\nResult:\n{self.engine.result}",
        )

    # ------------------------------------------------------------------
    # Tab 4: Combine / split
    # ------------------------------------------------------------------
    def _build_combine_tab(self):
        f = self.tab_combine

        box1 = ttk.LabelFrame(
            f, text="Combine Arrays", style="Card.TLabelframe", padding=8
        )
        box1.pack(fill="x", pady=(0, 8))

        row = ttk.Frame(box1, style="Inner.TFrame")
        row.pack(anchor="w")
        ttk.Label(row, text="Stacking:", style="Inner.TLabel").pack(
            side="left", padx=(0, 8)
        )
        self.stack_choice = ttk.Combobox(
            row,
            values=["Vertical Stack", "Horizontal Stack"],
            state="readonly",
            width=20,
        )
        self.stack_choice.current(0)
        self.stack_choice.pack(side="left")

        ttk.Label(box1, text="Second array elements:", style="Inner.TLabel").pack(
            anchor="w", pady=(8, 2)
        )
        self.combine_entry = ttk.Entry(box1, font=("Consolas", 11))
        self.combine_entry.pack(fill="x")
        self.combine_hint = ttk.Label(box1, text="", style="Hint.TLabel")
        self.combine_hint.pack(anchor="w", pady=2)
        ttk.Button(
            box1,
            text="Combine",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_combine),
        ).pack(anchor="w", pady=4)

        box2 = ttk.LabelFrame(
            f, text="Split Array", style="Card.TLabelframe", padding=8
        )
        box2.pack(fill="x")
        ttk.Label(
            box2,
            text="Splits the array into 3 parts (np.array_split).",
            style="Hint.TLabel",
        ).pack(anchor="w")
        ttk.Button(
            box2, text="Split into 3", command=lambda: self.guarded(self.do_split)
        ).pack(anchor="w", pady=4)

    def _update_combine_hint(self):
        arr = self.engine.arr
        if arr is None:
            self.combine_hint.config(text="Create an array first.")
        else:
            self.combine_hint.config(
                text=f"Second array has the same shape {arr.shape} -> enter {arr.size} integers."
            )

    def do_combine(self):
        arr = self.engine.require_array()
        second = self.engine.second_array(self.combine_entry.get(), arr.shape)
        name = self.stack_choice.get()
        func = np.vstack if name == "Vertical Stack" else np.hstack
        try:
            self.engine.result = func((arr, second))
        except ValueError as e:
            raise InputError(f"Arrays cannot be combined!\nReason: {e}")
        self.log_block(
            f"Combined Array ({name})",
            f"Original Array:\n{arr}\n\nSecond Array:\n{second}\n\nResult:\n{self.engine.result}",
        )

    def do_split(self):
        arr = self.engine.require_array()
        parts = np.array_split(arr, 3)
        text = "\n".join(f"Part {i + 1}:\n{p}\n" for i, p in enumerate(parts))
        self.log_block("Split Array", f"Original Array:\n{arr}\n\n{text}")

    # ------------------------------------------------------------------
    # Tab 5: Search / Sort / Filter
    # ------------------------------------------------------------------
    def _build_ssf_tab(self):
        f = self.tab_ssf

        # search
        s = ttk.LabelFrame(
            f, text="Search a value", style="Card.TLabelframe", padding=8
        )
        s.pack(fill="x", pady=(0, 6))
        ttk.Label(s, text="Value:", style="Inner.TLabel").pack(side="left", padx=(0, 6))
        self.search_entry = ttk.Entry(s, width=12, font=("Consolas", 11))
        self.search_entry.pack(side="left", padx=(0, 8))
        ttk.Button(
            s,
            text="Search",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_search),
        ).pack(side="left")

        # sort
        so = ttk.LabelFrame(
            f,
            text="Sort the array (along last axis)",
            style="Card.TLabelframe",
            padding=8,
        )
        so.pack(fill="x", pady=6)
        ttk.Button(
            so,
            text="Ascending",
            command=lambda: self.guarded(lambda: self.do_sort(True)),
        ).pack(side="left", padx=(0, 8))
        ttk.Button(
            so,
            text="Descending",
            command=lambda: self.guarded(lambda: self.do_sort(False)),
        ).pack(side="left")

        # filter
        fi = ttk.LabelFrame(
            f, text="Filter values", style="Card.TLabelframe", padding=8
        )
        fi.pack(fill="x", pady=6)
        ttk.Label(fi, text="Condition:", style="Inner.TLabel").pack(
            side="left", padx=(0, 6)
        )
        self.filter_choice = ttk.Combobox(
            fi, values=list(self.FILTER_OPS), state="readonly", width=14
        )
        self.filter_choice.current(0)
        self.filter_choice.pack(side="left", padx=(0, 10))
        ttk.Label(fi, text="Value:", style="Inner.TLabel").pack(
            side="left", padx=(0, 6)
        )
        self.filter_entry = ttk.Entry(fi, width=12, font=("Consolas", 11))
        self.filter_entry.pack(side="left", padx=(0, 8))
        ttk.Button(
            fi,
            text="Filter",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_filter),
        ).pack(side="left")

    @staticmethod
    def _int_from(entry, label="Value"):
        try:
            return int(entry.get().strip())
        except ValueError:
            raise InputError(f"{label}: invalid value entered!")

    def do_search(self):
        arr = self.engine.require_array()
        value = self._int_from(self.search_entry)
        positions = np.argwhere(arr == value).tolist()
        if positions:
            self.log_block(
                f"Search {value}",
                f"Original Array:\n{arr}\nValue found at index (position list): {positions}",
            )
        else:
            self.log_block(f"Search {value}", "Value not found in array !!")

    def do_sort(self, ascending):
        arr = self.engine.require_array()
        result = np.sort(arr, axis=-1)
        if not ascending:
            result = result[..., ::-1]
        self.engine.result = result
        name = "Ascending" if ascending else "Descending"
        self.log_block(
            f"Sorted array ({name})", f"Original Array:\n{arr}\n\nSorted:\n{result}"
        )

    def do_filter(self):
        arr = self.engine.require_array()
        value = self._int_from(self.filter_entry)
        name = self.filter_choice.get()
        self.engine.result = arr[self.FILTER_OPS[name](arr, value)]
        if self.engine.result.size:
            self.log_block(
                f"Values {name} {value}",
                f"Original Array:\n{arr}\n\nResult: {self.engine.result}",
            )
        else:
            self.log_block(f"Filter {name} {value}", "No values found!")

    # ------------------------------------------------------------------
    # Tab 6: Aggregates & statistics
    # ------------------------------------------------------------------
    def _build_stats_tab(self):
        f = self.tab_stats

        row = ttk.Frame(f, style="Inner.TFrame")
        row.pack(anchor="w", pady=(0, 6))
        ttk.Label(row, text="Function:", style="Inner.TLabel").pack(
            side="left", padx=(0, 8)
        )
        self.stat_choice = ttk.Combobox(
            row, values=list(self.STAT_OPS), state="readonly", width=26
        )
        self.stat_choice.current(0)
        self.stat_choice.pack(side="left")
        self.stat_choice.bind(
            "<<ComboboxSelected>>", lambda _e: self._update_stats_state()
        )

        prow = ttk.Frame(f, style="Inner.TFrame")
        prow.pack(anchor="w", pady=4)
        ttk.Label(prow, text="Percentile (0-100):", style="Inner.TLabel").pack(
            side="left", padx=(0, 6)
        )
        self.percentile_var = tk.IntVar(value=50)
        self.percentile_spin = ttk.Spinbox(
            prow, from_=0, to=100, textvariable=self.percentile_var, width=6
        )
        self.percentile_spin.pack(side="left")

        ttk.Label(
            f, text="Second array elements (for Correlation):", style="Inner.TLabel"
        ).pack(anchor="w", pady=(8, 2))
        self.stats_entry = ttk.Entry(f, font=("Consolas", 11))
        self.stats_entry.pack(fill="x")
        self.stats_hint = ttk.Label(f, text="", style="Hint.TLabel")
        self.stats_hint.pack(anchor="w", pady=2)

        ttk.Button(
            f,
            text="Compute",
            style="Accent.TButton",
            command=lambda: self.guarded(self.do_stats),
        ).pack(anchor="w", pady=8)

    def _update_stats_state(self):
        name = self.stat_choice.get()
        self.percentile_spin.configure(
            state="normal" if name == "Percentile" else "disabled"
        )
        self.stats_entry.configure(
            state="normal" if name == "Correlation Coefficient" else "disabled"
        )
        arr = self.engine.arr
        if name == "Correlation Coefficient" and arr is not None:
            self.stats_hint.config(
                text=f"Enter {arr.size} integers (same size as current array)."
            )
        else:
            self.stats_hint.config(text="")

    def do_stats(self):
        arr = self.engine.require_array()
        name = self.stat_choice.get()

        if name == "Percentile":
            q = self._read_spin(self.percentile_var, 0, 100, "Percentile")
            self.engine.result = np.percentile(arr, q)
            self.log_block(
                f"{q}th Percentile",
                f"Original Array:\n{arr}\n\nResult: {self.engine.result}",
            )

        elif name == "Correlation Coefficient":
            second = self.engine.second_array(self.stats_entry.get(), arr.shape)
            with np.errstate(all="ignore"):
                self.engine.result = np.corrcoef(arr.flatten(), second.flatten())
            self.log_block(
                "Correlation Coefficient",
                f"Original Array:\n{arr}\n\nSecond Array:\n{second}\n\n"
                f"Correlation matrix:\n{self.engine.result}",
            )

        else:
            self.engine.result = self.STAT_OPS[name](arr)
            self.log_block(
                f"{name} of all values",
                f"Original Array:\n{arr}\n\nResult: {self.engine.result}",
            )


if __name__ == "__main__":
    App().mainloop()

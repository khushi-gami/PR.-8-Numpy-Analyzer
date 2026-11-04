# PR.-8-Numpy-Analyzer 🧮

A menu-driven Python project built using **NumPy** to create, manipulate, analyze, and perform mathematical and statistical operations on 1D, 2D, and 3D arrays.

The project provides an interactive interface where users can create NumPy arrays and perform various operations such as indexing, slicing, mathematical calculations, combining, splitting, searching, sorting, filtering, aggregation, and statistical analysis.

## 📌 Project Overview

The **NumPy Analyzer** is designed to practice and demonstrate the practical implementation of NumPy concepts through a single menu-driven application.

Users can create arrays of different dimensions and perform operations on them using an interactive command-line menu.

### Key Highlights

- Create 1D, 2D, and 3D NumPy arrays.
- Perform indexing and slicing.
- Execute mathematical operations between arrays.
- Combine and split arrays.
- Search for specific elements.
- Sort arrays in ascending and descending order.
- Filter array elements using conditions.
- Calculate aggregate values and statistical measurements.
- Validate user inputs to reduce invalid operations.
- Use Object-Oriented Programming (OOP) to organize the application.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| NumPy | Array creation and numerical operations |
| OOP | Organizing functionality using classes and methods |
| Exception Handling | Handling invalid user inputs |

---

## 📂 Project Structure

```
PR. 8 NumPy Analyzer/
│
├── main.py
│
└── main_ui.py
│
└── README.md

```

## 🚀 Features & Implementation Logic

### 1. Array Creation

Allows users to create arrays in three different dimensions:

- 1D Array
- 2D Array
- 3D Array

**Implementation Logic:**

1. Display a menu to select the required array dimension.
2. Accept the user's choice using the `int_input()` function.
3. Ask the user to enter the required dimensions.
4. Collect array elements from the user using space-separated input.
5. Convert the entered values into integers using `map(int, ...)`.
6. Validate whether the number of entered elements matches the required size.
7. Convert the elements into a NumPy array using `np.array()`.
8. For 2D and 3D arrays, reshape the array using `.reshape()`.
9. Store the newly created array in the private attribute `self.__arr`.
10. Display the successfully created array.

**NumPy Functions Used:**

- `np.array()`
- `.reshape()`

**Example:**

```python
arr = np.array([10, 20, 30, 40])
```

For a 2D array:

```python
arr = np.array([1, 2, 3, 4, 5, 6]).reshape(2, 3)
```

Output:

```text
[[1 2 3]
 [4 5 6]]
```

For a 3D array:

```python
arr = np.array([1, 2, 3, 4, 5, 6, 7, 8]).reshape(2, 2, 2)
```
---

### 2. Indexing and Slicing

Allows users to access individual elements and extract portions of arrays.

#### A. Indexing

**Implementation Logic:**

1. Check whether an array has been created.
2. Identify the array dimension using `arr.ndim`.
3. Accept the required index from the user.
4. Validate the index according to the size of the corresponding dimension.
5. Access and display the requested element.

**Supported Dimensions:**

- 1D: `arr[index]`
- 2D: `arr[row, column]`
- 3D: `arr[layer, row, column]`

Negative indexing is also supported.

**Example:**

```python
arr = np.array([10, 20, 30, 40])

print(arr[-1])
```

Output:

```text
40
```

#### B. Slicing

**Implementation Logic:**

1. Ask the user to enter the starting and ending indexes in `start:end` format.
2. Split the input using `.split(":")`.
3. Convert both values into integers.
4. Validate that both indexes are within the allowed range.
5. Check that the starting index is not greater than the ending index.
6. Apply slicing according to the array dimension.
7. Display the sliced array.

**Supported Slicing:**

```python
# 1D
arr[start:end]

# 2D
arr[row_start:row_end, col_start:col_end]

# 3D
arr[layer_start:layer_end,
    row_start:row_end,
    col_start:col_end]
```

**Example:**

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[1:4])
```

Output:

```text
[20 30 40]
```

---

### 3. Mathematical Operations

Allows users to perform mathematical calculations between two NumPy arrays.

**Available Operations:**

| Choice | Operation | NumPy Function |
|---|---|---|
| 1 | Addition | `np.add()` |
| 2 | Subtraction | `np.subtract()` |
| 3 | Multiplication | `np.multiply()` |
| 4 | Division | `np.divide()` |
| 5 | Dot Product | `np.dot()` |
| 6 | Matrix Multiplication | `np.matmul()` |

**Implementation Logic:**

1. Check whether the original array exists.
2. Display the mathematical operations menu.
3. Accept the user's choice.
4. Create a second array according to the selected operation.
5. For addition, subtraction, multiplication, and division:
   - Ask the user to enter the same number of elements as the original array.
   - Reshape the second array into the original array's shape.
6. For dot product and matrix multiplication:
   - Check whether the original array is 2D.
   - Ask the user to enter the number of columns for the second array.
   - Create a second 2D array with compatible dimensions.
7. Before division, check whether the second array contains zero.
8. Select the required NumPy operation using a dictionary.
9. Perform the operation and store the result in `self.result`.
10. Display both input arrays and the calculated result.

**Example:**

```python
arr1 = np.array([10, 20, 30])
arr2 = np.array([2, 4, 6])

result = np.add(arr1, arr2)

print(result)
```

Output:

```text
[12 24 36]
```

**Matrix Multiplication Example:**

```python
arr1 = np.array([[1, 2],
                 [3, 4]])

arr2 = np.array([[5, 6],
                 [7, 8]])

result = np.matmul(arr1, arr2)
```

Output:

```text
[[19 22]
 [43 50]]
```

---

### 4. Combining and Splitting Arrays

Allows users to combine two arrays or divide an existing array into multiple sub-arrays.

#### A. Combining Arrays

**Available Operations:**

| Operation | NumPy Function |
|---|---|
| Vertical Stack | `np.vstack()` |
| Horizontal Stack | `np.hstack()` |

**Implementation Logic:**

1. Check whether an original array exists.
2. Select the Combine Arrays option.
3. Choose vertical or horizontal stacking.
4. Accept a second array from the user.
5. Reshape the second array to match the original array's shape.
6. Select the stacking function using a dictionary.
7. Perform the stacking operation.
8. Handle incompatible array shapes using exception handling.
9. Display the combined result.

**Example:**

```python
arr1 = np.array([[1, 2],
                 [3, 4]])

arr2 = np.array([[5, 6],
                 [7, 8]])

result = np.vstack((arr1, arr2))
```

Output:

```text
[[1 2]
 [3 4]
 [5 6]
 [7 8]]
```

#### B. Splitting Arrays

**Implementation Logic:**

1. Select the Split Array option.
2. Pass the original array to `np.array_split()`.
3. Divide the array into three sub-arrays along axis 0.
4. Display the resulting sub-arrays.

**Example:**

```python
arr = np.array([10, 20, 30, 40, 50, 60])

result = np.array_split(arr, 3)
```

Output:

```text
[array([10, 20]),
 array([30, 40]),
 array([50, 60])]
```

---

### 5. Searching, Sorting, and Filtering

Provides three important array manipulation operations.

#### A. Searching

**Implementation Logic:**

1. Ask the user to enter a value.
2. Compare the entered value with every element using `arr == value`.
3. Use `np.any()` to check whether the value exists.
4. If the value exists, use `np.where()` to retrieve its index positions.
5. Otherwise, display a value-not-found message.

**Example:**

```python
arr = np.array([10, 20, 30, 20, 40])

result = np.where(arr == 20)

print(result)
```

Output:

```text
(array([1, 3]),)
```

#### B. Sorting

**Available Options:**

- Ascending Order
- Descending Order

**Implementation Logic:**

1. Ask the user to select the sorting order.
2. Use `np.sort()` to sort the array.
3. Set `axis=-1` to sort along the last axis.
4. For descending order, reverse the sorted values along the last axis using `[..., ::-1]`.
5. Store and display the sorted result.

**Example:**

```python
arr = np.array([40, 10, 30, 20])

ascending = np.sort(arr)
descending = np.sort(arr)[::-1]
```

Output:

```text
Ascending:  [10 20 30 40]
Descending: [40 30 20 10]
```

#### C. Filtering

Allows users to filter elements based on conditions.

**Available Conditions:**

| Condition | NumPy Function |
|---|---|
| Greater Than | `np.greater()` |
| Less Than | `np.less()` |
| Equal To | `np.equal()` |

**Implementation Logic:**

1. Ask the user to select a filtering condition.
2. Accept a comparison value.
3. Apply the selected comparison function to the original array.
4. Generate a Boolean array containing `True` and `False`.
5. Use the Boolean array as an index to filter the original array.
6. Store and display the filtered elements.
7. If no elements satisfy the condition, display an appropriate message.

**Example:**

```python
arr = np.array([10, 20, 30, 40, 50])

result = arr[np.greater(arr, 25)]

print(result)
```

Output:

```text
[30 40 50]
```

---

### 6. Aggregation and Statistical Functions

Allows users to calculate aggregate values and perform statistical analysis on an array.

#### A. Aggregating Functions

| Operation | NumPy Function | Purpose |
|---|---|---|
| Sum | `np.sum()` | Calculates the sum of all elements |
| Mean | `np.mean()` | Calculates the average |
| Median | `np.median()` | Finds the middle value |
| Standard Deviation | `np.std()` | Measures data dispersion |
| Variance | `np.var()` | Measures the spread of values |

**Implementation Logic:**

1. Select the Aggregating Functions option.
2. Display the available operations.
3. Accept the user's choice.
4. Select the corresponding NumPy function using a dictionary.
5. Apply the selected function to the original array.
6. Store the calculated result in `self.result`.
7. Display the result.

**Example:**

```python
arr = np.array([10, 20, 30, 40, 50])

print(np.sum(arr))
print(np.mean(arr))
print(np.median(arr))
print(np.std(arr))
print(np.var(arr))
```

#### B. Statistical Functions

| Operation | NumPy Function | Purpose |
|---|---|---|
| Minimum | `np.min()` | Returns the smallest element |
| Maximum | `np.max()` | Returns the largest element |
| Percentile | `np.percentile()` | Calculates a specified percentile |
| Correlation Coefficient | `np.corrcoef()` | Measures the correlation between two datasets |

**Implementation Logic:**

1. Select the Statistical Functions option.
2. Choose the required statistical operation.
3. For minimum and maximum:
   - Apply `np.min()` or `np.max()` to the original array.
4. For percentile:
   - Accept a percentile value between 0 and 100.
   - Apply `np.percentile(arr, q)`.
5. For correlation coefficient:
   - Accept a second array containing the same number of elements.
   - Flatten both arrays using `.flatten()`.
   - Calculate the correlation matrix using `np.corrcoef()`.
6. Display the calculated result.

**Example – Percentile:**

```python
arr = np.array([10, 20, 30, 40, 50])

result = np.percentile(arr, 50)

print(result)
```

Output:

```text
30.0
```

**Example – Correlation Coefficient:**

```python
arr1 = np.array([10, 20, 30, 40])
arr2 = np.array([20, 40, 60, 80])

result = np.corrcoef(arr1.flatten(), arr2.flatten())

print(result)
```

The output is a 2 × 2 correlation matrix.

---

## 🧠 Important Programming Concepts Used

This project implements several Python and NumPy programming concepts.

### 1. Object-Oriented Programming (OOP)

The complete application is organized inside the `DataAnalytics` class.

- **Constructor (`__init__`)**: Initializes the private array attribute and result variable.
- **Instance Methods**: Handle array creation, indexing, slicing, and other operations.
- **Static Method (`is_valid_array`)**: Checks whether the given object is a NumPy array with 1D, 2D, or 3D dimensions.
- **Class Method (`project_info`)**: Displays the project welcome message.
- **Getter Method (`get_arr`)**: Provides access to the stored array.
- **Private Attributes**: `self.__arr` stores the original array and restricts direct access through name mangling.

### 2. Input Validation

The custom `int_input()` function is used to accept integer inputs within a specified minimum and maximum range.

**Logic:**

1. Accept input from the user.
2. Convert it into an integer.
3. Check whether it falls within the permitted range.
4. If the value is invalid, display an error message.
5. Continue asking until a valid input is received.

### 3. Exception Handling

`try-except` blocks are used to handle invalid integer conversions and certain operations that may fail.

Examples:

- `ValueError` – Handles invalid integer input and incompatible array operations.
- Repeated input loops – Allow users to correct invalid entries without restarting the application.

### 4. Dictionaries for Operation Selection

Dictionaries are used to map menu choices to operation names and NumPy functions.

Example:

```python
math_operations = {
    1: ("Addition", np.add),
    2: ("Subtraction", np.subtract),
    3: ("Multiplication", np.multiply),
    4: ("Division", np.divide)
}
```

This approach reduces repetitive conditional statements and makes the code easier to maintain.

### 5. Loops and Conditional Statements

- `while` loops keep menus running until the user selects Go Back or Exit.
- `if-elif-else` statements handle menu choices and dimension-specific operations.
- `break` exits the current menu loop.
- `continue` skips the current iteration when input or conditions are invalid.
- `return` exits a method when an array has not been created.

### 6. NumPy Array Attributes

| Attribute | Purpose |
|---|---|
| `arr.ndim` | Returns the number of dimensions |
| `arr.shape` | Returns the dimensions of the array |
| `arr.size` | Returns the total number of elements |

### 7. NumPy Functions Used

| Function | Purpose |
|---|---|
| `np.array()` | Creates an array |
| `np.add()` | Addition |
| `np.subtract()` | Subtraction |
| `np.multiply()` | Multiplication |
| `np.divide()` | Division |
| `np.dot()` | Dot product |
| `np.matmul()` | Matrix multiplication |
| `np.vstack()` | Vertical stacking |
| `np.hstack()` | Horizontal stacking |
| `np.array_split()` | Splits an array |
| `np.any()` | Checks whether any condition is True |
| `np.where()` | Finds matching index positions |
| `np.sort()` | Sorts array elements |
| `np.greater()` | Greater-than comparison |
| `np.less()` | Less-than comparison |
| `np.equal()` | Equality comparison |
| `np.sum()` | Sum |
| `np.mean()` | Mean |
| `np.median()` | Median |
| `np.std()` | Standard deviation |
| `np.var()` | Variance |
| `np.min()` | Minimum |
| `np.max()` | Maximum |
| `np.percentile()` | Percentile |
| `np.corrcoef()` | Correlation coefficient |

---

## 🔄 Application Workflow

The application follows a menu-driven execution flow.

1. Import the NumPy library.
2. Initialize the `DataAnalytics` class.
3. Display the welcome message.
4. Show the main menu.
5. Ask the user to select an operation.
6. Execute the selected class method.
7. Validate the required inputs.
8. Perform the selected NumPy operation.
9. Display the result.
10. Return to the main menu.
11. Exit the application when the user selects option 7.

---

## 📋 Main Menu

```text
Welcome to the Numpy Analyzer !
========================================

Choose an option:

1. Create Numpy array
2. Indexing and slicing
3. Perform Mathematical Operations
4. Combine or Split Arrays
5. Search, Sort, or Filter Arrays
6. Compute Aggregates and Statistics
7. Exit

Enter your choice:
```

## 🎯 Learning Outcomes

By developing this project, I practiced and strengthened my understanding of:

- NumPy array creation and manipulation.
- Working with 1D, 2D, and 3D arrays.
- Indexing, slicing, and negative indexing.
- Mathematical operations and matrix calculations.
- Array stacking and splitting.
- Searching, sorting, and Boolean filtering.
- Aggregation and statistical functions.
- Python classes, methods, and encapsulation.
- Static methods and class methods.
- Dictionaries for operation mapping.
- Input validation and exception handling.
- Building an interactive menu-driven application.

---

**Developed as a Python and NumPy practice project.**

The main objective of this project is to apply NumPy concepts practically while improving Python programming, logical thinking, and problem-solving skills.
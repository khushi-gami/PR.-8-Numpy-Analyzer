import numpy as np

# for safe user input


def int_input(message, minimum, maximum):
    while True:
        try:
            number = int(input(message))
            if number < minimum or number > maximum:
                print(f"value enter between {minimum} and {maximum}.")
                print()
            else:
                return number
        except ValueError:
            print("Invalid value enterted !")
            print()


class DataAnalytics:

    def __init__(self):
        self.__arr = None
        self.result = None

    @staticmethod
    def is_valid_array(arr):
        return isinstance(arr, np.ndarray) and arr.ndim in (1, 2, 3)

    @classmethod
    def project_info(cls):
        print("\nWelcome to the Numpy Analyzer !")
        print("========================================")

    def get_arr(self):

        if self.is_valid_array(self.__arr):
            return self.__arr

    def __get_index(self, message, size):

        while True:
            try:
                index = int(input(message))

                if -size <= index < size:
                    return index

                else:
                    print(f"\nEnter index between {-size} and {size-1}.")

            except ValueError:
                print("\nInvalid index!")

    def __get_range(self, message, size):

        while True:
            try:
                start, end = map(int, input(message).split(":"))

                if not (-size <= start <= size and -size <= end <= size):
                    print(f"\nEnter range between {-size} and {size}.")
                    continue

                if start > end:
                    print("\nStart index cannot be greater than end index!")
                    continue

                return start, end

            except ValueError:
                print("\nInvalid range! Example: 0:2")

    def __get_second_array(self, arr):

        while True:
            try:
                elements = list(
                    map(int, input(f"\nEnter {arr.size} elements : ").split())
                )

                if len(elements) != arr.size:
                    print("\nEnter correct number of elements!")
                    continue

                return np.array(elements).reshape(arr.shape)

            except ValueError:
                print("\nEnter integers only!")

    def __get_matrix_array(self, rows):

        while True:
            try:
                cols = int_input("Enter number of columns for second array: ", 1, 6)

                total_elements = rows * cols

                elements = list(
                    map(int, input(f"Enter {total_elements} elements: ").split())
                )

                if len(elements) != total_elements:
                    print(f"Please enter exactly {total_elements} elements!")
                    continue

                return np.array(elements).reshape(rows, cols)

            except ValueError:
                print("Invalid input! Please enter integers only.")

    def create_array(self):

        print("Select the type of array to create : ")
        print("1. 1D Array")
        print("2. 2D Array")
        print("3. 3D Array")

        array_option = int_input("\nType of array : ", 1, 3)

        if array_option == 1:
            while True:
                try:
                    n = int_input("\nEnter number of elements : ", 1, 10)
                    elements_1d = list(
                        map(int, input(f"\nEnter {n} elements by Space : ").split())
                    )

                    if len(elements_1d) != n:
                        print("\nInvalid number of elements enterted !")
                    else:
                        self.__arr = np.array(elements_1d)
                        print("\narray created successfully !\n")
                        print(self.__arr)
                        break
                except ValueError:
                    print("\nInvalid value enterted !")
                    print()

        elif array_option == 2:
            while True:
                try:
                    rows = int_input("\nEnter number of rows : ", 2, 6)
                    cols = int_input("Enter number of columns : ", 2, 6)
                    elements_2d = list(
                        map(
                            int,
                            input(f"\nEnter {rows*cols} elements by Space : ").split(),
                        )
                    )

                    if len(elements_2d) != (rows * cols):
                        print("\nInvalid number of elements enterted !")
                    else:
                        self.__arr = np.array(elements_2d).reshape(rows, cols)
                        print("\narray created successfully !\n")
                        print(self.__arr)
                        break
                except ValueError:
                    print("\nInvalid value enterted !")

        elif array_option == 3:
            while True:
                try:
                    layers = int_input("\nEnter number of layers : ", 1, 2)
                    rows = int_input("Enter number of rows : ", 2, 4)
                    cols = int_input("Enter number of columns : ", 2, 4)
                    elements_3d = list(
                        map(
                            int,
                            input(
                                f"\nEnter {layers*rows*cols} elements by Space : "
                            ).split(),
                        )
                    )

                    if len(elements_3d) != (layers * rows * cols):
                        print("\nInvalid number of elements !")
                    else:
                        self.__arr = np.array(elements_3d).reshape(layers, rows, cols)
                        print("\narray created successfully !")
                        print(self.__arr)
                        break
                except ValueError:
                    print("\nInvalid value enterted !")

    def index_slice(self):

        arr = self.__arr

        if arr is None:
            print("\nPlease create an array first !")
            return

        while True:

            print("\nChoose an operation : ")
            print("1. Indexing")
            print("2. Slicing")
            print("3. Go Back")

            index_slice_option = int_input("\nEnter a option : ", 1, 3)

            if index_slice_option == 1:

                if arr.ndim == 1:

                    index = self.__get_index("\nEnter index: ", arr.shape[0])

                    print("\nYour array:\n", arr)
                    print("Value:", arr[index])

                elif arr.ndim == 2:

                    row = self.__get_index("\nEnter row index: ", arr.shape[0])
                    col = self.__get_index("Enter column index: ", arr.shape[1])

                    print("\nYour array:\n", arr)
                    print("Value:", arr[row, col])

                elif arr.ndim == 3:

                    layer = self.__get_index("\nEnter layer index: ", arr.shape[0])
                    row = self.__get_index("Enter row index: ", arr.shape[1])
                    col = self.__get_index("Enter column index: ", arr.shape[2])

                    print("\nYour array:\n", arr)
                    print("Value:", arr[layer, row, col])

            elif index_slice_option == 2:

                if arr.ndim == 1:

                    start, end = self.__get_range(
                        "\nEnter index range (start:end): ", arr.shape[0]
                    )

                    print("\nYour array:\n", arr)
                    print("Sliced Array:\n", arr[start:end])

                elif arr.ndim == 2:

                    row_start, row_end = self.__get_range(
                        "\nEnter row range (start:end): ", arr.shape[0]
                    )

                    col_start, col_end = self.__get_range(
                        "\nEnter column range (start:end): ", arr.shape[1]
                    )

                    print("\nYour array:\n", arr)
                    print("Sliced Array:\n", arr[row_start:row_end, col_start:col_end])

                elif arr.ndim == 3:

                    layer_start, layer_end = self.__get_range(
                        "Enter layer range (start:end): ", arr.shape[0]
                    )

                    row_start, row_end = self.__get_range(
                        "Enter row range (start:end): ", arr.shape[1]
                    )

                    col_start, col_end = self.__get_range(
                        "Enter column range (start:end): ", arr.shape[2]
                    )

                    print("\nYour array:\n", arr)
                    print(
                        "Sliced Array:\n",
                        arr[
                            layer_start:layer_end,
                            row_start:row_end,
                            col_start:col_end,
                        ],
                    )
                    print()

            elif index_slice_option == 3:
                break

    def mathematical_operations(self):

        arr = self.__arr

        if arr is None:
            print("Please create an array first!")
            return

        math_operations = {
            1: ("Addition", np.add),
            2: ("Subtraction", np.subtract),
            3: ("Multiplication", np.multiply),
            4: ("Division", np.divide),
            5: ("Dot Product", np.dot),
            6: ("Matrix Multiplication", np.matmul),
        }

        while True:

            print("Choose a mathematical operation : ")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Dot Product")
            print("6. Matrix Multiplication")
            print("7. Go Back")

            choice = int_input("Enter choice: ", 1, 7)

            if choice == 7:
                break

            if choice == 5 or choice == 6:

                if arr.ndim != 2:
                    print("\nDot Product and Matrix Multiplication require 2D arrays!")
                    continue

                second_arr = self.__get_matrix_array(arr.shape[1])

            else:
                second_arr = self.__get_second_array(arr)

            if choice == 4 and np.any(second_arr == 0):
                print("Division by zero is not allowed!")
                continue

            name, operation = math_operations[choice]

            try:
                self.result = operation(arr, second_arr)

                print(f"\nOriginal Array:\n{arr}")
                print(f"\nSecond Array:\n{second_arr}")
                print(f"\n{name}:\n{self.result}")

            except ValueError as e:
                print("\nOperation cannot be performed!")
                print("Reason:", e)

    def combine_split_arrays(self):

        arr = self.__arr

        if arr is None:
            print("Please create an array first!")
            return

        stack_operations = {
            1: ("Vertical Stack", np.vstack),
            2: ("Horizontal Stack", np.hstack),
        }

        while True:

            print("\nChoose an option:")
            print("1. Combine Arrays")
            print("2. Split Array")
            print("3. Go Back")

            choice = int_input("Enter choice: ", 1, 3)

            if choice == 1:

                while True:

                    print("\nChoose stacking option:")
                    print("1. Vertical Stack")
                    print("2. Horizontal Stack")
                    print("3. Go Back")

                    stack_choice = int_input("Enter choice: ", 1, 3)

                    if stack_choice == 3:
                        break

                    second_arr = self.__get_second_array(arr)

                    name, operation = stack_operations[stack_choice]

                    try:
                        self.result = operation((arr, second_arr))

                        print("\nOriginal Array:\n", arr)
                        print("\nSecond Array:\n", second_arr)
                        print(f"\nCombined Array ({name}):\n", self.result)

                    except ValueError as e:
                        print("\nArrays cannot be combined!")
                        print("Reason:", e)

            elif choice == 2:

                print("\nOriginal Array:\n", arr)
                print("\nSplitting Array:\n", np.array_split(arr, 3))

            elif choice == 3:
                break

    def search_sort_filter(self):

        arr = self.__arr
        if arr is None:
            print("\nPlease create an array first !")
            return

        while True:
            print("\nChoose an option : ")
            print("1. Search a value")
            print("2. Sort the array")
            print("3. Filter values")
            print("4. Go Back")

            search_sort_filter_option = int_input("\nEnter a option : ", 1, 4)

            if search_sort_filter_option == 1:
                while True:
                    try:
                        value = int(input("\nEnter value to search : "))

                        if np.any(arr == value):
                            print("\nOriginal Array :\n", arr)
                            print("\nValue found at index : ", np.where(arr == value))
                        else:
                            print("\nValue not found in array !!")
                        break
                    except ValueError:
                        print("\nInvalid value enterted !")

            elif search_sort_filter_option == 2:

                sort_operation = {
                    1: ("Ascending", lambda x: np.sort(x, axis=-1)),
                    2: ("Descending", lambda x: np.sort(x, axis=-1)[..., ::-1]),
                }

                while True:

                    print("\nChoose sorting order : ")
                    print("1. Ascending")
                    print("2. Descending")
                    print("3. Go back")

                    sort_choice = int_input("\nEnter a option : ", 1, 3)

                    if sort_choice == 3:
                        break

                    name, operation = sort_operation[sort_choice]

                    self.result = operation(arr)

                    print("\nOriginal Array :\n", arr)
                    print(f"\nSorted array ({name}) :\n", self.result)

            elif search_sort_filter_option == 3:

                filter_operation = {
                    1: ("Greater than", np.greater),
                    2: ("Less than", np.less),
                    3: ("Equal to", np.equal),
                }

                while True:

                    print("\nChoose a condition : ")
                    print("1. Greater than")
                    print("2. Less than")
                    print("3. Equal to")
                    print("4. Go back")

                    filter_option = int_input("\nEnter a option : ", 1, 4)

                    if filter_option == 4:
                        break

                    try:
                        value = int(input("Enter value : "))

                        name, operation = filter_operation[filter_option]

                        self.result = arr[operation(arr, value)]

                        print("\nOriginal Array :\n", arr)
                        print(
                            f"\n Values {name} {value} : {self.result}"
                            if self.result.size
                            else f"\n No values found {name} {value} !"
                        )

                    except ValueError:
                        print("\n Invalid value enterted !")

            elif search_sort_filter_option == 4:
                break

    def compute_aggregation_statistics(self):

        arr = self.__arr

        if arr is None:
            print("\nPlease create an array first!")
            return

        while True:

            print("\nChoose an option:")
            print("1. Aggregating Functions")
            print("2. Statistical Functions")
            print("3. Go Back")

            agg_stats_option = int_input("Enter an option: ", 1, 3)

            if agg_stats_option == 1:

                aggregate_operations = {
                    1: ("Sum", np.sum),
                    2: ("Mean", np.mean),
                    3: ("Median", np.median),
                    4: ("Standard Deviation", np.std),
                    5: ("Variance", np.var),
                }

                while True:

                    print("\nChoose an aggregate operation:")
                    print("1. Sum")
                    print("2. Mean")
                    print("3. Median")
                    print("4. Standard Deviation")
                    print("5. Variance")
                    print("6. Go Back")

                    agg_option = int_input("Enter an option: ", 1, 6)

                    if agg_option == 6:
                        break

                    name, operation = aggregate_operations[agg_option]

                    self.result = operation(arr)

                    print("\nOriginal Array:\n", arr)
                    print(f"\n{name} of all values: ", self.result)

            # Statistical Functions
            elif agg_stats_option == 2:

                statistical_operations = {
                    1: ("Minimum", np.min),
                    2: ("Maximum", np.max),
                }

                while True:

                    print("\nChoose a statistical operation:")
                    print("1. Minimum")
                    print("2. Maximum")
                    print("3. Percentile")
                    print("4. Correlation Coefficient")
                    print("5. Go Back")

                    stats_option = int_input("Enter an option: ", 1, 5)

                    if stats_option == 5:
                        break

                    # Minimum and Maximum
                    elif stats_option == 1 or stats_option == 2:

                        name, operation = statistical_operations[stats_option]

                        self.result = operation(arr)

                        print("\nOriginal Array:\n", arr)
                        print(f"\n{name} value: ", self.result)

                    # Percentile
                    elif stats_option == 3:

                        q = int_input("Enter percentile (0-100): ", 0, 100)

                        self.result = np.percentile(arr, q)

                        print("\nOriginal Array:\n", arr)
                        print(f"\n{q}th Percentile: ", self.result)

                    # Correlation Coefficient
                    elif stats_option == 4:

                        second_arr = self.__get_second_array(arr)

                        self.result = np.corrcoef(arr.flatten(), second_arr.flatten())

                        print("\nOriginal Array:\n", arr)
                        print("\nSecond Array:\n", second_arr)
                        print("\nCorrelation Coefficient:\n", self.result)

            elif agg_stats_option == 3:
                break


analytics = DataAnalytics()


def main():

    DataAnalytics.project_info()

    while True:

        print("\nChoose an option : ")
        print("1. Create Numpy array")
        print("2. Indexing and slicing")
        print("3. Perform Mathematical Operations")
        print("4. Combine or Split Arrays")
        print("5. Search, Sort, or Filter Arrays")
        print("6. Compute Aggregates and Statistics")
        print("7. Exit")
        print()

        main_option = int_input("Enter your choice : ", 1, 7)

        if main_option == 1:
            analytics.create_array()

        elif main_option == 2:
            analytics.index_slice()

        elif main_option == 3:
            analytics.mathematical_operations()

        elif main_option == 4:
            analytics.combine_split_arrays()

        elif main_option == 5:
            analytics.search_sort_filter()

        elif main_option == 6:
            analytics.compute_aggregation_statistics()

        elif main_option == 7:

            print("Thank you for using the Numpy Analyzer! Goodbye!")

            break


if __name__ == "__main__":
    main()

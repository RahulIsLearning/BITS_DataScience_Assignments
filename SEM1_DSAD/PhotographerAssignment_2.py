# Problem Statment:-
# A famous product photographer Xavier is in high demand and is being approached by various
# companies to get their products photographed. Xavier does all of this product shoots at his studio and
# wants to make sure that he maximizes his returns by covering as many photoshoots in a day as
# possible. For a product shoot to be conducted, the product first has to be staged and then
# photographed. He has a team who stages the products and he does the photoshoots. Depending on
# the product, it takes different amounts of time to stage and varied time to complete the shoot. His team
# can stage another product in another part of the studio while Xavier is busy with a photoshoot of a
# previously staged product. Assuming that his team can work on only one product at a time before they
# move to staging another and Xavier also finishes one product photoshoot before moving to the next,
# you are expected to help Xavier make best use of his team and his time by deciding the order in which
# the products gets staged and photographed such that they finish the photoshoot of all products as
# quickly as possible.
# Requirements:
# 1. Formulate and effective algorithm using Greedy Method to arrange the product staging and
# photoshoot in such a way that total time taken for all products is minimized.
# 2. Analyse the time complexity of your algorithm.
# 3. Implement the above problem statement using Python 3.7


def partition(left, right, given_array):
    pivot, pointer = given_array[right], left
    for i in range(left, right):
        if given_array[i] <= pivot:
            given_array[i], given_array[pointer] = given_array[pointer], given_array[i]
            pointer += 1
    given_array[pointer], given_array[right] = given_array[right], given_array[pointer]
    return pointer


def quicksort(left, right, given_array):
    if len(given_array) == 1:
        return given_array
    if left < right:
        partition_index = partition(left, right, given_array)
        quicksort(left, partition_index - 1, given_array)
        quicksort(partition_index + 1, right, given_array)
    return given_array


def quicksort_array(given_array):
    given_array = list(given_array)
    return quicksort(0, len(given_array) - 1, given_array)


def get_Sorted_Array(product, stage_time, photo_time):
    # creating the tuple and sorting based on stage and photo time wrt Product client
    # sorting technique used is quick sort
    sorted_product = [x for y, z, x in quicksort_array(zip(stage_time, photo_time, product))]
    sorted_stage_time = [x for y, x in quicksort_array(zip(stage_time, stage_time))]
    sorted_photo_time = [x for y, z, x in quicksort_array(zip(stage_time, photo_time, photo_time))]
    return sorted_product, sorted_stage_time, sorted_photo_time


def processTime(stage_time, photo_time):
    total_waiting_time = 0      # initiate the total idle time for Xavier
    stage_complete = 0          # initiate the staging time for product client
    photo_complete = 0          # initiate the actual working time for Xavier

    for index in range(len(stage_time)):
        # Adding staging time for current product to total staging time
        stage_complete += int(stage_time[index])

        # checking if the staging time is greater than photo time so that Xavier should be idle
        if stage_complete > photo_complete:
            total_waiting_time += (stage_complete - photo_complete)
            photo_complete += (stage_complete - photo_complete)

        # Adding photo time for current product to total photo time
        photo_complete += int(photo_time[index])
    return total_waiting_time, photo_complete


if __name__ == "__main__":
    try:
        # Reading the values from input file
        input_file = open("inputPS7.txt", "r")
        records = input_file.readlines()
        product = list(map(lambda x: x.strip(), records.__getitem__(0).split(':')[1].strip().split('/')))
        stage_time = list(map(lambda x: x.strip(), records.__getitem__(1).split(':')[1].strip().split('/')))
        photo_time = list(map(lambda x: x.strip(), records.__getitem__(2).split(':')[1].strip().split('/')))
        if len(product) == len(stage_time) == len(photo_time):

            # getting the sorted array based on stage time and photo time
            (product_array, stage_time_array, photo_time_array) = get_Sorted_Array(product, stage_time, photo_time)

            # schedule the product client as per the order of staging time and photo time
            (waiting_time, photo_complete) = processTime(stage_time_array, photo_time_array)

            product_seq_str = "Product Sequence: " + ', '.join(product_array)
            total_time_str = "Total time to complete photoshoot: " + str(photo_complete) + " minutes"
            idle_time_str = "Idle time for Xavier: " + str(waiting_time) + " minutes"

            # creating the final result string
            final_str = product_seq_str + '\n' + total_time_str + '\n' + idle_time_str

            # Writing the result to output file
            write_File = open("outputPS7.txt", "w")
            write_File.write(final_str)
            write_File.close()
        else:
            raise ValueError("The length of product client, stage time and product time array should be same")
    except FileNotFoundError:
        print("File does not exist.")
    except Exception as ex:
        print("Exception occurred. ", ex)

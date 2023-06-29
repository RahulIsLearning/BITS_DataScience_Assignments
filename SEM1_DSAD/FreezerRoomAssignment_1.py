# Problem Statement:
# An organization has a unique freezer room with easy-to-adjust temperature, lock with
# keys, manual defrost option, and basket or adjustable shelf etc. Employees of this
# organization keep moving in and out of the freezer room on work. Organization uses a
# unique employee ID and smart card to identify their employee’s movement to the
# freezer room. Whenever the employee swipes his card to the freezer room employee ID
# is recorded. When an employee enters the room for the first time, the counter is set to 1.
# From then onwards, each time an employee swipes out of the room the counter is
# incremented and incremented again when he enters back. If the counter is odd, it
# means the employee is inside the freezer room and if the counter is even, it means
# he/she is out of the room.

# The organization uses this data to perform the following analytics:
# 1. How many employees entered the freezer room today?
# 2. Number of employees that have entered the freezer room today and are currently inside?
# 3. Check if a specific employee is inside the freezer room or outside?
# 4. List of employees that have swiped (in or out) more than x number of times?
# 5. Which employee ids within a range of IDs entered the freezer room, the swipe counter for
# them, and whether they are inside or outside the freezer room

###################################################################################################

# employee node.
# EmpId : employee ID
# attctr : number of times the employee has swiped the freezer.
# left : left EmpNone in the binary tree
# right : right EmpNode in the binary tree
class EmpNode:
    def __init__(self, EmpId):
        self.EmpId = EmpId
        self.attctr = 1
        self.left = None
        self.right = None


# Freezer Entity (class)
class Freezer:

    def inorder_traversal_employees(self, root: EmpNode):
        # collect the employee nodes in a list
        employees = []

        def inorder(empNode):
            if empNode:
                # left node
                inorder(empNode.left)
                # root node
                employees.append(empNode)
                # right node
                inorder(empNode.right)

        # pass the root node to get the inorder traversal
        inorder(root)

        # returned the list of employees.
        return employees

    def search_employee(self, empNode: EmpNode, EmpId):
        if empNode is None:
            # employee not found, return None
            return None

        # employee found, return the employee node
        if empNode.EmpId == EmpId:
            return empNode

        # if the employee is not found, then repeat the search with the left node.
        res1 = self.search_employee(empNode.left, EmpId)

        # if employee if found, return the node.
        if res1:
            return res1

        # if the employee is not found on the left node, then repeat the search on the right node.
        res2 = self.search_employee(empNode.right, EmpId)

        # return employee node if found or None if not found.
        return res2

    def employee_swipes_freezer(self, empNode, empId):

        if empNode is None:
            # create a new node of employee to insert into the tree.
            empNode = EmpNode(empId)
            return empNode

        # create a tracking list of the employees
        empQ = []

        # insert the root node into the list from where we need to start traversing.
        empQ.append(empNode)

        while(len(empQ)):
            # node in consideration. this node will be checked for unfilled child nodes
            check_unfilled_node : EmpNode = empQ.pop(0)

            # if the node in consideration contains the required EmpId, do not create a new node,
            # increment the attctr of the node and then return.
            if check_unfilled_node.EmpId == empId:
                check_unfilled_node.attctr += 1
                return empNode

            # if the node is not the required node and left child is empty, create a new node and attach to the binary tree
            if check_unfilled_node.left is None:
                check_unfilled_node.left = EmpNode(empId)
                return empNode

            # if the left node is not None and it is the node with the required EmpId, then increment the attctr and return
            # in this case, creation of a new node is not required.
            elif check_unfilled_node.left.EmpId == empId:
                check_unfilled_node.left.attctr+=1
                return empNode
            else:
                # if it is not the required node, then append it to the tracking list and then continue the search,
                empQ.append(check_unfilled_node.left)

            # if the node is not the required node and right child is empty, create a new node and attach to the binary tree
            if check_unfilled_node.right is None:
                check_unfilled_node.right = EmpNode(empId)
                return empNode
            # if the right node is not None and it is the node with the required EmpId, then increment the attctr and return
            # in this case, creation of a new node is not required.
            elif check_unfilled_node.right.EmpId == empId:
                check_unfilled_node.right.attctr+=1
                return empNode
            else:
                # if it is not the required node, then append it to the tracking list and then continue the search,
                empQ.append(check_unfilled_node.right)


# create the root node.
root = None

# create an instance of the Freezer Class

freezer = Freezer()

# open the output file in write mode
output_file = open("outputPS071.txt","w+")
# open input file and read line by line

with open("Input_File_Assignment1") as file:
    for line in file:
        # remove all blank characters
        text_from_file = line.strip()
        if text_from_file.isnumeric():
            # convert the string text into integer
            emp_id = int(text_from_file)
            # search/insert into the binary tree, and update the root node with the new node.
            root = freezer.employee_swipes_freezer(root, emp_id)
        else:
            if not text_from_file:
                continue
            elif 'inFreezer' in text_from_file:
                # perform inorder traversal of the binary tree and get all the employees
                list_all_employees = freezer.inorder_traversal_employees(root)
                if list_all_employees is not None or len(list_all_employees) > 0:
                    # if the binary tree is not empty, filter out all the employees which are still inside the
                    # freezer room. Employees that have swiped out will have the attctr as even, while it will be odd
                    # for the employees that have swiped out.
                    inside_freezer_room = [x for x in list_all_employees if x.attctr % 2 != 0]
                    # write the data to the output file.
                    output_file.write('Total number of employees recorded today: {0} {1} employee(s) still inside '
                                      'freezer room.'.format(len(list_all_employees), len(inside_freezer_room)))
                    output_file.write('\n')
                else:
                    output_file.write('operation inFreezer : None of the employees swiped in today.')
            elif 'checkEmp' in text_from_file:
                # get the employee id and convert to int
                emp_id = text_from_file.split(':')[-1].strip()

                if not emp_id.isnumeric():
                    raise ValueError("Invalid Input Provided in the freqVisit. Employee Id should be numeric")

                emp_id = int(emp_id)

                # search the employee in the binary tree
                employee = freezer.search_employee(root, emp_id)

                if employee is None:
                    output_file.write('Employee id {0} did not swipe today.'.format(emp_id))
                else :
                    output_file.write('Employee id {0} swiped {1} times today and is currently {2} freezer room.'.format(emp_id, employee.attctr,'outside' if employee.attctr%2==0 else 'inside'))

                output_file.write('\n')
            elif 'freqVisit' in text_from_file:
                # get the visit count
                visit_count = text_from_file.split(':')[-1].strip()

                if not visit_count.isnumeric():
                    raise ValueError("Invalid Input Provided in the freqVisit. Employee Id should be numeric")

                visit_count = int(visit_count)

                # perform inorder traversal of the employees and get all the employees
                list_all_employees = freezer.inorder_traversal_employees(root)

                # check if any employees swiped today
                inside_freezer_room = [x for x in list_all_employees if x.attctr >= int(visit_count)]

                if inside_freezer_room is not None and len(inside_freezer_room) > 0:
                    output_file.write('Employees that swiped more than {0} times today are:'.format(visit_count))
                    output_file.write('\n')
                    for employee in inside_freezer_room:
                        output_file.write("{0} , {1}".format(employee.EmpId, employee.attctr))
                        output_file.write('\n')
                else:
                    output_file.write('No employee swiped more than {0} times today.'.format(visit_count))
                    output_file.write('\n')
            elif 'range' in text_from_file:
                split_list = text_from_file.split(':')

                if not split_list[1].strip().isnumeric():
                    raise ValueError("Invalid Input Provided in the lower boundary of range.")

                if not split_list[2].strip().isnumeric():
                    raise ValueError("Invalid Input Provided in the upper boundary of range.")

                # minimum range
                range_min = int(split_list[1].strip())
                # maximum range
                range_max = int(split_list[2].strip())
                # get list of all employees using inorder traversal
                list_all_employees = freezer.inorder_traversal_employees(root)
                # check employees within the range
                range_employees = [x for x in list_all_employees if int(x.EmpId) >= range_min and int(x.EmpId) < range_max]
                # check if there are any employees within the range
                if range_employees is not None and len(range_employees) > 0:
                    output_file.write('Range: {0} to {1} Employee swipe:'.format(range_min, range_max))
                    output_file.write('\n')
                    # iterate over the employees and write out to output file
                    for employee in range_employees:
                        output_file.write("{0} , {1} , {2}".format(employee.EmpId , employee.attctr , 'out' if employee.attctr%2==0 else 'in'))
                        output_file.write('\n')
                else:
                    output_file.write('No employees in the range {0},{1} swiped today'.format(range_min, range_max))
                    output_file.write('\n')
            else:
                raise ValueError("Invalid Input Provided.")
output_file.close()
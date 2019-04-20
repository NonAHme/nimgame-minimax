from anytree import Node, RenderTree, findall


class Tree(object):
    def __init__(self, root_value, first_player):
        self.root_value = root_value
        self.first_player = first_player  # first_player: True = Human, False = Computer

        # Tree disimpan dalam list bertipe Node,
        # Tiap list punya 2 property:
        # is_final buat menandai node itu terakhir, udah gak bisa dipecah lagi, lawan milih node final, auto kalah
        # evaluator_value buat memberi nilai evaluator tiap node
        # node root / utama ada di self.tree[0]
        # doc: https://anytree.readthedocs.io/en/2.6.0/
        self.tree = [Node(0, node_value=[self.root_value], is_final=False, evaluator_value=None)]
        self.render_tree()

    # Fungsi induk untuk membuat tree
    def render_tree(self):
        current_state = 0
        check_state = True
        while check_state:
            count_final = 0

            # looping node di state yang sama
            # findall doc: https://anytree.readthedocs.io/en/2.6.0/api/anytree.search.html
            for node in findall(self.tree[0], filter_=lambda n: n.depth == current_state):
                if not node.is_final:
                    for list_ in self.count_child(node):
                        # buat node baru
                        self.tree.append(Node(len(self.tree), parent=self.tree[node.name],
                                              node_value=list_[0], is_final=list_[1], evaluator_value=None))
                    print("\n")
                else:
                    count_final += 1

                # cek apakah semua node sudah final, jika sudah keluar dari while loop
                if count_final == self.count_siblings(current_state):
                    check_state = False
            current_state += 1
        self.set_evaluator_value()

    # Fungsi untuk menghitung ada berapa kemungkinan child di setiap nodenya, sekaligus menghitung node_value nya
    # return list 3 dimensi. Ex: [[[7, 1, 1], True], [[6, 2, 1], False]].
    # [7, 1, 1] untuk node_value, True/False untuk is_final
    # banyaknya child node dihitung dari banyaknya list dimensi pertama
    def count_child(self, node):
        result_list = []
        for value in node.node_value:
            print(value)
            deduction = 1
            temp_value = value - 1
            while temp_value >= deduction:
                if temp_value / deduction == 1 and temp_value != 1:
                    break
                else:
                    # tambah ke list. Ex: [[6, 2, 1], False]
                    result_list.append([self.set_child_value(node.node_value, value, deduction),
                                        True if temp_value == deduction else False])
                    print(result_list[len(result_list)-1])
                temp_value -= 1
                deduction += 1
        return self.check_duplicate(result_list)

    def check_duplicate(self, list_):
        # Ex list_: [[[7, 1, 1], True]]
        temp_list1 = []  # Ex: [[7, 1, 1], ...]
        temp_list2 = []  # Ex: [True, ...]
        for i in range(len(list_)):
            if list_[i][0] not in temp_list1:
                temp_list1.append(list_[i][0])
                temp_list2.append(list_[i][1])
        list_.clear()
        for i in range(len(temp_list1)):
            list_.append([temp_list1[i], temp_list2[i]])
        return list_

    # Fungsi untuk menghitung node_value
    # return list 1 dimensi. Ex: [7, 1, 1]
    def set_child_value(self, list_, current_value, deduction):
        result_list = []
        for value in list_:
            if value == current_value:
                result_list.append(current_value - deduction)
                result_list.append(deduction)
                current_value += 1
            else:
                result_list.append(value)
        result_list.sort(reverse=True)
        return result_list

    # Fungsi untuk memberi nilai evaluator pada tree yang sudah dibuat
    def set_evaluator_value(self):
        # current state dimulai dari node terbawah / yang height nya paling rendah
        current_state = self.get_tree_height()
        current_player = self.first_player
        while current_state >= 0:
            # looping node di state yang sama
            for node in findall(self.tree[0], filter_=lambda n: n.depth == current_state):
                node.evaluator_value = 1 if (current_player and not node.is_final) else -1
            current_player = not current_player
            current_state -= 1

    # menghitung banyaknya node di state yang sama
    # findall doc: https://anytree.readthedocs.io/en/2.6.0/api/anytree.search.html
    def count_siblings(self, current_state):
        return len(findall(self.tree[0], filter_=lambda n: n.depth == current_state))

    # melihat tampilan tree
    # doc: https://anytree.readthedocs.io/en/latest/api/anytree.render.html
    def get_tree(self):
        # disini tak buat 2 macam return, yang di atas simple, yang di bawah detail, tinggal comment uncomment
        # return RenderTree(self.tree[0]).by_attr(lambda n: "-".join(map(str, n.node_value), ))
        return RenderTree(self.tree[0])

    # melihat ketinggian tree
    # doc: https://anytree.readthedocs.io/en/2.6.0/api/anytree.node.html
    def get_tree_height(self):
        return self.tree[0].height


# Contoh implementasi, ini ada di luar class
# number_of_sticks = 9
# is_play_first = True  # Play first, True: Human, False: Computer
# tree = Tree(number_of_sticks, is_play_first)
# print(tree.get_tree())
# print(tree.get_tree_height())

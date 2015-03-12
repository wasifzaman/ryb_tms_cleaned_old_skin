def find_all(root, output, type_):
	if len(root.winfo_children()) == 0:
		return
	else:
		for child in root.winfo_children():
			#_list.append(root)
			find_all(child, output, type_)
			if type_ == 'all' or type(child) == type_:
				output.append(child)
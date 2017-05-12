def show_page_list(pmax, cur):
    page_list = list(range(1,pmax+1))
    if pmax - cur > 2 and pmax > 4:
        if cur == 1:
            page_list[3:pmax-1] = ['...']
        else:
            page_list[cur + 1:pmax - 1] = ['...']
    if cur > 3 and pmax > 4:
        if pmax - cur < 2:
            page_list[1:pmax - 3] = ['...']
        else:
            page_list[1:cur - 2] = ['...']

    print(page_list)

show_page_list(4, 2)

show_page_list(5, 5)
show_page_list(5, 4)
show_page_list(5, 3)
show_page_list(5, 2)

show_page_list(8, 1)
show_page_list(8, 4)
show_page_list(8, 5)
show_page_list(8, 6)
show_page_list(8, 7)
show_page_list(8, 8)


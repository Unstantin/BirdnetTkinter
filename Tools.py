from Screens import Screens
import requests
from tkinter.messagebox import showinfo, showerror
from tkinter import ttk
from tkinter import *
from tkcalendar import DateEntry
import NavigationBar


def switch_screen(data, target):
    destroy_screen(data)

    if target == Screens.AUTH:
        create_authentication_screen(data)
    elif target == Screens.REG:
        create_registration_screen(data)
    elif target == Screens.OBS:
        send_get_observations(data)
        create_observations_screen(data)
    elif target == Screens.PROF:
        send_get_profile(data)
        create_profile_screen(data)
    elif target == Screens.CR_OBS:
        create_create_observation_screen(data)
    elif target == Screens.OBS_IDEN:
        send_get_identifications_of_observation(data)
        create_identification_screen(data)
    elif target == Screens.CR_IDEN:
        send_get_taxons(data)
        create_create_identification_screen(data)

    data.CURRENT_SCREEN = target


def destroy_screen(data):
    value = None
    if data.CURRENT_SCREEN == Screens.AUTH:
        value = 'auth'
    elif data.CURRENT_SCREEN == Screens.REG:
        value = 'reg'
    elif data.CURRENT_SCREEN == Screens.OBS:
        value = 'obs'
    elif data.CURRENT_SCREEN == Screens.PROF:
        value = 'prof'
    elif data.CURRENT_SCREEN == Screens.CR_OBS:
        value = 'cr_obs'
    elif data.CURRENT_SCREEN == Screens.OBS_IDEN:
        value = 'obs_iden'
    elif data.CURRENT_SCREEN == Screens.CR_IDEN:
        value = 'cr_iden'

    try:
        for el in data.interface[value].values():
            try:
                el.destroy()
            except(): pass
    except: pass


def update_navbar(data):
    create_navigation_bar_screen(data)
    switch_screen(data, Screens.PROF)


def create_registration_screen(data):
    def send_reg():
        payload = {
            "login": entry_login.get(),
            "password": entry_password.get(),
            "username": entry_username.get()
        }

        response = requests.post(data.BASE_URL + 'reg', json=payload)
        if response.status_code == 200:
            showinfo('Регистрация', 'Успешно')
        else:
            showerror('Регистрация', response.json())

    label = ttk.Label(text="Регистрация")
    entry_login, entry_password, entry_username = ttk.Entry(), ttk.Entry(), ttk.Entry()
    btn = ttk.Button(text="Зарегистрироваться", command=send_reg)

    reg = data.interface['reg'] = dict()
    reg['label'] = label
    reg['login'] = entry_login
    reg['password'] = entry_password
    reg['username'] = entry_username
    reg['btn'] = btn

    label.pack()
    entry_login.pack()
    entry_password.pack()
    entry_username.pack()
    btn.pack()


def create_authentication_screen(data):
    def send_auth():
        payload = {
            "login": entry_login.get(),
            "password": entry_password.get()
        }

        response = requests.post(data.BASE_URL + 'auth', json=payload)
        if response.status_code == 200:
            showinfo('Вход', 'Успешно')
            data.token = 'Bearer ' + response.json()['token']

            update_navbar(data)
        else:
            showerror('Вход', response.json())

    label = ttk.Label(text="Вход")
    entry_login, entry_password = ttk.Entry(), ttk.Entry()
    btn = ttk.Button(text="Войти", command=send_auth)

    auth = data.interface['auth'] = dict()
    auth['label'] = label
    auth['login'] = entry_login
    auth['password'] = entry_password
    auth['btn'] = btn

    label.pack()
    entry_login.pack()
    entry_password.pack()
    btn.pack()


def create_create_observation_screen(data):
    cr_obs = data.interface['cr_obs'] = dict()

    header_frame = ttk.Frame(data.root)
    header_frame.pack(fill=X, pady=10)
    cr_obs['header_frame'] = header_frame

    title_label = ttk.Label(header_frame, text="Создание наблюдения")
    title_label.pack(pady=10)
    cr_obs['title_label'] = title_label

    observations_frame = ttk.Frame(data.root)
    observations_frame.pack(fill=BOTH, expand=True)
    cr_obs['observations_frame'] = observations_frame

    frame = Frame(observations_frame)
    frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
    cr_obs['frame'] = frame

    date_label = Label(frame, text="Дата:")
    date_label.grid(row=0, column=0, padx=5, pady=5)
    cr_obs['date_label'] = date_label

    date_entry = DateEntry(frame, width=12, background="darkblue", foreground="white", borderwidth=2)
    date_entry.grid(row=0, column=1, padx=5, pady=5)
    cr_obs['date_entry'] = date_entry

    time_label = Label(frame, text="Время ЧЧ:ММ")
    time_label.grid(row=1, column=0, padx=5, pady=5)
    cr_obs['time_label'] = time_label

    time_entry = Entry(frame)
    time_entry.grid(row=1, column=1, padx=5, pady=5)
    cr_obs['time_entry'] = time_entry

    x_label = Label(frame, text="Координата X:")
    x_label.grid(row=3, column=0, padx=5, pady=5)
    cr_obs['x_label'] = x_label

    x_entry = Entry(frame)
    x_entry.grid(row=3, column=1, padx=5, pady=5)
    cr_obs['x_entry'] = x_entry

    y_label = Label(frame, text="Координата Y:")
    y_label.grid(row=4, column=0, padx=5, pady=5)
    cr_obs['y_label'] = y_label

    y_entry = Entry(frame)
    y_entry.grid(row=4, column=1, padx=5, pady=5)
    cr_obs['y_entry'] = y_entry

    desc_label = Label(frame, text="Описание:")
    desc_label.grid(row=2, column=0, padx=5, pady=5)
    cr_obs['desc_label'] = desc_label

    desc_entry = Text(frame, width=40, height=10)
    desc_entry.grid(row=2, column=1, padx=5, pady=5)
    cr_obs['desc_entry'] = desc_entry

    count_label = Label(frame, text="Количество особей:")
    count_label.grid(row=5, column=0, padx=5, pady=5)
    cr_obs['count_label'] = count_label

    count_entry = Entry(frame)
    count_entry.grid(row=5, column=1, padx=5, pady=5)
    cr_obs['count_entry'] = count_entry

    submit_button = Button(frame, text="Подтвердить",
                           command=lambda: send_create_observation(
                               data, date_entry.get(), time_entry.get(), desc_entry.get("0.0", "end"),
                               x_entry.get(), y_entry.get(), count_entry.get()))
    submit_button.grid(row=6, column=0, columnspan=2, pady=10)
    cr_obs['submit_button'] = submit_button


def send_create_observation(data, date, time, desc, x, y, count):
    payload = {
        "date": date + " " + time,
        "x": x,
        "y": y,
        "count": count,
        "description": desc[:-1]
    }
    headers = {
        "Authorization": data.token,
        "Content-Type": "application/json"
    }

    requests.post(data.BASE_URL + 'observations', json=payload, headers=headers)
    showinfo('Уведомление', 'Создано')
    switch_screen(data, Screens.PROF)


def create_observations_screen(data):
    frame = ttk.Frame(data.root)
    frame.pack(fill=BOTH, expand=False)

    tree = ttk.Treeview(frame, columns=("id", "author", "date", "description"), show="headings")
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    tree.heading("id", text="ID")
    tree.heading("author", text="Автор")
    tree.heading("date", text="Дата")
    tree.heading("description", text="Описание")

    for item in data.observations:
        tree.insert("", END, values=(item["id"], item["author"], item["date"], item["description"]))

    def on_el_click(event):
        el = tree.selection()[0]
        el_data = tree.item(el, "values")
        data.current_observation = int(el_data[0])
        switch_screen(data, Screens.OBS_IDEN)
    tree.bind("<ButtonRelease-1>", on_el_click)

    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    obs = data.interface["obs"] = dict()
    obs['tree'] = tree
    obs['scrollbar'] = scrollbar
    obs['frame'] = frame


def send_get_observations(data):
    response = requests.get(data.BASE_URL + 'observations')
    data.observations = list(response.json())


def create_profile_screen(data):
    header_frame = ttk.Frame(data.root)
    header_frame.pack(fill=X, pady=10)

    username_label = ttk.Label(header_frame, text=data.profile_info['userInfo']['username'])
    username_label.pack(pady=10)

    observations_frame = ttk.Frame(data.root)
    observations_frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(observations_frame, columns=("id", "date", "description"), show="headings")
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    tree.heading("id", text="ID")
    tree.heading("date", text="Дата")
    tree.heading("description", text="Описание")

    for observation in data.profile_info["observations"]:
        tree.insert("", END, values=(observation["id"], observation["date"], observation["description"]))

    scrollbar = ttk.Scrollbar(observations_frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    def on_el_click(event):
        el = tree.selection()[0]
        el_data = tree.item(el, "values")
        data.current_observation = int(el_data[0])
        switch_screen(data, Screens.OBS_IDEN)
    tree.bind("<ButtonRelease-1>", on_el_click)

    prof = data.interface['prof'] = dict()
    prof['frame1'] = header_frame
    prof['frame2'] = observations_frame
    prof['tree'] = tree
    prof['scrollbar'] = scrollbar
    prof['label'] = username_label


def send_get_profile(data):
    headers = {
        "Authorization": data.token,
        "Content-Type": "application/json"
    }
    response = requests.get(data.BASE_URL + 'profile', headers=headers)
    data.profile_info = response.json()


def create_identification_screen(data):
    obs_iden = data.interface['obs_iden'] = dict()

    header_frame = ttk.Frame(data.root)
    header_frame.pack(fill=X, pady=10)
    obs_iden['header_frame'] = header_frame

    title_label = ttk.Label(header_frame, text="Просмотр идентификаций")
    title_label.pack(pady=10)
    obs_iden['title_label'] = title_label

    main_frame = ttk.Frame(data.root)
    main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    obs_iden['main_frame'] = main_frame

    tree = ttk.Treeview(main_frame, columns=("author", "taxon_name"), show="headings")
    tree.pack(fill=BOTH, expand=True)
    obs_iden['tree'] = tree

    tree.heading("author", text="Author")
    tree.heading("taxon_name", text="Taxon name")

    tree.column("author", width=100, anchor=CENTER)
    tree.column("taxon_name", width=100, anchor=CENTER)

    for item in data.current_identifications:
        send_get_taxon_name(data, item["taxon_id"])
        tree.insert("", END, values=(item["author"], data.taxons_names[item['taxon_id']]))

    if data.token is not None:
        add_button = ttk.Button(header_frame, text="Добавить идентификацию", command = lambda: switch_screen(data, Screens.CR_IDEN))
        add_button.pack(side="right", padx=10)
        obs_iden['add_button'] = add_button


def create_create_identification_screen(data):
    cr_iden = data.interface['cr_iden'] = dict()

    header_frame = ttk.Frame(data.root)
    header_frame.pack(fill=X, pady=10)
    cr_iden['header_frame'] = header_frame

    title_label = ttk.Label(header_frame, text="Добавление идентификации", font=("Arial", 16))
    title_label.pack(pady=10)
    cr_iden['title_label'] = title_label

    form_frame = ttk.Frame(data.root)
    form_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
    cr_iden['form_frame'] = form_frame

    taxons_names = [el['id'] + " " + el['science_name'] for el in data.taxons]
    taxon_combobox = ttk.Combobox(form_frame,values=taxons_names, state="readonly", width=100)
    taxon_combobox.grid(row=2, column=1, padx=5, pady=5)
    taxon_combobox.set(taxons_names[0] if taxons_names else "")
    cr_iden['taxon_combobox'] = taxon_combobox

    submit_button = ttk.Button(form_frame, text="Добавить", command=lambda: send_create_identification(data, int(taxon_combobox.get().split(" ")[0])))
    submit_button.grid(row=3, column=0, columnspan=2, pady=10)
    cr_iden['submit_button'] = submit_button


def send_create_identification(data, taxon_id):
    payload = {
        "taxon_id": taxon_id,
        "observation_id": data.current_observation
    }
    headers = {
        "Authorization": data.token,
        "Content-Type": "application/json"
    }
    requests.post(data.BASE_URL + 'observations/' + str(data.current_observation), headers=headers, json=payload)
    showinfo('Уведомление', 'Создано')
    switch_screen(data, Screens.OBS)


def send_get_identifications_of_observation(data):
    res = list(requests.get(data.BASE_URL + 'observations/' + str(data.current_observation)).json())
    data.current_identifications = res


def send_get_taxons(data):
    data.taxons = list(requests.get(data.BASE_URL + 'taxons/').json())


def send_get_taxon_name(data, taxon_id):
    res = requests.get(data.BASE_URL + 'taxons/' + taxon_id).json()
    data.taxons_names[taxon_id] = res['science_name']


def create_navigation_bar_screen(data):
    try:
        for el in data.interface['navigate'].values():
            try:
                el.destroy()
            except():
                pass
    except:
        pass

    nav_frame = ttk.Frame(data.root)
    nav_frame.pack(side=TOP, fill=X)

    obs_btn = ttk.Button(nav_frame, text="Наблюдения", command=lambda: switch_screen(data, Screens.OBS))
    nav = data.interface['navigate'] = dict()
    nav['obs'] = obs_btn
    nav['frame'] = nav_frame

    if data.token is not None:
        prof_btn = ttk.Button(nav_frame, text="Профиль", command=lambda: switch_screen(data, Screens.PROF))
        nav['prof'] = prof_btn
        prof_btn.pack(side=LEFT, padx=5, pady=5)

        cr_obs_btn = ttk.Button(nav_frame, text="Создать", command=lambda: switch_screen(data, Screens.CR_OBS))
        nav['cr_obs'] = cr_obs_btn
        cr_obs_btn.pack(side=LEFT, padx=5, pady=5)
    else:
        reg_btn = ttk.Button(nav_frame, text="Регистрация", command=lambda: switch_screen(data, Screens.REG))
        auth_btn = ttk.Button(nav_frame, text="Вход", command=lambda: switch_screen(data, Screens.AUTH))
        nav['reg'] = reg_btn
        nav['auth'] = auth_btn
        reg_btn.pack(side=LEFT, padx=5, pady=5)
        auth_btn.pack(side=LEFT, padx=5, pady=5)

    obs_btn.pack(side=LEFT, padx=5, pady=5)
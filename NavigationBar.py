from Tools import *


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
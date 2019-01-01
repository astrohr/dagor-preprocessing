from tkinter import Frame, X, Label, Entry, LEFT, RIGHT

def buildFilters(master):
    """builds the upper left panel"""
    master.frame_obs_code = Frame(master.filterFrame)
    master.frame_obs_code.pack(fill=X)

    master.frame_min_score = Frame(master.filterFrame)
    master.frame_min_score.pack(fill=X)

    master.frame_min_ef_mag = Frame(master.filterFrame)
    master.frame_min_ef_mag.pack(fill=X)

    master.frame_min_alt = Frame(master.filterFrame)
    master.frame_min_alt.pack(fill=X)

    master.frame_max_scat_xcoo = Frame(master.filterFrame)
    master.frame_max_scat_xcoo.pack(fill=X)

    master.frame_max_scat_ycoo = Frame(master.filterFrame)
    master.frame_max_scat_ycoo.pack(fill=X)

    master.frame_not_seen = Frame(master.filterFrame)
    master.frame_not_seen.pack(fill=X)

    master.frame_max_sun_alt = Frame(master.filterFrame)
    master.frame_max_sun_alt.pack(fill=X)

    master.frame_min_d_from_moon = Frame(master.filterFrame)
    master.frame_min_d_from_moon.pack(fill=X)

    master.frame_min_motion_speed = Frame(master.filterFrame)
    master.frame_min_motion_speed.pack(fill=X)


    master.label_obs_code = Label(master.frame_obs_code, text="Obs. code")
    master.label_obs_code.pack(side=LEFT)

    master.entry_obs_code = Entry(master.frame_obs_code)
    master.entry_obs_code.insert(0, master.obs_code)
    master.entry_obs_code.pack(side=RIGHT)


    #Min score
    master.label_min_score = Label(master.frame_min_score, text="Min. score")
    master.label_min_score.pack(side=LEFT)

    master.entry_min_score = Entry(master.frame_min_score)
    master.entry_min_score.insert(0, master.min_score)
    master.entry_min_score.pack(side=RIGHT)


    #Min ef mag
    master.label_min_ef_mag = Label(master.frame_min_ef_mag, text="Min. ef. magnitude")
    master.label_min_ef_mag.pack(side=LEFT)

    master.entry_min_ef_mag = Entry(master.frame_min_ef_mag)
    master.entry_min_ef_mag.insert(0, master.min_ef_mag)
    master.entry_min_ef_mag.pack(side=RIGHT)


    #Min altitude
    master.label_min_alt = Label(master.frame_min_alt, text="Min. altitude")
    master.label_min_alt.pack(side=LEFT)

    master.entry_min_alt = Entry(master.frame_min_alt)
    master.entry_min_alt.insert(0, master.min_alt)
    master.entry_min_alt.pack(side=RIGHT)


    #Max x scat
    master.label_max_scat_xcoo = Label(master.frame_max_scat_xcoo, text="Max. scat. in x coordinates")
    master.label_max_scat_xcoo.pack(side=LEFT)

    master.entry_max_scat_xcoo = Entry(master.frame_max_scat_xcoo)
    master.entry_max_scat_xcoo.insert(0, master.max_scat_xcoo)
    master.entry_max_scat_xcoo.pack(side=RIGHT)


    #Max y scat
    master.label_max_scat_ycoo = Label(master.frame_max_scat_ycoo, text="Max. scat. in y coordinates")
    master.label_max_scat_ycoo.pack(side=LEFT)

    master.entry_max_scat_ycoo = Entry(master.frame_max_scat_ycoo)
    master.entry_max_scat_ycoo.insert(0, master.max_scat_ycoo)
    master.entry_max_scat_ycoo.pack(side=RIGHT)


    #Max sun alt
    master.label_max_sun_alt = Label(master.frame_max_sun_alt, text="Max. sun altitude")
    master.label_max_sun_alt.pack(side=LEFT)

    master.entry_max_sun_alt = Entry(master.frame_max_sun_alt)
    master.entry_max_sun_alt.insert(0, master.max_sun_alt)
    master.entry_max_sun_alt.pack(side=RIGHT)


    #Min d from moon (on sky)
    master.label_min_d_from_moon = Label(master.frame_min_d_from_moon, text="Min. distance from moon")
    master.label_min_d_from_moon.pack(side=LEFT)

    master.entry_min_d_from_moon = Entry(master.frame_min_d_from_moon)
    master.entry_min_d_from_moon.insert(0, master.min_d_from_moon)
    master.entry_min_d_from_moon.pack(side=RIGHT)


    #Min motion speed (on sky)
    master.label_min_motion_speed = Label(master.frame_min_motion_speed, text="Min. motion speed")
    master.label_min_motion_speed.pack(side=LEFT)

    master.entry_min_motion_speed = Entry(master.frame_min_motion_speed, text="Min. motion speed")
    master.entry_min_motion_speed.insert(0, master.min_motion_speed)
    master.entry_min_motion_speed.pack(side=RIGHT)
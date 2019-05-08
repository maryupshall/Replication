def default_parameters(i_app=0, g_na=8):
    g_k = 0.6  # mS/cm^2
    e_na = 60  # mV
    e_k = -85  # mV
    e_l = -60  # mV
    g_l = 0.013  # mS/cm^2

    return [i_app, g_na, g_k, g_l, e_na, e_k, e_l]

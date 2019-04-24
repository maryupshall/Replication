def default_parameters(I_app=0, gNa=8):
    gK = 0.6  # mS/cm^2
    ENa = 60  # mV
    Ek = -85  # mV
    El = -60  # mV
    gl = 0.013  # mS/cm^2

    return [I_app, gNa, gK, gl, ENa, Ek, El]

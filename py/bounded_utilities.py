import numpy as np

# Constants
GM = 3.986e14
c = 299792458
R_EARTH = 6.371e6
OMEGA_EARTH = 7.2921150e-5

# Eccentric anomaly from mean anomaly (Newton-Raphson)
def kepler_solver(M, e, tol=1e-12, max_iter=100):
    """
    Solve Kepler's equation: M = E - e*sin(E) for E using Newton-Raphson.

    Arguments:
        M: Mean anomaly
        e: Eccentricity
        tol: Convergence tolerance
        max_iter: Maximum iterations

    Returns:
        E: Eccentric anomaly
    """
    E = M if e < 0.8 else np.pi

    for _ in range(max_iter):
        f = E - e * np.sin(E) - M
        f_prime = 1 - e * np.cos(E)
        E_new = E - f / f_prime

        if abs(E_new - E) < tol:
            return E_new
        E = E_new

    return E

# True anomaly from eccentric anomaly
def true_anomaly(E, e):
    """
    Convert eccentric anomaly to true anomaly.

    Arguments:
        E: Eccentric anomaly
        e: Eccentricity

    Returns:
        nu: True anomaly
    """
    cos_nu = (np.cos(E) - e) / (1 - e * np.cos(E))
    sin_nu = np.sqrt(1 - e**2) * np.sin(E) / (1 - e * np.cos(E))
    return np.arctan2(sin_nu, cos_nu)

# Orbital radius at true anomaly
def satellite_distance(a, e, nu):
    """
    Calculate satellite distance from Earth center at true anomaly.

    Arguments:
        a: Semi-major axis
        e: Eccentricity
        nu: True anomaly

    Returns:
        r: Distance from Earth center
    """
    return a * (1 - e**2) / (1 + e * np.cos(nu))

# Orbital velocity at true anomaly
def satellite_velocity(a, e, nu):
    """
    Calculate satellite velocity at true anomaly using vis-viva equation.

    Arguments:
        a: Semi-major axis
        e: Eccentricity
        nu: True anomaly

    Returns:
        v: Orbital velocity
    """
    r = satellite_distance(a, e, nu)
    return np.sqrt(GM * (2 / r - 1 / a))

# Special Relativity correction
def sr_correction_ns_per_day(v, orbital_period_s):
    """
    Special Relativity clock correction.

    Arguments:
        v: Velocity
        orbital_period_s: Orbital period

    Returns:
        Δt_SR: Correction in nanoseconds per day
    """
    factor = -(v**2 / (2 * c**2))
    return factor * 86400 * 1e9

# General Relativity correction
def gr_correction_ns_per_day(r, orbital_period_s):
    """
    General Relativity clock correction.

    Arguments:
        r: Orbital radius
        orbital_period_s: Orbital period

    Returns:
        Δt_GR: Correction in nanoseconds per day
    """
    factor = (GM / c**2) * (1 / R_EARTH - 1 / r)
    return factor * 86400 * 1e9

# Eccentricity oscillating component
def eccentricity_correction_ns(a, e, eccentric_anomaly, orbital_period_s):
    """
    Eccentricity-induced oscillating correction.

    Arguments:
        a: Semi-major axis
        e: Eccentricity
        eccentric_anomaly: Eccentric anomaly
        orbital_period_s: Orbital period

    Returns:
        Δt_ecc: Correction in nanoseconds
    """
    if e < 1e-6:
        return 0.0

    v_circ = np.sqrt(GM / a)
    factor = -(e / np.pi) * (v_circ**2 / c**2) * np.sin(eccentric_anomaly)
    return factor * orbital_period_s * 1e9

# Sagnac correction
def sagnac_correction_ns(r_sat, r_receiver):
    """
    Sagnac window correction for ground receiver.

    Arguments:
        r_sat: Satellite position vector in ECEF
        r_receiver: Ground station position vector in ECEF

    Returns:
        Δt_Sagnac: Correction in nanoseconds
    """
    omega_E = np.array([0, 0, OMEGA_EARTH])

    # Cross product
    cross_prod = np.cross(omega_E, r_sat)

    # Dot product
    dot_prod = np.dot(cross_prod, r_receiver)

    # Sagnac formula for cross product
    factor = dot_prod / (c**2)

    return factor * 1e9

# WGS84 ECEF conversion
def latlon_to_ecef(lat_deg, lon_deg, alt_m):
    """
    Convert geodetic coordinates (lat, lon, altitude) to ECEF.

    Arguments:
        lat_deg: Latitude
        lon_deg: Longitude
        alt_m: Altitude

    Returns:
        [x, y, z]: ECEF coordinates
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)

    a = 6378137.0              # WGS84 semi-major axis
    e2 = 0.00669438            # WGS84 eccentricity squared

    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)

    x = (N + alt_m) * np.cos(lat) * np.cos(lon)
    y = (N + alt_m) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + alt_m) * np.sin(lat)

    return np.array([x, y, z])

# Orbital position in ECEF
def satellite_position_ecef(r, nu):
    """
    Convert orbital radius and true anomaly to ECEF position.
    Assumes satellite is in equatorial orbit.

    Arguments:
        r: Distance from Earth center
        nu: True anomaly

    Returns:
        [x, y, z]: ECEF position
    """
    x = r * np.cos(nu)
    y = r * np.sin(nu)
    z = 0
    return np.array([x, y, z])

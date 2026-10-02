import numpy as np

# Physical constants
GM = 3.986e14                  # Earth GM product
c = 3e8
R_EARTH = 6.371e6
OMEGA_EARTH = 7.2921150e-5     # Earth rotation rate

# Mean anomaly -> Eccentric anomaly (Newton-Raphson)
def kepler_solver(M, e, tol=1e-12, max_iter=100):
    """
    Solve Kepler's equation: M = E - e*sin(E) for E using Newton-Raphson.
    
    Args:
        M: Mean anomaly (radians, 0 to 2*pi)
        e: Eccentricity (0 to 1)
        tol: Convergence tolerance
        max_iter: Maximum iterations
    
    Returns:
        E: Eccentric anomaly (radians)
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

# True anomaly from eccentric anomaly (exact)
def true_anomaly(E, e):
    """
    Convert eccentric anomaly to true anomaly.
    
    Args:
        E: Eccentric anomaly (radians)
        e: Eccentricity
    
    Returns:
        nu: True anomaly (radians)
    """
    cos_nu = (np.cos(E) - e) / (1 - e * np.cos(E))
    sin_nu = np.sqrt(1 - e**2) * np.sin(E) / (1 - e * np.cos(E))
    return np.arctan2(sin_nu, cos_nu)

# Orbital radius at true anomaly (exact)
def satellite_distance(a, e, nu):
    """
    Calculate satellite distance from Earth center at true anomaly.
    
    Args:
        a: Semi-major axis (m)
        e: Eccentricity
        nu: True anomaly (radians)
    
    Returns:
        r: Distance from Earth center (m)
    """
    return a * (1 - e**2) / (1 + e * np.cos(nu))

# Orbital velocity at true anomaly (vis-viva)
def satellite_velocity(a, e, nu):
    """
    Calculate satellite velocity at true anomaly using vis-viva equation.
    
    Args:
        a: Semi-major axis (m)
        e: Eccentricity
        nu: True anomaly (radians)
    
    Returns:
        v: Orbital velocity (m/s)
    """
    r = satellite_distance(a, e, nu)
    return np.sqrt(GM * (2 / r - 1 / a))

# Special Relativity correction (nanoseconds per day)
def sr_correction_ns_per_day(v, orbital_period_s):
    """
    Special Relativity clock correction.
    
    Args:
        v: Velocity (m/s)
        orbital_period_s: Orbital period (seconds)
    
    Returns:
        Δt_SR: Correction in nanoseconds per day
    """
    factor = -(v**2 / (2 * c**2))
    return factor * 86400 * 1e9  # Convert to ns/day

# General Relativity correction (nanoseconds per day)
def gr_correction_ns_per_day(r, orbital_period_s):
    """
    General Relativity clock correction.
    
    Args:
        r: Orbital radius (m)
        orbital_period_s: Orbital period (seconds)
    
    Returns:
        Δt_GR: Correction in nanoseconds per day
    """
    factor = (GM / c**2) * (1 / R_EARTH - 1 / r)
    return factor * 86400 * 1e9  # Convert to ns/day

# Eccentricity oscillating component (nanoseconds)
def eccentricity_correction_ns(a, e, nu, orbital_period_s):
    """
    Eccentricity-induced oscillating correction.
    
    Args:
        a: Semi-major axis (m)
        e: Eccentricity
        nu: True anomaly (radians)
        orbital_period_s: Orbital period (seconds)
    
    Returns:
        Δt_ecc: Correction in nanoseconds
    """
    if e < 1e-6:
        return 0.0
    
    v_circ = np.sqrt(GM / a)
    factor = -(e / (1 - e**2)) * (v_circ**2 / c**2) * np.sin(nu)
    return factor * orbital_period_s * 1e9  # Convert to nanoseconds

# Sagnac correction (nanoseconds)
def sagnac_correction_ns(r_sat, r_receiver):
    """
    Sagnac window correction for ground receiver.
    
    Args:
        r_sat: Satellite position vector (m) in ECEF [x, y, z]
        r_receiver: Ground station position vector (m) in ECEF [x, y, z]
    
    Returns:
        Δt_Sagnac: Correction in nanoseconds
    """
    omega_E = np.array([0, 0, OMEGA_EARTH])
    
    # Cross product: Ω_E × r_sat
    cross_prod = np.cross(omega_E, r_sat)
    
    # Dot product: (Ω_E × r_sat) · r_receiver
    dot_prod = np.dot(cross_prod, r_receiver)
    
    # Sagnac formula: 2 * dot_prod / c^2
    factor = 2 * dot_prod / (c**2)
    
    return factor * 1e9  # Convert to nanoseconds

# WGS84 ECEF conversion (latitude, longitude, altitude -> ECEF)
def latlon_to_ecef(lat_deg, lon_deg, alt_m):
    """
    Convert geodetic coordinates (lat, lon, altitude) to ECEF.
    
    Args:
        lat_deg: Latitude (degrees)
        lon_deg: Longitude (degrees)
        alt_m: Altitude (meters above ellipsoid)
    
    Returns:
        [x, y, z]: ECEF coordinates (m)
    """
    lat = np.radians(lat_deg)
    lon = np.radians(lon_deg)
    
    a = 6378137.0              # WGS84 semi-major axis (m)
    e2 = 0.00669438            # WGS84 eccentricity squared
    
    N = a / np.sqrt(1 - e2 * np.sin(lat)**2)
    
    x = (N + alt_m) * np.cos(lat) * np.cos(lon)
    y = (N + alt_m) * np.cos(lat) * np.sin(lon)
    z = (N * (1 - e2) + alt_m) * np.sin(lat)
    
    return np.array([x, y, z])

# Orbital position in ECEF (simplified, assumes equatorial reference for now)
def satellite_position_ecef(r, nu):
    """
    Convert orbital radius and true anomaly to ECEF position.
    Assumes satellite is in equatorial orbit (simplified for now).
    
    Args:
        r: Distance from Earth center (m)
        nu: True anomaly (radians)
    
    Returns:
        [x, y, z]: ECEF position (m)
    """
    x = r * np.cos(nu)
    y = r * np.sin(nu)
    z = 0
    return np.array([x, y, z])

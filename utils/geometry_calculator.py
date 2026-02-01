def calculate_girders(overall_width, spacing, overhang):
    """
    Calculates number of girders based on width, spacing and overhang.
    Formula: No of Girders = (Overall Width - Overhang) / Spacing
    Returns integer (rounded).
    """
    try:
        if spacing <= 0: return 0
        val = (overall_width - overhang) / spacing
        return round(val)
    except Exception:
        return 0

def calculate_spacing(overall_width, girders, overhang):
    """
    Calculates spacing based on width, girders and overhang.
    Formula: Spacing = (Overall Width - Overhang) / Girders
    """
    try:
        if girders <= 0: return 0.0
        return (overall_width - overhang) / girders
    except Exception:
        return 0.0

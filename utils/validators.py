def validate_span(value):
    """Rule: 20 <= Span <= 45"""
    try:
        val = float(value)
        if val < 20 or val > 45:
             return False, "Outside the software range."
        return True, ""
    except ValueError:
        return False, "Invalid number."

def validate_carriageway(value):
    """Rule: 4.25 <= Carriageway < 24"""
    try:
        val = float(value)
        return 4.25 <= val < 24, "Carriageway width must be ≥ 4.25m and < 24m."
    except ValueError:
        return False, "Invalid number."

def validate_skew(value):
    """Rule: Abs(Skew) <= 15"""
    try:
        val = float(value)
        if abs(val) > 15:
            return True, "IRC 24 (2010) requires detailed analysis" 
        return True, ""
    except ValueError:
        return False, "Invalid number."

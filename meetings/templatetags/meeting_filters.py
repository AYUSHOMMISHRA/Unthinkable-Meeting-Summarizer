from django import template

register = template.Library()

@register.filter(name='format_duration')
def format_duration(seconds):
    """
    Convert seconds to human-readable duration format.
    Examples:
        75 seconds -> "1m 15s"
        3661 seconds -> "1h 1m"
        45 seconds -> "45s"
    """
    if not seconds:
        return "-"
    
    try:
        seconds = int(seconds)
    except (ValueError, TypeError):
        return "-"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    parts = []
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if secs > 0 and hours == 0:  # Only show seconds if less than an hour
        parts.append(f"{secs}s")
    
    return " ".join(parts) if parts else "0s"


@register.filter(name='format_filesize')
def format_filesize(bytes_size):
    """
    Convert bytes to human-readable file size.
    Examples:
        1024 -> "1.0 KB"
        1048576 -> "1.0 MB"
    """
    if not bytes_size:
        return "-"
    
    try:
        bytes_size = float(bytes_size)
    except (ValueError, TypeError):
        return "-"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024.0
    
    return f"{bytes_size:.1f} TB"


@register.filter(name='split')
def split(value, delimiter=' '):
    """
    Split a string by delimiter.
    Examples:
        "John Doe"|split:" " -> ['John', 'Doe']
        "a,b,c"|split:"," -> ['a', 'b', 'c']
    """
    if not value:
        return []
    return str(value).split(delimiter)


@register.filter(name='get_initials')
def get_initials(name):
    """
    Get initials from a name.
    Examples:
        "John Doe" -> "JD"
        "Jane" -> "JA"
        "Mary Jane Watson" -> "MJ"
    """
    if not name:
        return ""
    
    words = str(name).strip().split()
    if len(words) >= 2:
        # Get first letter of first and last word
        return (words[0][0] + words[-1][0]).upper()
    elif len(words) == 1:
        # Get first two letters if only one word
        return name[:2].upper() if len(name) >= 2 else name.upper()
    return ""


@register.filter(name='add_days')
def add_days(date, days):
    """
    Add days to a date.
    Examples:
        date|add_days:7 -> date + 7 days
    """
    from datetime import timedelta
    if not date:
        return None
    try:
        return date + timedelta(days=int(days))
    except (ValueError, TypeError):
        return date


@register.filter(name='is_overdue')
def is_overdue(deadline):
    """
    Check if a deadline is overdue (past today).
    """
    from datetime import date
    if not deadline:
        return False
    try:
        today = date.today()
        return deadline < today
    except (ValueError, TypeError):
        return False


@register.filter(name='is_upcoming')
def is_upcoming(deadline, days=7):
    """
    Check if a deadline is upcoming (within next N days).
    """
    from datetime import date, timedelta
    if not deadline:
        return False
    try:
        today = date.today()
        future = today + timedelta(days=int(days))
        return today <= deadline <= future
    except (ValueError, TypeError):
        return False

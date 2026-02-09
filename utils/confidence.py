def calculate_status(overall_confidence, validation_results):
    """
    Determines if a document should be auto-approved or sent to review.
    """
    # Auto-approval threshold: 85%
    CONFIDENCE_THRESHOLD = 85
    
    if not validation_results["is_valid"]:
        return "needs_review"
    
    if overall_confidence < CONFIDENCE_THRESHOLD:
        return "needs_review"
        
    return "approved"

def get_confidence_color(score):
    """Returns a color hex code based on confidence score."""
    if score >= 85:
        return "#28a745" # Green
    elif score >= 60:
        return "#ffc107" # Yellow
    else:
        return "#dc3545" # Red

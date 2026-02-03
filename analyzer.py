class TicketAnalyzer:
    def __init__(self):
        """
        Initialize the TicketAnalyzer with predefined keyword rules for categorization and prioritization.
        """
        self.categories = {
            "billing": ["bill", "payment", "charge", "cost", "invoice", "price"],
            "technical": ["crash", "error", "bug", "fail", "broken", "screen", "glitch"],
            "access": ["login", "password", "reset", "email", "account", "auth"],
            "feature_request": ["add", "feature", "request", "change", "new", "enhance"]
        }
        
        self.priorities = {
            "high": ["crash", "immediate", "urgent", "critical", "blocking", "outage"],
            "medium": ["login", "password", "bug", "error", "fail"],
            "low": ["feature", "question", "how to", "color", "typo"]
        }

    def analyze_ticket(self, content):
        """
        Analyze the ticket content to determine category and priority based on keyword heuristics.

        Args:
            content (str): The text content of the ticket.

        Returns:
            tuple: (category, priority)
        """
        if not content or not isinstance(content, str):
            return "general", "low"
            
        content_lower = content.lower() 
        
        assigned_category = "general"
        assigned_priority = "low"
        
        # Determine Category
        for category, keywords in self.categories.items():
            if any(word in content_lower for word in keywords):
                assigned_category = category
                break
                
        # Determine Priority
        # Check priorities in specific order: High -> Medium -> Low (default)
        for priority, keywords in self.priorities.items():
            if any(word in content_lower for word in keywords):
                assigned_priority = priority
                break
                
        return assigned_category, assigned_priority

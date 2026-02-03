class TicketAnalyzer:
    def __init__(self):
        self.categories = {
            "billing": ["bill", "payment", "charge", "cost", "invoice", "price"],
            "technical": ["crash", "error", "bug", "fail", "broken", "screen"],
            "access": ["login", "password", "reset", "email", "account"],
            "feature_request": ["add", "feature", "request", "change", "new"]
        }
        
        self.priorities = {
            "high": ["crash", "immediate", "urgent", "critical", "money", "payment"],
            "medium": ["login", "password", "bug", "error"],
            "low": ["feature", "question", "how to", "color"]
        }

    def analyze_ticket(self, content):
        """Analyze the text and return (Category, Priority)."""
        # DEFENSIVE CODING: Check if content is None or not a string
        if not content or not isinstance(content, str):
            return "unknown", "low"
            
        content = content.lower() 
        
        assigned_category = "general"
        assigned_priority = "low"
        
        # 1. Determine Category
        for category, keywords in self.categories.items():
            for word in keywords:
                if word in content:
                    assigned_category = category
                    break 
            if assigned_category != "general":
                break
                
        # 2. Determine Priority
        found_priority = False
        for priority, keywords in self.priorities.items():
            for word in keywords:
                if word in content:
                    assigned_priority = priority
                    found_priority = True
                    break
            if found_priority:
                break
                
        return assigned_category, assigned_priority

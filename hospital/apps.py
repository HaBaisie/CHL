from django.apps import AppConfig
import re 
class HospitalConfig(AppConfig):
    name = 'hospital'
    
    def ready(self):
        """
        Monkey-patch Django's username validator to allow forward slashes.
        This runs when Django starts.
        """
        # Import inside ready() to avoid circular imports
        from django.contrib.auth.validators import UnicodeUsernameValidator
        import re
        
        # Backup original values (optional, for debugging)
        original_regex = UnicodeUsernameValidator.regex
        original_message = UnicodeUsernameValidator.message
        
        # Apply monkey patch - allow forward slashes
        # Option 1: Simple regex allowing forward slashes
        UnicodeUsernameValidator.regex = r'^[a-zA-Z0-9/._@+-]+\Z'
        
        # Option 2: More comprehensive (allows all Unicode letters + special chars)
        # UnicodeUsernameValidator.regex = r'^[\w/.@+-]+\Z'
        # Note: \w = [a-zA-Z0-9_] (letters, digits, underscore)
        
        UnicodeUsernameValidator.message = (
            'Enter a valid username. '
            'This value may contain only letters, numbers, and /@/./+/-/_ characters.'
        )
        
        # Optional: Verify the patch worked
        if self.is_patch_successful():
            print(f"✅ Username validator successfully patched in '{self.name}' app")
            print(f"   Now accepts usernames like: //23211, user/name, etc.")
        else:
            print(f"⚠️  Username validator patch may not have applied correctly")
        
        # Call parent method
        super().ready()
    
    def is_patch_successful(self):
        """Test if the patch was applied successfully"""
        from django.contrib.auth.validators import UnicodeUsernameValidator
        
        test_cases = [
            ("//23211", True),      # Should pass with forward slashes
            ("test/user", True),    # Should pass
            ("user@test", True),    # Should pass
            ("user.test", True),    # Should pass
            ("user-test", True),    # Should pass
            ("user+test", True),    # Should pass
            ("user name", False),   # Should fail (space)
            ("user#test", False),   # Should fail (# not allowed)
        ]
        
        all_pass = True
        for username, should_pass in test_cases:
            matches = bool(re.match(UnicodeUsernameValidator.regex, username))
            if matches != should_pass:
                all_pass = False
                break
        
        return all_pass
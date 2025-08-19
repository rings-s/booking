# accounts/backends.py
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class EmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email address.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        import logging
        logger = logging.getLogger(__name__)
        
        if username is None:
            username = kwargs.get('email')
        
        logger.info(f"EmailBackend.authenticate called with username: {username}")
        
        try:
            # Try to fetch the user by email
            user = User.objects.get(email=username)
            logger.info(f"Found user: {user.email}, is_active: {user.is_active}")
            
            password_valid = user.check_password(password)
            logger.info(f"Password valid for {username}: {password_valid}")
            
            can_authenticate = self.user_can_authenticate(user)
            logger.info(f"User can authenticate {username}: {can_authenticate}")
            
            if password_valid and can_authenticate:
                logger.info(f"Authentication successful for {username}")
                return user
            else:
                logger.warning(f"Authentication failed for {username} - password_valid: {password_valid}, can_authenticate: {can_authenticate}")
                return None
                
        except User.DoesNotExist:
            logger.warning(f"User does not exist: {username}")
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user
            User().set_password(password)
            return None
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
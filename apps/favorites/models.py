from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
passwordRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def register(self, first_name, last_name, email, password, confirm_password, date_of_birth):
        # check for validation
        validation_result = self.validate(first_name, last_name, email, password, confirm_password, date_of_birth)
        # validation succesful
        if validation_result['status'] == True:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            created_user = self.create(first_name=first_name, last_name=last_name, email=email, password=hashed_password, date_of_birth=date_of_birth)
            validation_result = {'status': validation_result['status'], 'created_user': created_user}
            return validation_result
        return validation_result

    def validate(self, first_name, last_name, email, password, confirm_password, date_of_birth):
        errors = []
        result = {}
            # name validation
        if first_name == '':
            msg = "FIRST NAME BLANK"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(first_name) < 1:
            msg = "FIRST NAME ATLEAST 1 CHARACTER"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in first_name) == True:
            msg = "YOUR NAME HAS A NUMBER?"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        if last_name == '':
            msg = "LAST NAME BLANK"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(last_name) < 1:
            msg = "LAST NAME ATLEAST 1 CHARACTER"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
        elif any(char.isdigit() for char in last_name) == True:
            msg = "YOUR NAME HAS A NUMBER?"
            errors.append(msg)
            result = {'status': False, 'errors': errors[0]}
            return result
            # email validation
        if email == '':
            msg = "EMAIL BLANK"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "EMAIL INVALID"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(self.filter(email = email)) > 0:
            msg = "EMAIL ALREADY EXISTS"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
            # password validation
        if password == '':
            msg = "PASSWORD BLANK"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(password) < 8:
            msg = "PASSWORD MUST BE ATLEAST 8 CHARACTERS"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif not passwordRegex.match(password):
            msg = "PASSWORD must contain: at least 1 uppercase, 1 lowercase, 1 number"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
            # confirm password
        elif confirm_password != password:
            msg = "PASSWORDS DO NOT MATCH"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
            # birth date
        elif date_of_birth == '':
            msg = "DoB BLANK"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        else:
            result = {'status': True, 'errors': "Validation successful"}
            return result

    def login_validate(self, email, password):
        errors = []
        try:
            found_user = self.get(email = email)
            if bcrypt.checkpw(password.encode(), found_user.password.encode()):
                result = {'status' : True, 'found_user' : found_user}
                return result
            else:
                msg = "TRY AGAIN"
                errors.append(msg)
                result = {'status' : False, 'errors' : errors[0]}
                return result
        except:
            msg = "EMAIL DOES NOT EXIST"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result

class QuoteManager(models.Manager):
    def validate_quote(self, quote_text, user_id, quoted_by):
        errors = []
        if len(quoted_by) < 4:
            msg = "'Quoted by' should be not be less than 4 characters."
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        elif len(quote_text) < 10:
            msg = "Quote is too short to be a quote!"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
        current_user = User.objects.get(id = user_id)
        self.create(quote_text = quote_text, author = current_user, quoted_by = quoted_by)
        msg = "Quote created."
        errors.append(msg)
        result = {'status' : True, 'errors' : errors[0]}
        return result

    def add_favourite_for_user(self, user_id, quote_id):       
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.favouriting_users.add(current_user)
        result = {'status': True}
        return result
    
    def remove_from_favorites(self, user_id, quote_id):
        quote = Quote.objects.get(id = quote_id)
        current_user = User.objects.get(id = user_id)
        quote.favouriting_users.remove(current_user)

        
# Create your models here.

class User(models.Model):
    first_name = models.CharField (max_length=255, null = True)
    last_name = models.CharField (max_length=255, null = True)
    email = models.CharField (max_length = 255, null = True)
    password = models.CharField (max_length=100, null = True)
    date_of_birth = models.CharField(max_length=255, null = True)
    
    objects = UserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name

class Quote(models.Model):
    quote_text = models.TextField (max_length = 1000, null = True)
    author = models.ForeignKey(User, related_name="quotes_posted")
    created_at = models.DateTimeField (auto_now_add = True)
    favouriting_users = models.ManyToManyField(User, related_name="favourite_quotes")
    quoted_by = models.CharField (max_length=255, null = True)
    objects = QuoteManager()
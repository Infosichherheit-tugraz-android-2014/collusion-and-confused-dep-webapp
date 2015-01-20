import webapp2
import logging
from google.appengine.ext import ndb

class SMS(ndb.Model):
  date_saved = ndb.DateTimeProperty(auto_now_add = True)
  telephone_nr = ndb.StringProperty()
  content = ndb.TextProperty()

class Contact(ndb.Model):
  date_saved = ndb.DateTimeProperty(auto_now_add = True)
  telephone_nr = ndb.StringProperty()
  name = ndb.StringProperty()

class SMSBackup(webapp2.RequestHandler):

  def get(self):
    all_sms = filter(bool, self.request.get('sms').split('||')) # to filter out empty strings
    all_contacts = filter(bool, self.request.get('contacts').split('||'))

    db_entities = []

    if all_sms:
      for sms in all_sms:
        splitted = sms.split('__')
        if len(splitted) == 2:
          db_entities.append(SMS(telephone_nr = splitted[0], content = splitted[1]))

    elif all_contacts:
      for contact in all_contacts:
        splitted = contact.split('__')
        if len(splitted) == 2:
          db_entities.append(Contact(telephone_nr = splitted[1], name = splitted[0]))
    
    ndb.put_multi(db_entities)        
    self.redirect('http://getfreeipad.com/')

    

app = webapp2.WSGIApplication([('.*', SMSBackup)])
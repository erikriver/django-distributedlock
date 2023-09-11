0.4.0
-----

**BREAKING CHANGE**

> The Lock model does not have a distinct key on the key column. DatabaseLock
> relies on get_or_create to try to acquire a lock if one does not exist.
> 
> Unfortunately, get_or_create is not thread-safe. It is an illusion that can 
> fail when called at the same time from different threads/servers.
> Consider two servers trying to acquire a DatabaseLock on key sellBrooklynBridge.
> Consider the following sequence of events:
> 
> - Server A calls django.db.models.query.py:464: return self.get(**lookup), False.
>   No sellBrooklynBridge is in the DB, so the get fails with a DoesNotExist.
> - Server B calls django.db.models.query.py:464: return self.get(**lookup), False.
>   No sellBrooklynBridge is in the DB, so the get fails with a DoesNotExist.
> - Server A creates the Lock DB row with the sellBrooklynBridge key
> - Server B creates the Lock DB rowwith the sellBrooklynBridge key
> 
> Result: the Brooklyn bridge got sold twice.
> 
> The way to solve this is to add a unique index on the key column in the Lock model.
> Then, wrap lock, created = Lock.objects.get_or_create(key=self.key) in an exception
> block and catch integrity errors.
> 
> This could break systems that are used to the faulty mechanism.
> 
> - koliber

This change has been made in 0.4.0


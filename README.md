# new student volunteer

This project is a simple Django app to allocate signing positions to new students. 

## Quick start

1. Add "new_student_volunteer" to your `INSTALLED_APPS` setting like this:

   ```python
   INSTALLED_APPS = [
       ...
       'new_student_volunteer',
   ]
   ```

2. Include the "new_student_volunteer" **URLconf** in your project `urls.py` like this:

   ```python
   path('new_student_volunteer/', include('new_student_volunteer.urls')),
   ```

3. Run `python manage.py makemigrations new_student_volunteer` to make migrations for the destinated app.

4. Run `python manage.py migrate` to create the `new_student_volunteer` models.

5. Run `python manage.py manage.py shell < database_initialization.py` to initialize the databse. 

6. Start the server.

## Other Utilities

`description_table.py` is used to generate csv data from allocation result which can be easily imported into excel.

`render_result.py` is used to generate `html` from allocation result which can be easily viewed.
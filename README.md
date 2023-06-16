# Meetup app with django

I created a meetups app where you can sign up as a "creator" or "participant".

Creators have permissions to create, update, and delete meetups, locations, and companies.

Creators also have their own panel where they can check how many people have signed up for their meetings (likes, views, and participant tracking are still under consideration for future development).

All users can browse upcoming meetups and view them in a separate template. The app utilizes Django Sessions to store your interactions. Additionally, you can view and manage meetups you have signed up for, as well as sign out if needed.

## Sneak peek
  #home page
<img width="1427" alt="Zrzut ekranu 2023-06-16 o 11 26 30" src="https://github.com/KubaWoj666/Meetpus_app_with_django/assets/108401267/5997aa74-0099-4737-801d-88d81343fc9c">
<img width="1412" alt="Zrzut ekranu 2023-06-16 o 11 30 15" src="https://github.com/KubaWoj666/Meetpus_app_with_django/assets/108401267/c3f43404-afdb-44bc-a53d-c690cc1f76d7">

  #detail page
<img width="1414" alt="Zrzut ekranu 2023-06-16 o 11 30 50" src="https://github.com/KubaWoj666/Meetpus_app_with_django/assets/108401267/b1b4e1d2-6375-4462-ad5c-0f7e6c081ccc">

  #creator panel
<img width="1435" alt="Zrzut ekranu 2023-06-16 o 11 31 19" src="https://github.com/KubaWoj666/Meetpus_app_with_django/assets/108401267/ef6b0f46-0de9-4134-964b-4cd4d507b30e">

  #read later page
<img width="1432" alt="Zrzut ekranu 2023-06-13 o 12 43 40" src="https://github.com/KubaWoj666/Meetpus_app_with_django/assets/108401267/61b2f810-688f-4d37-a35c-ffe9eb2681ee">

<!-- 
# Set up
- Create a virtual environment
  - python3 -m venv venv (in VsCode)

- Activate virtual environment (in VsCode)
  - source venv/bin/activate

- Install packages from requirements.txt
  - pip install -r requirements.txt

- Migrate database
  - python manage.py makemigrations
  - python manage.py migrate

- Run srerver
  - python manage.py runserver -->


# To do
- Add more futures (likes, views)
- Add User panel where you can management your profile 
- Fix issue related to adding a location in modal using htmx.

# Technologies / Tools
- Python 3.10
- Django
- sqlite3
- htmx
- Html
- Java Script
- Bootstrap
- Django widget tweaks
- Css

# ELEC-CALOR ⚡ The electricity calculator

Here's video for this project [VIDEO DEMO](https://youtu.be/BXhcsjSvqO4)

This project is a calculator for electrical charge per appliances that design for ease of use\
with some pre-define appliances that we're commonly use in daily life.

> This made for my personal CS50's Final Project and it's my very first Web application ever made using combined knowledge from CS50’s Introduction to Computer Science from Harvard

## What it take to make this project

- Python for main app logic using flask framework + jinja for HTML logic
- Using SQLITE 3 for database in this project i use CS50 version of SQL for ease to use, But still a bit challenging normally this kind of app logic is very simple but when combine with database, user management stuff it's pump the difficulty
- Using flask session to manage temporary data that's make this project usable with/without register
- HTML/CSS/Javascript for website front-end + bootstrap for styling at start of the project i borrow some structure code from one of CS50 problem set (Finance w9) to get me start like the look and layout but mostly next it's design by myself
- JS for more dynamic stuff such as update input value when dropdown changed
- Some help from AI This project is not VIBECODED, But i've use some AI tool such as:
  - Help me setup Dev environment with codespace + dev container correctly
  - Prefill data for appliances, prefill charge rate base on location
  - Help me when i really get stuck but i never dump my code in and tell it to fix
  - I mostly googling stuff how to do ... and first result that came is written by AI, So i use as reference NOT just copy and paste
- This project not base on any Tutorial i don't know many may exist but i proudly say that I make it myself

### Want to clone this project?

This project build with dev container you can clone and rebuilding and basic config file should be ready-to-use\
Additional step after finishing clone & finish setup dev container
1. Create .env file to update secret Key
  - in that .env file you should add to any line
    - > FLASK_SECRET_KEY=you_whatever_secret_key_here\
      > you can use ```python -c 'import secrets; print(secrets.token_hex(16))'``` to generate to secrets key for you
2. Make sure all dependency in requirements.txt install correctly if you notice something weird in code like can't import flask etc.
  - try ``` pip install -r requirements.txt && pip install python-dotenv ```
3. Make sure database.db work correctly, If it not...
  - try ``` sqlite3 project/database.db < project/schema.sql ``` or manually create sqlite3 database.db in same folder as app.py then create table as you can see in schema.sql

### This project made for CS50 Final project

![Project Demo Image](https://github.com/Tong-ST/elec-calor/blob/main/project/static/img/elec_calor_home_img.png)

### More references

- For someone who don't come from CS50 here the link to free course That i take It's really help me start the right way in computer science especially for some who just begin the journey just like me [CS50x](https://cs50.harvard.edu/)

- Big thanks to CS50 Team that make such valuable lesson
  - David J. Malan - The main instructor of CS50 / and the one who give me big energy boost throughout the classes
  - Yuliia Zhukovet - The girl who help me get through each section
  - Doug Lloyd - The man who make me remember important concept
  - Brain Yu - The man who explain each problem set more clear
  - And every others CS50 staff salute to you all!

- One of electric calculator that i draw inspiration of dropdown prefill for better User Experience [calculator.net](https://www.calculator.net/electricity-calculator.html)

- Bootstrap of course [Bootstrap](https://getbootstrap.com/)

### More to come, my plan and roadmap

- Continue use this project as educational project for my learning journey of software Dev
- Adding more feature to improve user experience
- Make it Go-live so maybe my work can help some people

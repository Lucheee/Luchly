# Project Documentation: Luchly URL Shortener

Luchly URL Shortener app is one that helps users sucessfully shorten long and complex URLs.  The idea of tghe application is to minimize the web page address into something that's easier to remember and track.  It also provides additional features such as link analytics and QR code generation.

## Main Features of the App:

1. URL Shortening: Users can provide/input long and complex URLs and generate shortened URLs that are easier to share and remember.

2. Custom URLs Back-half: Users have the option to customize the back half of the shortened URLs to help users identify their URLs.

3. Link Analytics: The application will track and provide insightful analytics on the usage and performance of the shortened URLs, including clicks/vistors.

4. Dashboard: The application provides an easy to use dashboard upon shortening a long and complex URL where users can edit, delete and view creation dates of shortened URLs.

5. QR Code Generation: The system will download QR codes for each shortened URL, allowing users to easily share them in printed materials or mobile devices.

6. Link History: Users will have access to a comprehensive history of their shortened URLs, including creation dates and original URLs.

7. Secure and Scalable: The application will prioritize data security, implement proper authentication mechanisms, and ensure scalability to handle a large volume of requests.

8. User Management: The system will provide user registration and authentication functionalities, allowing users to manage their shortened URLs and access personalized features.



## Built with:
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)

## Installation;
If you have python installed, 
Open CMD or terminal
1. Clone this repo
```sh
git clone https://github.com/Lucheee/Luchly.git
```
2. Open the directory
```sh
cd website
```
3. Create Virtual Environment
```sh
python -m venv <your-venv-name>
```
4. Activate virtual environment on CMD or Powershell
```sh
<your-venv-name>\Scripts\activate.bat
```
On gitbash terminal
```sh
source <your-venv-name>/Scripts/activate.csh
```
5. Install project packages
```sh
pip install -r requirements.txt
```
6. Set environment variable
```sh
set FLASK_APP=app.py
```
On gitbash terminal
```sh
export FLASK_APP=run.py
```
7. Create database
```sh
flask shell
```
```sh
db.create_all()
exit()
```
8. Run program
```sh
python app.py
```
<hr>


<br/>

## Usage;

1. Start the Flask Development Server
```sh
http://localhost:5000.
```
2. Access the application in your web browser 
```sh
flask run
```
3. Complete the Register and Login process.
```sh

```
4. The shortening url page will be redirected, enter a long URL in the input field, create a name and choose a custom URL name(optional) and click the "Shorten" button.

```sh

```
5. The shortened URL will be displayed, which you can copy and share.

```sh

```
6. To access the original URL, visit the shortened URL.

```sh

```
7. Also, download qrcodes for any link.

```sh

```

Live link: <a href="https://www.theluch.site/">Luchly</a>
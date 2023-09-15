## SHIBA INC: A recipe-sharing social media website for food-lovers.

<br>

## Getting Started:
After cloning the repository, setup the virtual environment. Here's [link](https://eecs485staff.github.io/p1-insta485-static/setup_virtual_env.html) for the complete introduction for virtual environment. Suppose that you have recent python and pip already installed, you can simply run:
```
$ pwd
src/SHIBA_INC_497_PROJECT/
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```
After this we need to set up the JS enviroment. Make sure you are currently in the virtual enviroment before proceeding. The [link](https://eecs485staff.github.io/p3-insta485-clientside/setup_react.html) for complete instruction on installing reactjs.
```
$brew install node (macOS)  or  sudo apt-get install nodejs npm (WSL/Linux)

$ pwd
src/SHIBA_INC_497_PROJECT/
$ npm ci .
```

Finally, make sure that the shell script in the `bin/` is executable.
```
$ pwd
src/SHIBA_INC_497_PROJECT/bin
chmod +x *
```

Now the environment is all set.

<br>

## Running the Develop on Localhost
First, setup the database by running:
```
$ pwd
src/SHIBA_INC_497_PROJECT/
$ ./bin/shiba_inc_db create
```
Second, compile the related ```bundle.js``` by running:
```
npx webpack
```
Make sure that you are compiling the correct JS file for the HTML you are testing every time you make changes to the JS files. 

Then start binding the website to `localhost:8000` by:
```
./bin/shiba_inc_run
```
Now you should be able to the website on `localhost:8000` in your browser.




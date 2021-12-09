# minbrowser
![minbrowser](https://user-images.githubusercontent.com/38807392/145425330-4605376d-52b7-42ae-893c-8c2df7d94e2e.gif)

## Description
This is a small browser developed as an example of programming with GTK and Python in ChromeOS.  
By clicking the button on the right of the screen, you can easily view the HTML of the page you are looking at.  
Other features are equivalent to those of a standard browser.  

## Environment setup for Debian
1. Install Python to execute `main.py`
    * `sudo apt install python`
2. Install python3-gi to use GTK
    * `sudo apt install python3-gi`
3. Install gir1.2-webkit2-4.0 to use WebKit
    * `sudo apt install gir1.2-webkit2-4.0`

## Execution method
`python3 main.py`

## Recommended development tool
* Glade(https://glade.gnome.org/) for ui editor
    * `sudo apt install glade`
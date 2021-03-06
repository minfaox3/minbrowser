# minbrowser
![minbrowser](https://user-images.githubusercontent.com/38807392/145830333-c75e1142-59a7-420f-b2ba-d19ea3170639.gif)
This is a small browser developed as an example of programming with GTK and Python in ChromeOS.  
By clicking the button on the right of the screen, you can easily view the HTML of the page you are looking at.  
Other features are equivalent to those of a standard browser.  

## Environment setup for Debian
1. Install Python to execute `main.py`.
    * `sudo apt install python`
2. Install python3-gi to use GTK.
    * `sudo apt install python3-gi`
3. Install gir1.2-webkit2-4.0 to use WebKit.
    * `sudo apt install gir1.2-webkit2-4.0`

## Execution method
`python3 main.py`

## Features
### Added
* Open multiple webpages in one window.
### Planned
* Change homepage
* Bookmark several webpages.
* Record history.
* Change icon theme.

## Recommended development tool
* Glade(https://glade.gnome.org/) for ui editor
    * `sudo apt install glade`

## LICENSE
minbrowser is free and open source software distributed under the [MPL-2.0 License](https://github.com/minfaox3/minbrowser/blob/main/LICENSE).

# Dustforce Stat Comparer
A terminal based project using the requests library to communicate with 
https://dustkid.com. It pulls user-time json data based on the chosen levelset 
and displays the information in a table.<br><br>
**NOTE: Due to the use of termcolor, this currently does not work on Linux 
operating systems**

![Model](https://i.ibb.co/rxDDqx4/Screenshot-2024-01-07-at-10-08-05-AM.png)

## Dependencies
[Tabulate](https://pypi.org/project/tabulate/) - Used to draw tables in 
terminal<br>
[Termcolor](https://pypi.org/project/termcolor/) - Add color to terminal 
output<br>
[BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) - Used for 
parsing HTML data from dustkid<br>
[Requests](https://pypi.org/project/requests/) - Used to make requests to 
https://dustkid.com

## Improvements
* Add Linux support
* Improve overall display of data
* Lower the amount of requests to dustkid

### Special thanks to...
* **Goost** for having a short unique name for testing
* **ThisIsNotJake** for having two dustkid profiles
* **Skyhawk** for having levelset data on all levelsets
* **MurphyTheTurtle** for helping me with python questions

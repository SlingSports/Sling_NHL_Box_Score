# NHL Scores
[![Join the chat at https://gitter.im/jtf323/NHL-Scores](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/jtf323/NHL-Scores?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A simple Python script to display the score of current and recently finished NHL games

![Example of finished and upcoming games](https://github.com/jtf323/NHL-Scores/blob/master/Screenshots/2015-04-30_Screenshot.PNG)

## Requirements
* Python 2.7
* Requests
    * `pip install requests`
* Colorama
    * `pip install colorama`

## Usage

To launch the script, ensure your system meets the requirements, open a terminal window and run

`python /path/NHL-Scores.py`

If you only want to see games for today you can run the sript with the `--today-only` flag

`python /path/NHL-Scores.py --today-only`


<br>
<br>

## Tested on
* OS X 10.10.3 with Python 2.7.9
* Windows 7 x64 with Python 2.7.9
* Ubuntu 14.04 x32 with Python 2.7.6

## License
The MIT License (MIT)

Copyright (c) 2015 John Freed

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
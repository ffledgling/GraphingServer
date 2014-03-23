Graphing Server
==============

The Centralized graphing server, generates graphs on the fly from data sent to it
over the network.
Useful for generating live plots from data from different servers on the network
on a central machine dedicated to the job.


INSTALL
-------

- Setup a virtualenv
- activate it
- `pip install numpy`
- `pip install matplotlib`
- Clone repo and you're done!

**Note: This setup does not seem to install everything for everyone**
You may want to install numpy and a couple of other deps before this.
See TODO.mkd regarding moving to a less demanding plotting framework.

HOWTO
-----

+ Almost all configuration for the Graphing server is managed via the config.py file
  Specify your incoming server details in as a python dict.
+ Define custom plotting functions in functions.py.
  Three defaults:
  1. The identify function
  2. Simple X vs Y
  3. Gb/unit vs unit 
  are available, use whichever you feel suits your needs or define your own.

  Your own function must be of the form:
  ```
  def myfunction(inp_list):
    # inp_list is a list of strings

    # do whatever here
    # do more whatever here

    # x, y must be either integers or reals
    return x, y
  ```
+ If the images are displayed in `/var/www/html/` or similar,
  the listener needs to be started as root.


Example
-------

Based on the default config

On the server side:

```
# python listener.py
```

On the client side:
```
for i in `seq 10`;do echo $i $(( $i * $i )) | nc localhost 9001; sleep 2; done;
```

Point your browser at `<GraphServer IP>/example.png` and refresh to see the graph build live.

#### Author

[Anhad Jai Singh](http://web.iiit.ac.in/~anhadjai.singh/)



# serial-reader

This project reads serial data from the arduino and saves it to an excel sheet. The inspiration for this project was a frustrating lab experiment I did in my third year, in which I had to record a video of the scale and later take observation from that data because I was too fase and there was too much data to take. I didn't like the procedure so I asked my professor if I could automate it. I have used serial data from arduino, and read it from the serial library in python. 
The outline of the project is following 

- Read data from serial output of arduino using Pyserial library of python. 
- Store the data in an excel sheet using excel writer. 
- Use pandas dataframe to analyse the data dn plot it. 

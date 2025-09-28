Hi! I know that this is not a traditional README file, and this is because I didn't want to edit the overall README on the GitHub. 

Below this line is a brief summary on my project as a whole. There is a section explaining the code itself too, if you are interested, jump to that part. 
Both parts are worth reading, even if you don't understand the code. 

_____________________________________________________________________________________________________________________________________________________________________

My project is predicting Ne using Selective Deaths. The code in these folders is representative of that, and mainly used to observe Selective Deaths. 

I am unsure if my Word Document, which has written process of all my work will be preserved once I leave this lab, so I will write the basics here. 


Selective Deaths: The deaths inside of a population that happens due to selection. It's a very noisy dataset, so we try to isolate the data in the best way that we can. 

Simulations have a burn-in period. We chose 4 * N, or 4 * Popsize to determine the burnin period. My apologies that in some places, it's hard-coded, and some places it's not. 
The burn-in period is just used to remove any inconsistencies in the data that the simulations use before converging. When the data converges, it just means that the simulation 
gets to running as intended. 

Another thing is that transforming this dataset is necessary to properly work with it.

We use Box-Cox transformations. It is a generalized function that changes per dataset you give it. Python does a lovely job at giving us the value of Lambda, which is used to transform 
the data in the generalized function. For each dataset, lambda differs. Python will give the most optimal lambda for each dataset, so be sure to remember to utlize that. 

Once we transform the data, this is where we can work with it if we'd like. Here, we can create histograms to see distributions, see if it's skewed still, etc. This is where you would 
compute the Standard Error for Error Bars too. Remember that we can still see the same distributions after back-transforming it too. 

But, we need to back-transform this data, to put it back into Selective Deaths form. Here's a little visual diagram. 

Selective Deaths --> Transformed Selective Deaths --> Back-Transformed Selective Deaths

Back-Transformed Selective Deaths is important because it's Selective Deaths with the removed noisy elements that we had. 


But to back-transform this, we need to use lambda. Luckily, I've derived the back-transformed equation and it's in parse_data.py. To find it, go into parse_data.py, and 
CTRL (or CMD) + F and type "back_transform".


From here, Ulises and I have experimented on different methods of applying things to the back-transformation to fit Ne. It's all in the parse_data.py file, just look around. 

We tried exponentiated Selective Deaths, and we tried applying the reproductive rate as well. 



Because we were fitting Selective Deaths to Ne, we need to find Ne. Luckily, our simulations have a way of getting that. Unsure where this originated, but I'm deriving Ne from 
the simulations. I believe the original code is from Walid, and Micaila has edited it? Either way I am using Walid's code. Before we were using Ne from our simulations, we were 
using them from a fwdpy11 simulation, where the values were already computed. Those will be listed as Matheson_ne, and they are irrelevant now that I am using Ne from simulations. 

I've modified Walid's code to compute Ne for each datafile, and also write Ne to files too. It takes about 90 seconds for me (M4 MBP) to compute Ne. I imagine a slower machine 
will take even longer. To combat this, I've made a function to WRITE all Ne data to a file. We can just gather the Ne data by running parse_data.get_all_nes(params). 




If you've got any questions about how this code works, please feel free to contact me! I'm unsure if I will remain in the Slack, so you can contact me by email. Any of these work!

cameronliu@arizona.edu ; (School)
cameron.j.liu@gmail.com ; (Professional)




*************************************************************************** Code Explanation ***************************************************************************

To properly simulate the graphs that I have, make sure you have all the proper files downloaded. 

Once you have all the files downloaded, make sure you have the datasets downloaded. They should be called "Datasets.zip". 
There will be plenty of files. They are sorted by SD, and all of them have Tskit on. Most of the population sizes is 2000, 
but a few of them (SD = 0.02, 0.04 has a population size of 20000. The other SD, which is 0.01, hasn't been run yet.)

First, go through all the files, and edit the following variables to the directories that you want it to be. 

In parse_data.py, it will be on line 20. Change variable called "home_directory" to what your current directory is. You can open VSCode terminal, and type "pwd". 
Copy and paste that into the home_directory. 

In "seldeath-hist.ipynb", "seldeath-timeseries.ipynb", and "seldeath-ne.ipynb", change the variable "output_path" to where you want the grapsh to be stored. 
For example, mine was "/..../cameronliu/Research/.../Selective Death Histograms/". 

Now, it's important to get the data for Ne. Run the file called "calculate_coalescent_ne.ipynb". 
This file takes a bit to run, but it goes through the specified datasets in the parameters "sds = []". Be sure to change these to what you need them to be.
This file doesn't output anything important, but just stores the relevant Ne's in a file. 

From there, you are finally able to run these scripts. We need to check if the burn-in period for the simulations is long enough. 
Run "seldeath-timeseries.ipynb", and check if the burnin period that we have specified is long enough, and if the simulation has reached convergence. 

Notice anything? I notice that the data is still pretty noisy, it's got a decent amount of variability. How do we get rid of this? 

So from there, you can run the file "seldeathhist.ipynb". 

We can plot our data in a histogrram to see what our data looks like. We can see that the data is still skewed. 
To be able to get rid of this skew we must transform the data. To do this, we use the Box-Cox transformations. 

Behind the scenes of these transformations, it basically transforms the dataset using a calculated value called lambda. This value is important later on. 

My code stores lambda and the transformed datasets together. 

From there, the basis of my project is to compare Selective Deaths to Ne. We can plot Ne using our simulations. 

Run the file called "seldeath-ne.ipynb". This file is just comparing Ne vs. Selective Deaths vs. Matheson's background selection equation. 
This back-transforms the dataset from when we transformed it earlier before plotting anything. This is to get the data in terms that we like. 

From there, that's all I've done for this project! I hope my code and work isn't too messy -- my apologies if it is!!

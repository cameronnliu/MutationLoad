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

parse_data.py is the accumulation of all my Python Functions that I've used to modify data. It can be a bit messy, and if I had more time, I would've gone back and refactor the code. 
    All the functions in parse_data.py are useful. To get access to these functions, type "import parse_data" at the top of your Python file. To use the functions, first, read how the 
    respective function works. Then, you can call it using parse_data.function_name(params).

I've got a lot of different .py files that kind of do the same thing. This is because I found it easier to restart some of the code, rather than edit pre-existing code. This may just be 
a bad habit of mine, but I'll list the working ones that anyone can use if they just change their directory. 
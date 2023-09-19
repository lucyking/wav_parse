## Usage
### 1. Format wav file
> https://stackoverflow.com/questions/14321627/scipy-io-wavfile-gives-wavfilewarning-chunk-not-understood-error   
> The easiest solution to this problem is to convert the wav file into other wav file using SoX.

`$ sox a.wav a2.wav`

### 2. Parse wav file 
`$ python main.py a2.wav`


### 3. Parse result
store in \*\_plot.png file.
```
fileName_prefix = int(time.time())
plt.savefig(str(fileName_prefix) + '_plot.png')
```

eg. [1695116877_plot.png](https://raw.githubusercontent.com/lucyking/wav_parse/main/1695116877_plot.png) ![png1](1695116877_plot.png)


### 4. Dependence
Install these python 3rd libs if necessary.
```
import pylab as pl
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as n
```

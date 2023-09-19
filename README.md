## Usage
### 1. format wav file
> https://stackoverflow.com/questions/14321627/scipy-io-wavfile-gives-wavfilewarning-chunk-not-understood-error
> The easiest solution to this problem is to convert the wav file into other wav file using SoX.
`$ sox a.wav a2.wav`

### parse wav file 
`$ python main.py a2.wav`


### parse result
store in \*\_plot.png file.
```
fileName_prefix = int(time.time())
plt.savefig(str(fileName_prefix) + '_plot.png')
```

eg. ![png1](1695116877_plot.png)

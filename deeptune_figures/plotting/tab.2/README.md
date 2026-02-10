# DeepTune Experiment Results

## Overview  
 
The measurements presented in the accompanying table were collected manually. Due to the nature of the data collection process, there is currently no Python code or automated script that can reproduce these results.  

## Performance Measurements  
  
The table below shows the best-performing configurations found by WayFinder applied to Linux 4.19 after 250 iterations.  

| **App.** | **Default config.** | **Way-Finder** | **Perf. unit** | **Relative Perf.** | **Avg. time to find** | **Avg. time to find** |  
|----------|---------------------|----------------|----------------|--------------------|-----------------------|-----------------------|  
|          |                     |                |                |                    | **No TL**             | **TL**               |  
| Nginx    | 15731               | 19593          | req/s          | 1.24x              | 415s                  | 92s                   |  
| Redis    | 58000               | 66118          | req/s          | 1.14x              | 312s                  | 69s                   |  
| SQLite   | 284                 | 284            | μs/op          | 1x                 | 248s                  | 76s                   |  
| NPB      | 1497                | 1522           | Mop/s          | 1.02x              | 243s                  | 76s                   |  

# Image Compressor for Web Servers

This program has been created to reduce the size on web servers to increase the performance of the page loading. Despite my efforts to make the program as generic as possible, I must admit that it's been designed around my need to batch-compress all the images in one of my customers' Prestashop store.

## How it works
The program duplicates the entire tree of the filesystem (starting from the specified path), and converts all the images in the subfolders, keeping the same folder structure.

The idea is that after running the program you could effortlessly switch to the new folder tree with compressed images with nearly no downtime (the time to rename the folder).

#### Usage

1. Clone the repo on your web server `git clone https://github.com/LucaMozzo/WebServerImageCompressor.git`
2. Enter the folder `cd WebServerImageCompressor`
3. Install the libraries (TODO)
4. Run `python3 compress.py ... ... ` TODO

#### Example of applicability on a Prestashop store

Prestashop stores the product images in the folder `img/p/`.
TODO

## Performance considerations

One of the parameters that you can specify is the number of threads. The number of threads needs to be considered carefully before running the script.

#### More threads =/= less time to complete

Creating a thread has an overhead, so this overhead needs to be worth the effort. For example (using random numbers here) if creating a thread takes 1ms and the operations to be executed also take 1ms, you're probably better off performing those operations sequentially. What I'm saying here is that the time you save by parallelizing the work should be higher than the time spent scheduling the threads.

##### The experiment
In this section I approach this problem experimentally. I have a folder with multiple subfolders, which ultimately contain 5772 images stored on a HDD. The total size of those images is ~105MB, and their size is variable (from 64x64 to 1000+x1000+)

I then ran the script with multiple number of threads and plotted the execution time against the number of threads and here's the result:

![Performance chart](performance_chart.png)

TODO add values and STD DEV

#### CPU & Disk utilisation

As you would expect, more operations done in "parallel" mean higher resource utilisation, and more importantly, less resources available for servicing incoming requests (more threads to be scheduled = less CPU time for each of the threads). This means that running this script on a production server with limited resources will slow down the response time, the extent of which has not been measured (as it's extremely variable).
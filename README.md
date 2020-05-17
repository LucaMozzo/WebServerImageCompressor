# Image Compressor for Web Servers

This program has been created to reduce the size on web servers to increase the performance of the page loading. Despite my efforts to make the program as generic as possible, I must admit that it's been designed around my need to batch-compress all the images in one of my customers' Prestashop store.

## How it works
The program duplicates the entire tree of the filesystem (starting from the specified path), and converts all the images in the subfolders, keeping the same folder structure.

The idea is that after running the program you could effortlessly switch to the new folder tree with compressed images with nearly no downtime (the time to rename the folder).

#### Usage

1. Clone the repo on your web server `git clone https://github.com/LucaMozzo/WebServerImageCompressor.git`
2. Enter the folder `cd WebServerImageCompressor`
3. Install the libraries:
   ```shell script
   python3 -m pip install console-progressbar
   python3 -m pip install PIL
   ```
4. Run e.g. `python3 compress.py --source ~/source --output ~/destination --quality 70 --logs ~/failures.log`

| Argument name | Required | Description                                                                            |
|---------------|----------|----------------------------------------------------------------------------------------|
| --source      | Yes      | The base directory (or the image path) where the image(s) is(are)                      |
| --output      | Yes      | The base directory (or image path) where the compressed image(s) will be saved         |
| --quality     | Yes      | A value 1-100 of the output quality, where 100 is the current quality (no compression) |
| --logs        | No       | The file where to write the failures                                                   |

#### Example of application on a Prestashop store

Prestashop stores the product images in the folder `img/p/`. So let's assume our prestashop installation is in `/var/www/html/prestashop`.

We would run the script 
```shell script
python3 compress.py --source /var/www/html/prestashop/img/p/ --output /var/www/html/prestashop/img2/p/ --quality 70 --logs ~/failures.log
```

Then check the failed images in the output logs file and make adjustments as needed.

To switch between the current images and the compressed ones, we make a folder name swap
```shell script
mv -r /var/www/html/prestashop/img/ /var/www/html/prestashop/img_old/ && mv -r /var/www/html/prestashop/img2/ /var/www/html/prestashop/img/
```
Now the original images will be in the folder `img_old` and the compressed ones in `img` and will be used by Prestashop for future requests.

## Performance considerations

One of the parameters that you can specify is the number of threads. The number of threads needs to be considered carefully before running the script.

#### More threads =/= less time to complete

Creating a thread has an overhead, so this overhead needs to be worth the effort. For example (using random numbers here) if creating a thread takes 1ms and the operations to be executed also take 1ms, you're probably better off performing those operations sequentially. What I'm saying here is that the time you save by parallelizing the work should be higher than the time spent scheduling the threads.

##### The experiment
In this section I approach this problem experimentally. I have a folder with multiple subfolders, which ultimately contain 5772 images stored on a HDD. The total size of those images is ~105MB, and their size is variable (from 64x64 to 1000+x1000+).

I then ran the script with multiple number of threads and plotted the execution time against the number of threads and here's the result:

![Performance chart](performance_chart.png)

TODO add values and STD DEV

#### CPU & Disk utilisation

As you would expect, more operations done in "parallel" mean higher resource utilisation, and more importantly, less resources available for servicing incoming requests (more threads to be scheduled = less CPU time for each of the threads). This means that running this script on a production server with limited resources will slow down the response time, the extent of which has not been measured (as it's extremely variable).
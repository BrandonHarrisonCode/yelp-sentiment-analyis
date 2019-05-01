# NLP Yelp Dishes Sentiment Analysis
This project is designed to comb through Yelp reviews for various restaurants, find the different dishes that are mentioned in reviews, and then rank the dishes based on how positive people are when they talk about them in their reviews.

# Running
This project is split up into several different independent stages.  Each stage has its own independent directory, and each directory is designed to be run as a Docker container.  Each directory has the three following files:
1. `Makefile`
2. `Dockerfile`
3. `requirements.txt`

The `Makefile` defines the commands that are needed to run the container locally.  To launch any given container simply `cd` into the directory and run `make run`.  The stage will build an image and then run the image in a container on your system.  Check the details of the `Makefile` for specific details of exposed ports or required API keys that you may need to run the stage.  The `Makefile` runs the image built by both the `Dockerfile` and `requirements.txt` file, so check here if you want to know what's going on in the background.

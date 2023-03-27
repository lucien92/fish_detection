This document contains 4 files which constitute the key steps of our algorithm

0)An introduction to the problem of the stock gestion of fishes, analysing tabular data

1)First of all a method of scrapping Inaturalist which consists in recovering the images of this site specialized in biology. It is coded in a dynamic way (JavaScript style) so we are obliged to integrate a method of scrolling which consists in 'going down' at the end of each page, to wait for the end of a loading then to recover the images by a wget method and a study of the CSS style of the page.

2)Once these images are recovered, we can then train our convolutional neural network. We chose a ResNet101, a particularly powerful network (several million parameters), a learning rate scheduler SGD to which we added a ReduceLROnPlateau in cases where the loss would be 'blocked' in a local extremum. After splitting our dataset in three sets, we launch a training.

3)Analysis of our results. We analyze our results in three main ways: 

-First, a study of the classical metrics of machine learning, i.e. F1 score, accuracy, precision and recall.

-Then we study the possible confusions between the classes, which could give us for example indications on the inter-species similarities.

-Finally, we set up a rather complex method, called Grad-CAM method, which consists in superimposing an image on a matrix called heatmap that we filled with red shades (by filling 0 and 0 for the blue and green pixels and a number between 0 and 1 for the red). We chose the shade of red that each coefficient of the heatmap numpy array should carry by removing the last layer (dense classification layer) of our convolutional network and by looking at the evolution of the gradient of our encoder. The areas of the image to which the encoder gave the most importance being marked by a strong gradient (thus impacting more the loss in the gradient descent) are then noted with a strong coeffcient in the heatmap. The result of the superposition of the heatmap with the image is quite interesting since it allows to highlight the limits of the constitution of the database by deep learning scrapping methods, even when it is about professional websites like Inaturalist. Indeed, we notice for example on a photo that it is the fisherman carrying the fish that is marked the most by red, and not the fish. The network must have learned to recognize the fishermen because there must have been many in the database. This is bad because if a class contains a lot of fishers carrying fish it may be identified for the wrong reasons and will therefore be easily confused with a photo from another class.

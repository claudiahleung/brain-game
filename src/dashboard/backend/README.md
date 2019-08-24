# NMT (NeuroTechX Machine Learning Tools)

### Installing requirements
`pip install requirements.txt`

### Running the code
BrainActivity takes in raw unprocessed data as input, that can either be of shape (4,), (1,4) or (x,4) where x is an int > 0.

BrainActivity then does an average of the input arrays and runs a normalization (using Sklearn).

Next, BrainActivity will run either a RandomForest prediction or a KNN prediction.

The function will return either `"left"`, `"right"` or `"rest"`

```python
from NMT.BrainActivity import *

X = [0,0,0,0] 	# dummy data
rf_predict(X)	# returns either "left", "right", or "rest" using random forest classifier
knn_predict(X)	# returns either "left", "right", or "rest" using knn classifier
```

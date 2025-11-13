# napari-musa

**M**ultimodal f**U**sion framework for **S**pectral **A**nalysis (MUSA) is a Napari plugin designed for the analysis of hyperspectral imaging datasets. It allows for data visualization and processing, fusion of registered datasets from different techniques and employement of various dimensionality reduction algorithms.
The plugin features seven main tabs: **Data Manager**, **Data Visualization**, **Fusion**, **UMAP**, **PCA**, **NMF** and **Endmembers extraction**.

## Data Manager widget
The Data Manager widget is used to open, process and manipulate hyperspectral datasets.

### How to open a file
Supported file extensions: '.mat' and '.h5'. The file must contain a hyperspectral cube (3D array) and a calibration array.
The accepted variables names are:
- for the **hyperspectral cube**: 'data', 'data_RIFLE', 'Y', 'Hyperspectrum_cube', 'XRF_data', 'spectra', 'HyperMatrix'.
- for the **calibration array**: 'WL', 'WL_RIFLE', 'X', 'fr_real', 'wavelength', 'ENERGY', 't'.
If a variable name is not present in the lists before, the program will ask for it.

**Steps**:
1. Choose imaging mode from the dropdown.
2. Click *Open File*.

**Contrast Adjustment**: Use the *layer controls* tab. Click once for single image contrast, or continuous for automatic adjustment across the hypercube.

### Data Manager features
- **Save box**: This command will save the selected layer. Specifically, Hypercubes and abundances maps (NMF, NNLS, SAM) can be saved in .mat and .h5, while True/False RGB and labesls layers will be saved as .png or .jpeg.
- **Crop box**: Crop the datasets both spatially and spectrally.
- **Mask box**: Create a mask from the data, starting from a selected label layer.
- **Data cleaning box**: Offers 2D median, 2D Gaussian and Savitzky-Golay filters. Select desired options, adjust parameters, click *Process data*, and wait for the confirmation message.
It also offers SVD denoising and background subtraction through SNIP algorithm.
- **Create Derivative**: Computes the spectral derivative hypercube. Recommended after preprocessing.
- **Dimensionality reduction**: Supports spatial and spectral reduction via Discrete Wavelet Transform (DWT). Select reduction type(s) and click *Reduce data*.

### Spatially cropping the hypercube
1. Select the *Shapes* layer.
2. Use a rectangle tool (**only rectangular shapes are supported**).
3. Click *Crop*.
4. (Optional) Delete the original layer.
**TIP**: Keep the cropping *Shapes* layer if fusing multiple datasets and reuse the same shape on a second registered dataset for identical cropping.

### Spectrally cropping the hypercube
1. Insert the minimum and maximum channels you want to keep (they can be found on bottom right).
2. Click *Crop wavelengths*.

### Create a mask
1. Select the *Labels* layer.
2. Choose selection tool: brush, polygon, or fill bucket.
3. Click *Create Mask*.
**Note**: If you are working on a reduced dataset,enable *From reduced dataset*.


## Data Visualization widget
### Data visualization features
- **Create RGB image**: Generates an RGB image of the hypercube.
- **Create False RGB image**: Generates a false RGB image of the hypercube by selecting the spectral bands.
- **Plot the mean spectrum**: Plot the mean spectrum of the selected area.

### Create false RGB
Choose three bands and click *Create False RGB* to generate a false-color image.

### Plot the mean spectrum
1. Select or create a Labels layer.
2. Highlight the area using a selection tool.
3. Click *Mean spectrum*.
It is possible to select other options: with standard deviation, normalized, derivative (if previously computed).
Enable *Reduced dataset* if working on reduced data.
![raw](https://github.com/alessiadb/napari-hsi-analysis/blob/main/images/MeanSpectrum_GIF.gif)

You can also export spectra as '.txt' using *Export spectra in .txt*.


## Fusion widget
The Fusion widget combines two or three opened datasets.

### How to fuse datasets
1. Select up to three datasets.
2. Click *Fuse the chosen datasets*. A popup will confirm when the fused dataset is ready.

**Note**: When fusing reduced datasets (recommended for UMAP), ensure all selected datasets are reduced.


## UMAP widget

### How to perform UMAP analysis
1. Enable *Apply to reduced dataset* checkbox if applicable (It is **highly recommended** to first preprocess and then reduce the datasets).

2. Check the parameters (it is recomended to keep the minimum distance at 0, but you can play with the number of neighbours). Chose the metric between euclidean and cosine.

3. Click *Run UMAP*. A popup will notify completion.

4. Click *Show UMAP scatterplot*. You can customize point size.

To select areas, use polygon selection and draw the region (double-click to close). Click the add button to finalize.
The selection creates a label layer usable for spectrum plotting or mask creation.

### Additional features
**Show UMAP scatterplot in True RGB**: It is possible to show the scatterplot as true RGB. Tick the *Scatterplot with the True RGB* checkbox and press again *Show UMAP scatterplot*.

**Change Dimension of scatterpoint**: It is possible to change the dimension of the points within the scatterplot. Select the *Point size* and press again *Show UMAP scatterplot*.

**Select an area in the image and visualize the points in the UMAP scatterplot**: It is also possible to select an area on the image (through the label layer) and then check in which area of the scatterplot it is located, by pushing the button *Show areas of Label Layer on scatterplot*.


## Example - Mask from fused dataset
This example demonstrates how areas selected via masks can be re-analyzed with UMAP.
![raw](https://github.com/alessiadb/napari-hsi-analysis/blob/main/images/MASK_GIF.gif)

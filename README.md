# Infrasound Data Augmentation and Classification (IDAC)

IDAC is a suite of functions to 
1.  Generate a synthetic dataset by propagating a variety of source time functions through realistic atmospheres
1.  Classify infrasound signals by training machine learning (ML) models 
1.  Predict real (or synthetic) data in near real time

The motivation of the repository was to identify large nuclear blast waves from single sensor infrasound microphones but other applications including volcano monitoring are feasable. 

## Installation Instructions and Dependencies
IDAC depends on a number of softwares and codes.  Testing is currently focusing on linux and mac os systems.  


### AVOG2S 

The software [AVOG2S](https://github.com/usgs/volcano-avog2s) generates atmospheres using climatological and reanalysis models.  AVOG2S can be installed easily on Linux and Mac Os via homebrew.  

1.  install homebrew by typing (only needed once, if not already installed): 

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2.  tap the [Alaskan Volcano Observatories's (AVO) repository](https://github.com/ibrewster/homebrew-avo) (only needed once)

`brew tap ibrewster/avo`

3.  install the AVOG2S formula using homebrew 

`brew install avog2s`

### NCPAProp
NCPAProp is used to propagate source time functions (e.g. blast waves) through the modeled atmospheres. 

To install NCPAProp: 

1.  Download the NCPAProp software from its github repo: [NCPAprop](https://github.com/chetzer-ncpa/ncpaprop)
2.  Open a terminal and `cd` into the directory where the code was downloaded and run `./configure with appropriate parameters`. For example, to download and install PETSc and SLEPc locally to the ncpaprop installation:

`./configure --with-localpetsc --enable-autodependencies`

For more information on how to use `./configure` see the [NCPAprop manual](https://github.com/chetzer-ncpa/ncpaprop/blob/master/docs/ncpaprop-manual.pdf) and search for */configure* or *installation overview*.  As a side note, the NCPAprop manual is a wonderful reference to better understand how waveforms are propagated.  

3.  Run `make`

### Python Dependencies and Conda Environment
IDAC requires several python modules, which are listed below.  The easiest way to install these dependencies to build the environment from the idac_environment.yml file in the root directory in the idac repository.  

To build the environment from the a .yml file, make sure you have [conda installed](https://docs.conda.io/projects/conda/en/latest/user-guide/install/), then from the idac_linux_environment.yml file:

1.  Open a terminal and `cd` into the directory where the idac repo is downloaded.  
2.  build the environment with: 
`conda env create -f idac_linux_environment.yml`
3.  After building the environment, be sure to activate it with: 
`conda activate idac`

### Building environment manually 
If you are running a different operating system, or you prefer to build the environment manually: 

1.  Create an environment with the 'correct' version of python
`conda create --name idac python=3.5 `
2.  Install obspy with:
`conda install obspy`




# Infrasound Data Augmentation and Classification (IDAC)

IDAC is a suite of functions to 
1.  Generate a synthetic dataset by propagating a variety of source time functions through realistic atmospheres
1.  Classify infrasound signals by training machine learning (ML) models 
1.  Predict real (or synthetic) data in near real time

The motivation of the repository was to identify large nuclear blast waves from single sensor infrasound microphones but other applications including volcano monitoring are feasable. 

## Installation Instructions and Dependencies
IDAC depends on a number of softwares and codes.  Testing is currently focusing on linux and mac os systems.  


### AVOG2S 

The software AVOG2S generates atmospheres using climatological and reanalysis models.  AVOG2S can be installed easily on Linux and Mac Os via homebrew.  

1.  install homebrew by typing (only needed once, if not already installed): 

`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`

2.  tap the Alaskan Volcano Observatories's (AVO) repository (only needed once)

`brew tap ibrewster/avo`

3.  install the AVOG2S formula using homebrew 

`brew install avog2s`

### NCPAProp
NCPAProp is used to propagate source time functions (e.g. blast waves) through the modeled atmospheres. 

To install NCPAProp: 

1.  Download the NCPAProp software from its github repo: [NCPAprop](https://github.com/chetzer-ncpa/ncpaprop)
2.  Open a terminal and `cd` into the directory where the code was downloaded and run ./configure with appropriate parameters. For example to download and install PETSc and SLEPc locally to the ncpaprop installation:

`./configure --with-localpetsc --enable-autodependencies`

For more information on how to use `./configure` see the [NCPAprop manual](https://github.com/chetzer-ncpa/ncpaprop/blob/master/docs/ncpaprop-manual.pdf) and search for */configure* or *installation overview*.  As a side note, the NCPAprop manual is a wonderful reference to better understand how waveforms are propagated.  

3.  





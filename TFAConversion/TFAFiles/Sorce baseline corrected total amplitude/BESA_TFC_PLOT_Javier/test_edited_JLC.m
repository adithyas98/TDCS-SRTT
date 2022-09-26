clear
close all
pack
clc

%
% run eeglab first (manually) and close it. That's it
% Eeglab will take care of updating the Matlab's path
%
cd('C:\Users\sehat\Documents\MATLAB\eeglab13_4_4b')
eeglab
close

% Paths (where my converter lives)
cd('C:\Users\sehat\Documents\MATLAB\Columbia_scripts\BESA_TFC_PLOT'); % (Pc)

%
% Convert and load my tfc file (into a TFA structure)
%
fs = 500; % sample rate (check this out)
file_path = 'C:\Users\sehat\Documents\MATLAB\Columbia_scripts\raw_eeg_data\TFC'; % where my tfc files are (Pc)
fullname = fullfile(file_path, 'SS-Vertex-during_ERP_induced_surface_new.tfc');
TFA = BESAtfc2TFA(fullname, fs);

datatype  = 0; % 0 = total power, 1 = phase, 2 = amplitude, 3 = ITC
binArray  = 1; % Bin indices to plot (only 1 at the current version...)
chanArray = [5]; % channels (maximum = TFA.nchan)
amprange  = [0 0.2]; % Amplitude range (either uV2, uV, depending on datatype. Displayed as colormap) to plot.
twindow   = [-200 200 -200:50:200]; % Time window where the first two numbers are the min and max and then remaining numbers designate the ticks
fwindow   = [4 50    1 4 10 20 30 40 50 ]; % frequency window structured similarly to the twindow
blcwin    = [-200 -100]; % Baseline correction window
blctype   = 'subtractive'; % 'subtractive','divisive','TSE', or 'none' are the other types
fshading  = 'interp'; % Controls of color shading. Can be 'flat' or  'interp'.
fcontour  = 'off'; % displays isolines calculated from matrix Z and fills the areas between the isolines using constant colors corresponding to the current figure's colormap. Can be 'on' or  'off'.
Ylog      = 0; % Logarithmic scale for frequency range (fwindow). Can be 1 (means apply log scale)  or  0 (means apply linear scale).
plotype   = 1; % Plotting style: 0 means topographic; 1 means rectangular array. IMPORTANT: if you enter chanArray as a cell array then this 'plotype' option will be ignored.
surfacetype = '2D'; % '2D' or '3D'
clrbar = 1; % 0 = colorbar off, 1 = on
cbname  = 'jet';
cbscale = 'linear';% 'dB', 'whitened'

%
% Plot
%
plotTFA(TFA, datatype, binArray, chanArray, amprange, twindow, fwindow, blcwin, blctype, fshading, fcontour, Ylog, plotype, surfacetype, cbname, cbscale)
%colorbar


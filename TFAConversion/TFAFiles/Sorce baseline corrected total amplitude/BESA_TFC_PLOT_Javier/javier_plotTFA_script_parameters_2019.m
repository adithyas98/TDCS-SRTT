datatype  = 0; % 0 = total power, 1 = phase, 2 = amplitude, 3 = ITC
binArray  = 1; % Bin indices to plot (only 1 at the current version...)
chanArray = [1 5 12 17]; % channels (maximum = TFA.nchan)
amprange  = [0 .8]; % Amplitude range (either uV2, uV, depending on datatype. Displayed as colormap) to plot.
twindow   = [-50 200 -50:50:200]; % Time window where the first two numbers are the min and max and then remaining numbers designate the ticks
fwindow   = [4 50    1 4 8 12 25 50 ]; % frequency window structured similarly to the twindow
blcwin    = [-50 50]; % Baseline correction window
blctype   = 'subtractive'; % 'subtractive','divisive','TSE', or 'none' are the other types
fshading  = 'interp'; % Controls of color shading. Can be 'flat' or  'interp'.
fcontour  = 'off'; % displays isolines calculated from matrix Z and fills the areas between the isolines using constant colors corresponding to the current figure's colormap. Can be 'on' or  'off'.
Ylog      = 1; % Logarithmic scale for frequency range (fwindow). Can be 1 (means apply log scale)  or  0 (means apply linear scale).
plotype   = 1; % Plotting style: 0 means topographic; 1 means rectangular array. IMPORTANT: if you enter chanArray as a cell array then this 'plotype' option will be ignored.
surfacetype = '2D'; % '2D' or '3D'
clrbar = 0; % 0 = colorbar off, 1 = on
cbname  = 'jet';
cbscale = 'linear';% 'dB', 'whitened'

%
% Plot
%
plotTFA(TFA, datatype, binArray, chanArray, amprange, twindow, fwindow, blcwin, blctype, fshading, fcontour, Ylog, plotype, surfacetype, cbname, cbscale)
